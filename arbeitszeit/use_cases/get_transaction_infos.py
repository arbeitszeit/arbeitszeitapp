from dataclasses import dataclass
from typing import List, Union, Dict
from datetime import datetime
from decimal import Decimal

from injector import inject

from arbeitszeit.entities import (
    AccountTypes,
    Company,
    Member,
    SocialAccounting,
    Transaction,
)
from arbeitszeit.repositories import (
    AccountOwnerRepository,
    MemberRepository,
    TransactionRepository,
)


@dataclass
class TransactionInfo:
    date: datetime
    sender_name: str
    receiver_name: str
    transaction_volumes: Dict[str, Decimal]
    purpose: str


@inject
@dataclass
class GetTransactionInfos:
    transaction_repository: TransactionRepository
    member_repository: MemberRepository
    acount_owner_repository: AccountOwnerRepository

    def __call__(self, user: Union[Member, Company]) -> List[TransactionInfo]:
        return [
            self._create_info(user, transaction)
            for transaction in self._get_all_transactions_sorted(user)
        ]

    def _create_info(
        self,
        user: Union[Member, Company],
        transaction: Transaction,
    ) -> TransactionInfo:
        sender, user_is_sender = self._get_sender(transaction, user)
        receiver, user_is_receiver = self._get_receiver(transaction, user)
        sender_name = self._get_sender_name(sender, user_is_sender)
        receiver_name = self._get_receiver_name(receiver, user_is_receiver)

        if isinstance(user, Company):
            transaction_volumes = self._get_volumes_for_company_transaction(
                transaction,
                user,
                user_is_sender,
                user_is_receiver,
            )
        else:
            transaction_volumes = self.__get_volume_for_member_transaction(
                transaction, user_is_sender, user_is_receiver
            )

        return TransactionInfo(
            transaction.date,
            sender_name,
            receiver_name,
            transaction_volumes,
            transaction.purpose,
        )

    def _get_all_transactions_sorted(self, user):
        all_transactions = []
        for account in user.accounts():
            all_transactions.extend(
                self.transaction_repository.all_transactions_sent_by_account(account)
            )
            all_transactions.extend(
                self.transaction_repository.all_transactions_received_by_account(
                    account
                )
            )

        # delete duplicate transactions, where user is sender and receiver
        transactions_without_duplicates = []
        transactions_checked = set()
        for trans in all_transactions:
            if trans.id in transactions_checked:
                pass
            else:
                transactions_without_duplicates.append(trans)
                transactions_checked.add(trans.id)

        all_transactions_sorted = sorted(
            transactions_without_duplicates, key=lambda x: x.date, reverse=True
        )
        return all_transactions_sorted

    def _get_sender(self, transaction, user):
        if transaction.account_from in user.accounts():
            sender = user
            user_is_sender = True
        else:
            sender = self.acount_owner_repository.get_account_owner(
                transaction.account_from
            )
            user_is_sender = False
        return sender, user_is_sender

    def _get_receiver(self, transaction, user):
        if transaction.account_to in user.accounts():
            receiver = user
            user_is_receiver = True
        else:
            receiver = self.acount_owner_repository.get_account_owner(
                transaction.account_to
            )
            user_is_receiver = False
        return receiver, user_is_receiver

    def _get_sender_name(self, sender, user_is_sender):
        if user_is_sender:
            sender_name = "Mir"
        elif isinstance(sender, Company) or isinstance(sender, Member):
            sender_name = sender.name
        elif isinstance(sender, SocialAccounting):
            sender_name = "Öff. Buchhaltung"

        return sender_name

    def _get_receiver_name(self, receiver, user_is_receiver):
        if user_is_receiver:
            receiver_name = "Mich"
        else:
            receiver_name = receiver.name
        return receiver_name

    def _get_volumes_for_company_transaction(
        self,
        transaction,
        user,
        user_is_sender,
        user_is_receiver,
    ):
        if user_is_sender and user_is_receiver:  # company buys from itself
            transaction_volumes = self._get_volumes_for_company_transaction_if_company_is_sender_and_receiver(
                transaction,
                user,
            )

        elif user_is_sender:
            transaction_volumes = (
                self._get_volumes_for_company_transaction_if_company_is_sender(
                    transaction,
                    user,
                )
            )

        elif user_is_receiver:
            transaction_volumes = (
                self._get_volumes_for_company_transaction_if_company_is_receiver(
                    transaction,
                    user,
                )
            )

        return transaction_volumes

    def _get_volumes_for_company_transaction_if_company_is_sender_and_receiver(
        self, transaction, user
    ):
        transaction_volumes = {}
        transaction_volumes[AccountTypes.p.value] = (
            -1 * transaction.amount
            if transaction.account_from == user.means_account
            else ""
        )
        transaction_volumes[AccountTypes.r.value] = (
            -1 * transaction.amount
            if transaction.account_from == user.raw_material_account
            else ""
        )
        transaction_volumes[AccountTypes.a.value] = (
            -1 * transaction.amount
            if transaction.account_from == user.work_account
            else ""
        )
        transaction_volumes[AccountTypes.prd.value] = (
            1 * transaction.amount
            if transaction.account_to == user.product_account
            else ""
        )
        return transaction_volumes

    def _get_volumes_for_company_transaction_if_company_is_sender(
        self,
        transaction,
        user,
    ):
        transaction_volumes = {}
        factor = -1
        transaction_volumes[AccountTypes.p.value] = (
            factor * transaction.amount
            if transaction.account_from == user.means_account
            else ""
        )
        transaction_volumes[AccountTypes.r.value] = (
            factor * transaction.amount
            if transaction.account_from == user.raw_material_account
            else ""
        )
        transaction_volumes[AccountTypes.a.value] = (
            factor * transaction.amount
            if transaction.account_from == user.work_account
            else ""
        )
        transaction_volumes[AccountTypes.prd.value] = (
            factor * transaction.amount
            if transaction.account_from == user.product_account
            else ""
        )
        return transaction_volumes

    def _get_volumes_for_company_transaction_if_company_is_receiver(
        self,
        transaction,
        user,
    ):
        transaction_volumes = {}
        transaction_volumes[AccountTypes.p.value] = (
            transaction.amount if transaction.account_to == user.means_account else ""
        )
        transaction_volumes[AccountTypes.r.value] = (
            transaction.amount
            if transaction.account_to == user.raw_material_account
            else ""
        )
        transaction_volumes[AccountTypes.a.value] = (
            transaction.amount if transaction.account_to == user.work_account else ""
        )
        transaction_volumes[AccountTypes.prd.value] = (
            transaction.amount if transaction.account_to == user.product_account else ""
        )
        return transaction_volumes

    def __get_volume_for_member_transaction(
        self, transaction, user_is_sender, user_is_receiver
    ):
        transaction_volumes = {}
        if user_is_sender:
            transaction_volumes[AccountTypes.member.value] = -transaction.amount
        elif user_is_receiver:
            transaction_volumes[AccountTypes.member.value] = transaction.amount

        return transaction_volumes

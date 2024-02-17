from __future__ import annotations

from dataclasses import dataclass
from typing import List

from arbeitszeit.datetime_service import DatetimeService
from arbeitszeit.transactions import TransactionTypes
from arbeitszeit.use_cases.show_prd_account_details import (
    ShowPRDAccountDetailsUseCase as UseCase,
)
from arbeitszeit_web.translator import Translator
from arbeitszeit_web.url_index import UrlIndex
from arbeitszeit_web.www.navbar import NavbarItem


@dataclass
class ShowPRDAccountDetailsPresenter:
    @dataclass
    class TransactionInfo:
        transaction_type: str
        date: str
        transaction_volume: str
        purpose: str
        peer_name: str
        peer_type_icon: str

    @dataclass
    class ViewModel:
        transactions: List[ShowPRDAccountDetailsPresenter.TransactionInfo]
        show_transactions: bool
        account_balance: str
        plot_url: str
        navbar_items: list[NavbarItem]

    translator: Translator
    url_index: UrlIndex
    datetime_service: DatetimeService

    def present(self, use_case_response: UseCase.Response) -> ViewModel:
        transactions = [
            self._create_info(transaction)
            for transaction in use_case_response.transactions
        ]
        return self.ViewModel(
            transactions=transactions,
            show_transactions=bool(transactions),
            account_balance=str(round(use_case_response.account_balance, 2)),
            plot_url=self.url_index.get_line_plot_of_company_prd_account(
                use_case_response.company_id
            ),
            navbar_items=[
                NavbarItem(
                    text=self.translator.gettext("Accounts"),
                    url=self.url_index.get_company_accounts_url(
                        company_id=use_case_response.company_id
                    ),
                ),
                NavbarItem(
                    text=self.translator.gettext("Account prd"),
                    url=None,
                ),
            ],
        )

    def _create_info(self, transaction: UseCase.TransactionInfo) -> TransactionInfo:
        assert transaction.transaction_type in [
            TransactionTypes.sale_of_consumer_product,
            TransactionTypes.sale_of_fixed_means,
            TransactionTypes.sale_of_liquid_means,
            TransactionTypes.expected_sales,
        ]
        transaction_type = (
            self.translator.gettext("Debit expected sales")
            if transaction.transaction_type == TransactionTypes.expected_sales
            else self.translator.gettext("Sale")
        )
        return self.TransactionInfo(
            transaction_type=transaction_type,
            date=self.datetime_service.format_datetime(
                date=transaction.date, zone="Europe/Berlin", fmt="%d.%m.%Y %H:%M"
            ),
            transaction_volume=str(round(transaction.transaction_volume, 2)),
            purpose=transaction.purpose,
            peer_name=self._get_peer_name(transaction.peer),
            peer_type_icon=self._get_peer_type_icon(transaction.peer),
        )

    def _get_peer_type_icon(
        self,
        peer: UseCase.MemberPeer | UseCase.CompanyPeer | UseCase.SocialAccountingPeer,
    ) -> str:
        if isinstance(peer, UseCase.MemberPeer):
            return "fas fa-user"
        elif isinstance(peer, UseCase.CompanyPeer):
            return "fas fa-industry"
        else:
            return ""

    def _get_peer_name(
        self,
        peer: UseCase.MemberPeer | UseCase.CompanyPeer | UseCase.SocialAccountingPeer,
    ) -> str:
        if isinstance(peer, UseCase.MemberPeer):
            return self.translator.gettext("Anonymous worker")
        elif isinstance(peer, UseCase.CompanyPeer):
            return peer.name
        else:
            return ""

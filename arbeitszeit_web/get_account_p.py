from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from arbeitszeit.use_cases.get_account_p import GetAccountPResponse, TransactionInfo


@dataclass
class ViewModelTransactionInfo:
    transaction_type: str
    date: datetime
    transaction_volume: Decimal
    purpose: str


@dataclass
class GetAccountPResponseViewModel:
    transactions: List[ViewModelTransactionInfo]
    account_balance: Decimal


class GetAccountPPresenter:
    def present(
        self, use_case_response: GetAccountPResponse
    ) -> GetAccountPResponseViewModel:
        transactions = [
            self._create_info(transaction)
            for transaction in use_case_response.transactions
        ]
        return GetAccountPResponseViewModel(
            transactions=transactions, account_balance=use_case_response.account_balance
        )

    def _create_info(self, transaction: TransactionInfo) -> ViewModelTransactionInfo:
        return ViewModelTransactionInfo(
            transaction.type_of_transaction.value,
            transaction.date,
            round(transaction.transaction_volume, 2),
            transaction.purpose,
        )

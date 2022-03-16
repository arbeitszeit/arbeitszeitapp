from dataclasses import dataclass
from datetime import datetime
from typing import List

from arbeitszeit.transactions import TransactionTypes
from arbeitszeit.use_cases.show_prd_account_details import (
    ShowPRDAccountDetailsResponse,
    TransactionInfo,
)
from arbeitszeit_web.translator import Translator


@dataclass
class ViewModelTransactionInfo:
    transaction_type: str
    date: datetime
    transaction_volume: str
    purpose: str


@dataclass
class ShowPRDAccountDetailsResponseViewModel:
    transactions: List[ViewModelTransactionInfo]
    show_transactions: bool
    account_balance: str


@dataclass
class ShowPRDAccountDetailsPresenter:
    translator: Translator

    def present(
        self, use_case_response: ShowPRDAccountDetailsResponse
    ) -> ShowPRDAccountDetailsResponseViewModel:
        transactions = [
            self._create_info(transaction)
            for transaction in use_case_response.transactions
        ]
        return ShowPRDAccountDetailsResponseViewModel(
            transactions=transactions,
            show_transactions=bool(transactions),
            account_balance=str(round(use_case_response.account_balance, 2)),
        )

    def _create_info(self, transaction: TransactionInfo) -> ViewModelTransactionInfo:
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
        return ViewModelTransactionInfo(
            transaction_type,
            transaction.date,
            str(round(transaction.transaction_volume, 2)),
            transaction.purpose,
        )
from datetime import datetime
from decimal import Decimal
from typing import List
from unittest import TestCase

from arbeitszeit.use_cases.get_member_account import (
    GetMemberAccountResponse,
    TransactionInfo,
)
from arbeitszeit_web.presenters.get_member_account_presenter import (
    GetMemberAccountPresenter,
)
from tests.datetime_service import FakeDatetimeService

from .dependency_injection import get_dependency_injector


class TestPresenter(TestCase):
    def setUp(self) -> None:
        self.injector = get_dependency_injector()
        self.datetime_service = self.injector.get(FakeDatetimeService)
        self.presenter = self.injector.get(GetMemberAccountPresenter)

    def test_that_empty_transaction_list_is_shown_if_no_transactions_took_place(
        self,
    ):
        response = self.get_use_case_response([])
        view_model = self.presenter.present_member_account(response)
        self.assertFalse(view_model.transactions)

    def test_that_one_transaction_is_shown_if_one_transaction_took_place(
        self,
    ):
        response = self.get_use_case_response([self.get_transaction()])
        view_model = self.presenter.present_member_account(response)
        self.assertEqual(len(view_model.transactions), 1)

    def test_that_two_transactions_are_shown_if_two_transactions_took_place(
        self,
    ):
        response = self.get_use_case_response(
            [self.get_transaction(), self.get_transaction()]
        )
        view_model = self.presenter.present_member_account(response)
        self.assertEqual(len(view_model.transactions), 2)

    def test_that_correct_balance_is_returned(
        self,
    ):
        response = self.get_use_case_response([], balance=Decimal("10"))
        view_model = self.presenter.present_member_account(response)
        self.assertEqual(view_model.balance, "10.00")

    def test_that_balance_sign_is_shown_correctly_if_balance_is_negative(
        self,
    ):
        response = self.get_use_case_response([], balance=Decimal("-10"))
        view_model = self.presenter.present_member_account(response)
        self.assertFalse(view_model.is_balance_positive)

    def test_that_balance_sign_is_shown_correctly_if_balance_is_zero(
        self,
    ):
        response = self.get_use_case_response([], balance=Decimal("0"))
        view_model = self.presenter.present_member_account(response)
        self.assertTrue(view_model.is_balance_positive)

    def test_that_balance_sign_is_shown_correctly_if_balance_is_positive(
        self,
    ):
        response = self.get_use_case_response([], balance=Decimal("10"))
        view_model = self.presenter.present_member_account(response)
        self.assertTrue(view_model.is_balance_positive)

    def test_that_date_of_transaction_is_formatted_correctly(self):
        test_date = self.datetime_service.freeze_time(datetime(2022, 5, 1, 10, 30))
        response = self.get_use_case_response([self.get_transaction(date=test_date)])
        view_model = self.presenter.present_member_account(response)
        self.assertEqual(view_model.transactions[0].date, "01.05.2022 10:30")

    def test_that_transaction_volume_is_formatted_correctly(self):
        response = self.get_use_case_response([self.get_transaction()])
        view_model = self.presenter.present_member_account(response)
        self.assertEqual(view_model.transactions[0].volume, "20.01")

    def test_that_transaction_volume_sign_is_shown_correctly_if_volume_is_negative(
        self,
    ):
        response = self.get_use_case_response(
            [self.get_transaction(transaction_volume=Decimal("-1"))]
        )
        view_model = self.presenter.present_member_account(response)
        self.assertFalse(view_model.transactions[0].is_volume_positive)

    def test_that_transaction_volume_sign_is_shown_correctly_if_volume_is_zero(
        self,
    ):
        response = self.get_use_case_response(
            [self.get_transaction(transaction_volume=Decimal("0"))]
        )
        view_model = self.presenter.present_member_account(response)
        self.assertTrue(view_model.transactions[0].is_volume_positive)

    def test_that_transaction_volume_sign_is_shown_correctly_if_volume_is_positive(
        self,
    ):
        response = self.get_use_case_response(
            [self.get_transaction(transaction_volume=Decimal("2"))]
        )
        view_model = self.presenter.present_member_account(response)
        self.assertTrue(view_model.transactions[0].is_volume_positive)

    def get_use_case_response(
        self, transactions: List[TransactionInfo], balance: Decimal = None
    ) -> GetMemberAccountResponse:
        if balance is None:
            balance = Decimal("10")
        return GetMemberAccountResponse(transactions=transactions, balance=balance)

    def get_transaction(
        self, date: datetime = None, transaction_volume: Decimal = None
    ) -> TransactionInfo:
        if date is None:
            date = self.datetime_service.now()
        if transaction_volume is None:
            transaction_volume = Decimal("20.006")
        return TransactionInfo(
            date=date,
            peer_name="test company",
            transaction_volume=transaction_volume,
            purpose="test purpose",
        )

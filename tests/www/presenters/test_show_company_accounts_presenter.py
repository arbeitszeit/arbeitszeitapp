from decimal import Decimal

from arbeitszeit.use_cases.show_company_accounts import ShowCompanyAccountsResponse
from arbeitszeit_web.www.presenters.show_company_accounts_presenter import (
    ShowCompanyAccountsPresenter,
)
from tests.www.base_test_case import BaseTestCase


class ShowCompanyAccountsPresenterTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.presenter = self.injector.get(ShowCompanyAccountsPresenter)

    def test_show_correct_balance_string_for_balances(self):
        presentation = self.presenter.present(
            ShowCompanyAccountsResponse(
                balances=[Decimal(0), Decimal(-1), Decimal(2.0051), Decimal(2.5)]
            )
        )
        self.assertEqual(presentation.balance_fixed, "0.00")
        self.assertEqual(presentation.balance_liquid, "-1.00")
        self.assertEqual(presentation.balance_work, "2.01")
        self.assertEqual(presentation.balance_product, "2.50")

    def test_show_correct_signs_for_balances(self):
        presentation = self.presenter.present(
            ShowCompanyAccountsResponse(
                balances=[Decimal(0), Decimal(-1), Decimal(2.0051), Decimal(2.5)]
            )
        )
        self.assertEqual(presentation.is_fixed_positive, True)
        self.assertEqual(presentation.is_liquid_positive, False)
        self.assertEqual(presentation.is_work_positive, True)
        self.assertEqual(presentation.is_product_positive, True)

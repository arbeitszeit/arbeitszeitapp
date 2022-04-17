from unittest import TestCase

from arbeitszeit.use_cases.pay_means_of_production import PayMeansOfProductionResponse
from arbeitszeit_web.pay_means_of_production import (
    PayMeansOfProductionController,
    PayMeansOfProductionPresenter,
)
from tests.translator import FakeTranslator

from .notifier import NotifierTestImpl

reasons = PayMeansOfProductionResponse.RejectionReason


class PayMeansOfProductionTests(TestCase):
    def setUp(self) -> None:
        self.notifier = NotifierTestImpl()
        self.trans = FakeTranslator()
        self.presenter = PayMeansOfProductionPresenter(
            user_notifier=self.notifier, trans=self.trans
        )

    def test_show_confirmation_when_payment_was_successful(self) -> None:
        self.presenter.present(
            PayMeansOfProductionResponse(
                rejection_reason=None,
            )
        )
        self.assertIn(self.trans.gettext("Successfully paid."), self.notifier.infos)

    def test_missing_plan_show_correct_notification(self) -> None:
        self.presenter.present(
            PayMeansOfProductionResponse(
                rejection_reason=reasons.plan_not_found,
            )
        )
        self.assertIn(
            self.trans.gettext("Plan does not exist."), self.notifier.warnings
        )

    def test_invalid_purpose_shows_correct_notification(self) -> None:
        self.presenter.present(
            PayMeansOfProductionResponse(
                rejection_reason=reasons.invalid_purpose,
            )
        )
        self.assertIn(
            self.trans.gettext("The specified purpose is invalid."),
            self.notifier.warnings,
        )

    def test_inactive_plan_shows_correct_notification(self) -> None:
        self.presenter.present(
            PayMeansOfProductionResponse(
                rejection_reason=reasons.plan_is_not_active,
            )
        )
        self.assertIn(
            self.trans.gettext(
                "The specified plan has expired. Please contact the provider to obtain a current plan ID."
            ),
            self.notifier.warnings,
        )

    def test_trying_to_pay_public_service_shows_correct_notification(self) -> None:
        self.presenter.present(
            PayMeansOfProductionResponse(
                rejection_reason=reasons.cannot_buy_public_service,
            )
        )
        self.assertIn(
            self.trans.gettext(
                "Payment failed. Companies cannot acquire public products."
            ),
            self.notifier.warnings,
        )

    def test_trying_to_pay_for_own_product_shows_correct_notification(self) -> None:
        self.presenter.present(
            PayMeansOfProductionResponse(
                rejection_reason=reasons.buyer_is_planner,
            )
        )
        self.assertIn(
            self.trans.gettext(
                "Payment failed. Companies cannot acquire their own products."
            ),
            self.notifier.warnings,
        )

    def test_no_malformed_data_results_in_no_warning(self):
        self.presenter.present_malformed_data_warnings(
            PayMeansOfProductionController.MalformedInputData({})
        )
        self.assertFalse(self.notifier.warnings)

    def test_one_malformed_field_with_two_messages_results_in_two_warnings_with_correct_messages(
        self,
    ):
        self.presenter.present_malformed_data_warnings(
            PayMeansOfProductionController.MalformedInputData({"a": ["one", "two"]})
        )
        self.assertEqual(len(self.notifier.warnings), 2)
        self.assertIn("one", self.notifier.warnings)
        self.assertIn("two", self.notifier.warnings)

    def test_two_malformed_fields_with_one_message_each_results_in_two_warnings_with_correct_messages(
        self,
    ):
        self.presenter.present_malformed_data_warnings(
            PayMeansOfProductionController.MalformedInputData(
                {"a": ["one"], "b": ["two"]}
            )
        )
        self.assertEqual(len(self.notifier.warnings), 2)
        self.assertIn(
            "one",
            self.notifier.warnings,
        )
        self.assertIn(
            "two",
            self.notifier.warnings,
        )

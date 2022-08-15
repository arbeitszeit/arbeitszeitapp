from typing import List
from unittest import TestCase
from uuid import uuid4

from arbeitszeit.use_cases.end_cooperation import EndCooperationResponse
from arbeitszeit_web.presenters.end_cooperation_presenter import EndCooperationPresenter
from arbeitszeit_web.session import UserRole
from tests.request import FakeRequest
from tests.session import FakeSession
from tests.translator import FakeTranslator

from .dependency_injection import get_dependency_injector
from .notifier import NotifierTestImpl
from .url_index import UrlIndexTestImpl

SUCCESSFUL_RESPONSE = EndCooperationResponse(rejection_reason=None)

REJECTED_RESPONSE_PLAN_NOT_FOUND = EndCooperationResponse(
    rejection_reason=EndCooperationResponse.RejectionReason.plan_not_found,
)

REJECTED_RESPONSE_COOPERATION_NOT_FOUND = EndCooperationResponse(
    rejection_reason=EndCooperationResponse.RejectionReason.cooperation_not_found,
)


class PresenterTests(TestCase):
    def setUp(self) -> None:
        self.injector = get_dependency_injector()
        self.request = self.injector.get(FakeRequest)
        self.notifier = self.injector.get(NotifierTestImpl)
        self.url_index = self.injector.get(UrlIndexTestImpl)
        self.translator = self.injector.get(FakeTranslator)
        self.presenter = self.injector.get(EndCooperationPresenter)
        self.session = self.injector.get(FakeSession)
        self.session.login_company("test@test.test")

    def test_404_and_empty_url_returned_when_use_case_response_returned_plan_not_found(
        self,
    ):
        view_model = self.presenter.present(REJECTED_RESPONSE_PLAN_NOT_FOUND)
        self.assertTrue(view_model.show_404)
        self.assertFalse(view_model.redirect_url)

    def test_notification_returned_when_operation_was_rejected_because_plan_was_not_found(
        self,
    ):
        self.presenter.present(REJECTED_RESPONSE_PLAN_NOT_FOUND)
        self.assertTrue(self._get_warning_notifications())

    def test_correct_notification_is_returned_when_operation_was_rejected_because_plan_was_not_found(
        self,
    ):
        self.presenter.present(REJECTED_RESPONSE_PLAN_NOT_FOUND)
        self.assertIn(
            self.translator.gettext("Cooperation could not be terminated."),
            self._get_warning_notifications(),
        )

    def test_url_gets_returned_when_use_case_response_is_successfull(
        self,
    ):
        self.request.set_arg("plan_id", str(uuid4()))
        self.request.set_arg("cooperation_id", str(uuid4()))
        view_model = self.presenter.present(SUCCESSFUL_RESPONSE)
        self.assertFalse(view_model.show_404)
        self.assertTrue(view_model.redirect_url)

    def test_coop_summary_url_gets_returned_as_default_when_no_referer_is_given(
        self,
    ):
        coop_id = uuid4()
        self.request.set_arg("plan_id", str(uuid4()))
        self.request.set_arg("cooperation_id", str(coop_id))
        view_model = self.presenter.present(SUCCESSFUL_RESPONSE)
        self.assertFalse(view_model.show_404)
        self.assertEqual(
            view_model.redirect_url,
            self.url_index.get_coop_summary_url(
                coop_id=coop_id, user_role=UserRole.company
            ),
        )

    def test_plan_summary_url_gets_returned_when_plan_summary_url_was_referer(
        self,
    ):
        plan_id = uuid4()
        self.request.set_header("Referer", f"/company/plan_summary/{str(plan_id)}")
        self.request.set_arg("plan_id", str(plan_id))
        self.request.set_arg("cooperation_id", str(uuid4()))
        view_model = self.presenter.present(SUCCESSFUL_RESPONSE)
        self.assertFalse(view_model.show_404)
        self.assertEqual(
            view_model.redirect_url,
            self.url_index.get_company_plan_summary_url(plan_id=plan_id),
        )

    def test_correct_notification_is_returned_when_operation_was_successfull(
        self,
    ):
        self.request.set_arg("plan_id", str(uuid4()))
        self.request.set_arg("cooperation_id", str(uuid4()))
        self.presenter.present(SUCCESSFUL_RESPONSE)
        self.assertIn(
            self.translator.gettext("Cooperation has been terminated."),
            self._get_info_notifications(),
        )

    def _get_info_notifications(self) -> List[str]:
        return self.notifier.infos

    def _get_warning_notifications(self) -> List[str]:
        return self.notifier.warnings

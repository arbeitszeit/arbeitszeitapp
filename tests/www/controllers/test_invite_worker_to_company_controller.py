from dataclasses import dataclass
from uuid import uuid4

from arbeitszeit_web.www.controllers.invite_worker_to_company_controller import (
    InviteWorkerToCompanyController,
)
from tests.www.base_test_case import BaseTestCase


class InviteWorkerToCompanyControllerTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.controller = self.injector.get(InviteWorkerToCompanyController)
        self.company_id = uuid4()
        self.session.login_company(company=self.company_id)

    def test_current_user_is_company_in_use_case_request(self) -> None:
        use_case_request = self.controller.import_request_data(
            form=Form(worker_id=str(uuid4())),
        )
        self.assertEqual(use_case_request.company, self.company_id)

    def test_raise_value_error_if_worker_id_is_empty_string(self) -> None:
        with self.assertRaisesRegex(ValueError, "worker_id"):
            self.controller.import_request_data(
                form=Form(worker_id=""),
            )

    def test_raise_value_error_if_worker_id_is_not_a_uuid(self) -> None:
        with self.assertRaises(ValueError):
            self.controller.import_request_data(
                form=Form(worker_id="1"),
            )

    def test_use_case_request_contains_specified_worker_id(self) -> None:
        expected_worker_id = uuid4()
        use_case_request = self.controller.import_request_data(
            form=Form(worker_id=str(expected_worker_id)),
        )
        self.assertEqual(use_case_request.worker, expected_worker_id)


class AnonymousUserTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.controller = self.injector.get(InviteWorkerToCompanyController)
        self.session.logout()

    def test_raise_value_error_if_user_is_not_logged_in(self) -> None:
        with self.assertRaisesRegex(ValueError, r"User is not logged in"):
            self.controller.import_request_data(
                form=Form(worker_id=str(uuid4())),
            )


@dataclass
class Form:
    worker_id: str

    def get_worker_id(self) -> str:
        return self.worker_id

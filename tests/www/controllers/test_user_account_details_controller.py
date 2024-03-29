from uuid import uuid4

import pytest

from arbeitszeit_web.www.controllers import (
    user_account_details_controller as controller,
)
from tests.www.base_test_case import BaseTestCase


class UserAccountDetailsControllerTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.controller = self.injector.get(controller.UserAccountDetailsController)

    def test_that_controller_raises_if_user_is_not_logged_in(self) -> None:
        self.session.logout()
        with pytest.raises(Exception):
            self.controller.parse_web_request()

    def test_that_controller_does_not_raise_if_user_is_logged_in_as_member(
        self,
    ) -> None:
        self.session.login_member(uuid4())
        self.controller.parse_web_request()

    def test_that_controller_does_not_raise_if_user_is_logged_in_as_company(
        self,
    ) -> None:
        self.session.login_company(uuid4())
        self.controller.parse_web_request()

    def test_that_controller_does_not_raise_if_user_is_logged_in_as_accountant(
        self,
    ) -> None:
        self.session.login_accountant(uuid4())
        self.controller.parse_web_request()

    def test_that_request_generated_by_controller_contains_current_user_id(
        self,
    ) -> None:
        user_id = uuid4()
        self.session.login_member(user_id)
        request = self.controller.parse_web_request()
        assert request.user_id

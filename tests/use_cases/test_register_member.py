from unittest import TestCase

from arbeitszeit.entities import AccountTypes
from arbeitszeit.use_cases import (
    RegisterMember,
    RegisterMemberRequest,
    RegisterMemberResponse,
)
from tests.data_generators import MemberGenerator
from tests.token import TokenDeliveryService

from .dependency_injection import get_dependency_injector
from .repositories import AccountRepository, MemberRepository

DEFAULT = dict(
    email="test@cp.org",
    name="test name",
    password="super safe",
)


class RegisterMemberTests(TestCase):
    def setUp(self) -> None:
        self.injector = get_dependency_injector()
        self.use_case = self.injector.get(RegisterMember)
        self.account_repository = self.injector.get(AccountRepository)
        self.member_repo = self.injector.get(MemberRepository)
        self.member_generator = self.injector.get(MemberGenerator)
        self.token_delivery = self.injector.get(TokenDeliveryService)

    def test_that_a_token_is_sent_out_when_a_member_registers(self) -> None:
        self.use_case(RegisterMemberRequest(**DEFAULT))
        self.assertTrue(self.token_delivery.delivered_tokens)

    def test_that_token_was_delivered_to_registering_email(self) -> None:
        expected_mail = "mailtest321@cp.org"
        request_args = DEFAULT.copy()
        request_args.pop("email")
        self.use_case(RegisterMemberRequest(email=expected_mail, **request_args))
        self.assertEqual(
            self.token_delivery.delivered_tokens[0].email,
            expected_mail,
        )

    def test_that_registering_member_is_possible(self) -> None:
        request = RegisterMemberRequest(**DEFAULT)
        response = self.use_case(request)
        self.assertFalse(response.is_rejected)

    def test_that_registering_a_member_does_create_a_member_account(self) -> None:
        self.use_case(RegisterMemberRequest(**DEFAULT))
        self.assertEqual(len(self.account_repository.accounts), 1)
        self.assertEqual(
            self.account_repository.accounts[0].account_type, AccountTypes.member
        )

    def test_that_correct_member_attributes_are_registered(self) -> None:
        request = RegisterMemberRequest(**DEFAULT)
        self.use_case(request)
        assert len(self.member_repo.members) == 1
        for member in self.member_repo.members.values():
            self.assertEqual(member.email, request.email)
            self.assertEqual(member.name, request.name)
            self.assertIsNotNone(member.registered_on)
            self.assertIsNone(member.confirmed_on)

    def test_that_correct_error_is_raised_when_user_with_mail_exists(self) -> None:
        self.member_generator.create_member(email="test@cp.org")
        request = RegisterMemberRequest(**DEFAULT)
        response = self.use_case(request)
        self.assertTrue(response.is_rejected)
        self.assertEqual(
            response.rejection_reason,
            RegisterMemberResponse.RejectionReason.member_already_exists,
        )

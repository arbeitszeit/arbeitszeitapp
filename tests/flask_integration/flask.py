from typing import List, Optional
from unittest import TestCase

from flask import Flask
from injector import Module

from arbeitszeit.entities import Company, Member
from arbeitszeit.repositories import CompanyRepository, MemberRepository
from arbeitszeit_flask.token import FlaskTokenService
from tests.data_generators import CompanyGenerator, EmailGenerator, MemberGenerator

from .dependency_injection import get_dependency_injector


class FlaskTestCase(TestCase):
    def setUp(self) -> None:
        self.injector = get_dependency_injector(self.get_injection_modules())
        self.app = self.injector.get(Flask)

    def get_injection_modules(self) -> List[Module]:
        return []


class ViewTestCase(FlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = self.app.test_client()
        self.member_generator = self.injector.get(MemberGenerator)
        self.company_generator = self.injector.get(CompanyGenerator)
        self.email_generator = self.injector.get(EmailGenerator)
        self.member_repository = self.injector.get(MemberRepository)
        self.company_repository = self.injector.get(CompanyRepository)

    def login_member(
        self,
        member: Optional[Member] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        confirm_member: bool = True,
    ) -> Member:
        if password is None:
            password = "password123"
        if email is None:
            email = self.email_generator.get_random_email()
        if member is None:
            member = self.member_generator.create_member_entity(
                password=password, email=email
            )
        response = self.client.post(
            "/member/login",
            data=dict(
                email=email,
                password=password,
            ),
            follow_redirects=True,
        )
        assert response.status_code < 400
        if confirm_member:
            self._confirm_member(email)
        updated_member = self.member_repository.get_by_email(email)
        assert updated_member
        return updated_member

    def _confirm_member(
        self,
        email: str,
    ) -> None:
        token = FlaskTokenService().generate_token(email)
        response = self.client.get(
            f"/member/confirm/{token}",
            follow_redirects=True,
        )
        assert response.status_code < 400

    def login_company(
        self,
        company: Optional[Company] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        confirm_company: bool = True,
    ) -> Company:
        if password is None:
            password = "password123"
        if email is None:
            email = self.email_generator.get_random_email()
        if company is None:
            company = self.company_generator.create_company(
                password=password, email=email
            )
        response = self.client.post(
            "/company/login",
            data=dict(
                email=email,
                password=password,
            ),
            follow_redirects=True,
        )
        assert response.status_code < 400
        if confirm_company:
            self._confirm_company(email)
        updated_company = self.company_repository.get_by_email(email)
        assert updated_company
        return updated_company

    def _confirm_company(
        self,
        email: str,
    ) -> None:
        token = FlaskTokenService().generate_token(email)
        response = self.client.get(
            f"/company/confirm/{token}",
            follow_redirects=True,
        )
        assert response.status_code < 400

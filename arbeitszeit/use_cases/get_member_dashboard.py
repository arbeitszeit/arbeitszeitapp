from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from arbeitszeit.datetime_service import DatetimeService
from arbeitszeit.records import CompanyWorkInvite
from arbeitszeit.repositories import DatabaseGateway


@dataclass
class GetMemberDashboard:
    @dataclass
    class Workplace:
        workplace_name: str
        workplace_email: str

    @dataclass
    class WorkInvitation:
        invite_id: UUID
        company_id: UUID
        company_name: str

    @dataclass
    class PlanDetails:
        plan_id: UUID
        prd_name: str
        activation_date: datetime

    @dataclass
    class Response:
        workplaces: List[GetMemberDashboard.Workplace]
        invites: List[GetMemberDashboard.WorkInvitation]
        three_latest_plans: List[GetMemberDashboard.PlanDetails]
        account_balance: Decimal
        name: str
        email: str
        id: UUID

    database_gateway: DatabaseGateway
    datetime_service: DatetimeService

    def __call__(self, member: UUID) -> Response:
        record = (
            self.database_gateway.get_members()
            .with_id(member)
            .joined_with_email_address()
            .first()
        )
        assert record
        _member, email = record
        workplaces = [
            self.Workplace(
                workplace_name=workplace.name,
                workplace_email=email.address,
            )
            for workplace, email in self.database_gateway.get_companies()
            .that_are_workplace_of_member(member)
            .joined_with_email_address()
        ]
        invites = [
            self._render_company_work_invite(invite)
            for invite in self.database_gateway.get_company_work_invites().addressing(
                member
            )
        ]
        return self.Response(
            workplaces=workplaces,
            invites=invites,
            three_latest_plans=self._get_three_latest_plans(),
            account_balance=self._get_account_balance(member),
            name=_member.name,
            email=email.address,
            id=_member.id,
        )

    def _get_account_balance(self, member: UUID) -> Decimal:
        result = (
            self.database_gateway.get_accounts()
            .owned_by_member(member)
            .joined_with_balance()
            .first()
        )
        assert result
        return result[1]

    def _render_company_work_invite(self, invite: CompanyWorkInvite) -> WorkInvitation:
        company = self.database_gateway.get_companies().with_id(invite.company).first()
        assert company
        return self.WorkInvitation(
            invite_id=invite.id,
            company_id=invite.company,
            company_name=company.name,
        )

    def _get_three_latest_plans(self) -> List[PlanDetails]:
        now = self.datetime_service.now()
        latest_plans = (
            self.database_gateway.get_plans()
            .that_will_expire_after(now)
            .that_were_activated_before(now)
            .ordered_by_creation_date(ascending=False)
            .limit(3)
        )
        plans = []
        for plan in latest_plans:
            assert plan.activation_date
            plans.append(self.PlanDetails(plan.id, plan.prd_name, plan.activation_date))
        return plans

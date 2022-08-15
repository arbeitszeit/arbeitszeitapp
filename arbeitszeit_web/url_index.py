"""This module contains interfaces for getting urls. Please note that
there is legacy code in this module. In the past we used to implement
individual interfaces for different "kinds" of urls. This is now
deprecated and unwanted. If you want to add a new url to the index,
simply add an appropriate method the the UrlIndex interface. If you
need different urls for different roles include the role name in the
method name, for example "get_member_dashboard_url" and
"get_company_dashboard_url".
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Protocol
from uuid import UUID

from injector import inject

from arbeitszeit_web.session import Session, UserRole


class DraftUrlIndex(Protocol):
    def get_draft_summary_url(self, draft_id: UUID) -> str:
        ...


class CompanyUrlIndex(Protocol):
    def get_company_dashboard_url(self) -> str:
        ...


class AnswerCompanyWorkInviteUrlIndex(Protocol):
    def get_answer_company_work_invite_url(self, invite_id: UUID) -> str:
        ...


class UrlIndex(Protocol):
    def get_member_dashboard_url(self) -> str:
        ...

    def get_company_plan_summary_url(self, plan_id: UUID) -> str:
        ...

    def get_member_plan_summary_url(self, plan_id: UUID) -> str:
        ...

    def get_work_invite_url(self, invite_id: UUID) -> str:
        ...

    def get_company_summary_url(
        self, user_role: Optional[UserRole], company_id: UUID
    ) -> str:
        ...

    def get_coop_summary_url(self, user_role: Optional[UserRole], coop_id: UUID) -> str:
        ...


class TogglePlanAvailabilityUrlIndex(Protocol):
    def get_toggle_availability_url(self, plan_id: UUID) -> str:
        ...


class RenewPlanUrlIndex(Protocol):
    def get_renew_plan_url(self, plan_id: UUID) -> str:
        ...


class HidePlanUrlIndex(Protocol):
    def get_hide_plan_url(self, plan_id: UUID) -> str:
        ...


class RequestCoopUrlIndex(Protocol):
    def get_request_coop_url(self) -> str:
        ...


class EndCoopUrlIndex(Protocol):
    def get_end_coop_url(self, plan_id: UUID, cooperation_id: UUID) -> str:
        ...


class ConfirmationUrlIndex(Protocol):
    def get_confirmation_url(self, token: str) -> str:
        ...


class AccountantInvitationUrlIndex(Protocol):
    def get_accountant_invitation_url(self, token: str) -> str:
        ...


class PayMeansOfProductionUrlIndex(Protocol):
    def get_pay_means_of_production_url(self) -> str:
        ...


class PlotsUrlIndex(Protocol):
    def get_global_barplot_for_certificates_url(
        self, certificates_count: Decimal, available_product: Decimal
    ) -> str:
        ...

    def get_global_barplot_for_means_of_production_url(
        self, planned_means: Decimal, planned_resources: Decimal, planned_work: Decimal
    ) -> str:
        ...

    def get_global_barplot_for_plans_url(
        self, productive_plans: int, public_plans: int
    ) -> str:
        ...

    def get_line_plot_of_company_prd_account(self, company_id: UUID) -> str:
        ...

    def get_line_plot_of_company_r_account(self, company_id: UUID) -> str:
        ...

    def get_line_plot_of_company_p_account(self, company_id: UUID) -> str:
        ...

    def get_line_plot_of_company_a_account(self, company_id: UUID) -> str:
        ...


class AccountantDashboardUrlIndex(Protocol):
    def get_accountant_dashboard_url(self) -> str:
        ...


class LanguageChangerUrlIndex(Protocol):
    def get_language_change_url(self, language_code: str) -> str:
        ...


@inject
@dataclass
class UserUrlIndex:
    """This class is not an interface and therefore should not be
    implemented by the web framework. It is merely used internally as
    a convinience interface. You should refrain from using this class
    in your tests and instead rely on the UrlIndex interface. In a
    test scenario you most likely know in advance if you expect a url
    intended for a member, company or any other role. This is why the
    UrlIndex interface is much better suited for testing needs.
    """

    session: Session
    plan_url_index: UrlIndex

    def get_plan_summary_url(self, plan_id: UUID) -> str:
        user_role = self.session.get_user_role()
        if user_role == UserRole.member:
            return self.plan_url_index.get_member_plan_summary_url(plan_id)
        if user_role == UserRole.company:
            return self.plan_url_index.get_company_plan_summary_url(plan_id)
        raise Exception(f"Cannot get plan summary url for role {user_role}")

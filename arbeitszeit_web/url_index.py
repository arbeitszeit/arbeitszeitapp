from decimal import Decimal
from typing import Protocol
from uuid import UUID


class AnswerCompanyWorkInviteUrlIndex(Protocol):
    def get_answer_company_work_invite_url(self, invite_id: UUID) -> str:
        ...


class WorkInviteMessageUrlIndex(Protocol):
    def get_work_invite_message_url(self, message_id: UUID) -> str:
        ...


class PlanSummaryUrlIndex(Protocol):
    def get_plan_summary_url(self, plan_id: UUID) -> str:
        ...


class CoopSummaryUrlIndex(Protocol):
    def get_coop_summary_url(self, coop_id: UUID) -> str:
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


class CompanySummaryUrlIndex(Protocol):
    def get_company_summary_url(self, company_id: UUID) -> str:
        ...


class ListMessagesUrlIndex(Protocol):
    def get_list_messages_url(self) -> str:
        ...


class ConfirmationUrlIndex(Protocol):
    def get_confirmation_url(self, token: str) -> str:
        ...


class AccountantInvitationUrlIndex(Protocol):
    def get_accountant_invitation_url(self, token: str) -> str:
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

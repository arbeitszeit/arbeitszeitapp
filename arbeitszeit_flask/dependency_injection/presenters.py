from injector import Module, provider

from arbeitszeit.datetime_service import DatetimeService
from arbeitszeit.use_cases.register_company.company_registration_message_presenter import (
    CompanyRegistrationMessagePresenter,
)
from arbeitszeit.use_cases.register_member.member_registration_message_presenter import (
    MemberRegistrationMessagePresenter,
)
from arbeitszeit.use_cases.send_accountant_registration_token.accountant_invitation_presenter import (
    AccountantInvitationPresenter,
)
from arbeitszeit_flask.url_index import CompanyUrlIndex, GeneralUrlIndex
from arbeitszeit_web.colors import Colors
from arbeitszeit_web.email import EmailConfiguration, MailService, UserAddressBook
from arbeitszeit_web.formatters.plan_summary_formatter import PlanSummaryFormatter
from arbeitszeit_web.get_company_transactions import GetCompanyTransactionsPresenter
from arbeitszeit_web.get_plan_summary_company import (
    GetPlanSummaryCompanySuccessPresenter,
)
from arbeitszeit_web.get_plan_summary_member import GetPlanSummarySuccessPresenter
from arbeitszeit_web.get_statistics import GetStatisticsPresenter
from arbeitszeit_web.invite_worker_to_company import InviteWorkerToCompanyPresenter
from arbeitszeit_web.language_service import LanguageService
from arbeitszeit_web.list_drafts_of_company import ListDraftsPresenter
from arbeitszeit_web.notification import Notifier
from arbeitszeit_web.pay_means_of_production import PayMeansOfProductionPresenter
from arbeitszeit_web.plotter import Plotter
from arbeitszeit_web.presenters.accountant_invitation_presenter import (
    AccountantInvitationEmailPresenter,
    AccountantInvitationEmailView,
)
from arbeitszeit_web.presenters.list_available_languages_presenter import (
    ListAvailableLanguagesPresenter,
)
from arbeitszeit_web.presenters.log_in_company_presenter import LogInCompanyPresenter
from arbeitszeit_web.presenters.member_purchases import MemberPurchasesPresenter
from arbeitszeit_web.presenters.register_accountant_presenter import (
    RegisterAccountantPresenter,
)
from arbeitszeit_web.presenters.register_company_presenter import (
    RegisterCompanyPresenter,
)
from arbeitszeit_web.presenters.register_member_presenter import RegisterMemberPresenter
from arbeitszeit_web.presenters.registration_email_presenter import (
    RegistrationEmailPresenter,
    RegistrationEmailTemplate,
)
from arbeitszeit_web.presenters.self_approve_plan import SelfApprovePlanPresenter
from arbeitszeit_web.presenters.send_confirmation_email_presenter import (
    SendConfirmationEmailPresenter,
)
from arbeitszeit_web.presenters.send_work_certificates_to_worker_presenter import (
    SendWorkCertificatesToWorkerPresenter,
)
from arbeitszeit_web.presenters.show_a_account_details_presenter import (
    ShowAAccountDetailsPresenter,
)
from arbeitszeit_web.presenters.show_company_work_invite_details_presenter import (
    ShowCompanyWorkInviteDetailsPresenter,
)
from arbeitszeit_web.presenters.show_p_account_details_presenter import (
    ShowPAccountDetailsPresenter,
)
from arbeitszeit_web.presenters.show_prd_account_details_presenter import (
    ShowPRDAccountDetailsPresenter,
)
from arbeitszeit_web.presenters.show_r_account_details_presenter import (
    ShowRAccountDetailsPresenter,
)
from arbeitszeit_web.request_cooperation import RequestCooperationPresenter
from arbeitszeit_web.session import Session
from arbeitszeit_web.translator import Translator
from arbeitszeit_web.url_index import (
    AnswerCompanyWorkInviteUrlIndex,
    ConfirmationUrlIndex,
    EndCoopUrlIndex,
    PlotsUrlIndex,
    RequestCoopUrlIndex,
    TogglePlanAvailabilityUrlIndex,
)


class CompanyPresenterModule(Module):
    @provider
    def provide_pay_means_of_production_presenter(
        self, notifier: Notifier, trans: Translator, company_url_index: CompanyUrlIndex
    ) -> PayMeansOfProductionPresenter:
        return PayMeansOfProductionPresenter(
            notifier, trans, pay_means_of_production_url_index=company_url_index
        )

    @provider
    def provide_request_cooperation_presenter(
        self,
        translator: Translator,
        mail_service: MailService,
        email_configuration: EmailConfiguration,
    ) -> RequestCooperationPresenter:
        return RequestCooperationPresenter(
            translator, mail_service, email_configuration
        )

    @provider
    def provide_send_work_certificates_to_worker_presenter(
        self, notifier: Notifier, translator: Translator
    ) -> SendWorkCertificatesToWorkerPresenter:
        return SendWorkCertificatesToWorkerPresenter(notifier, translator)

    @provider
    def provide_show_prd_account_details_presenter(
        self,
        translator: Translator,
        url_index: PlotsUrlIndex,
        datetime_service: DatetimeService,
    ) -> ShowPRDAccountDetailsPresenter:
        return ShowPRDAccountDetailsPresenter(
            translator=translator,
            url_index=url_index,
            datetime_service=datetime_service,
        )

    @provider
    def provide_show_r_account_details_presenter(
        self,
        translator: Translator,
        url_index: PlotsUrlIndex,
        datetime_service: DatetimeService,
    ) -> ShowRAccountDetailsPresenter:
        return ShowRAccountDetailsPresenter(
            trans=translator, url_index=url_index, datetime_service=datetime_service
        )

    @provider
    def provide_show_a_account_details_presenter(
        self,
        translator: Translator,
        url_index: PlotsUrlIndex,
        datetime_service: DatetimeService,
    ) -> ShowAAccountDetailsPresenter:
        return ShowAAccountDetailsPresenter(
            trans=translator, url_index=url_index, datetime_service=datetime_service
        )

    @provider
    def provide_show_p_account_details_presenter(
        self,
        translator: Translator,
        url_index: PlotsUrlIndex,
        datetime_service: DatetimeService,
    ) -> ShowPAccountDetailsPresenter:
        return ShowPAccountDetailsPresenter(
            trans=translator, url_index=url_index, datetime_service=datetime_service
        )

    @provider
    def provide_get_company_transactions_presenter(
        self, translator: Translator, datetime_service: DatetimeService
    ) -> GetCompanyTransactionsPresenter:
        return GetCompanyTransactionsPresenter(
            translator=translator, datetime_service=datetime_service
        )


class PresenterModule(Module):
    @provider
    def provide_log_in_company_presenter(
        self,
        translator: Translator,
        session: Session,
        company_url_index: GeneralUrlIndex,
    ) -> LogInCompanyPresenter:
        return LogInCompanyPresenter(
            translator=translator,
            session=session,
            company_url_index=company_url_index,
        )

    @provider
    def provide_self_approve_plan_presenter(
        self, notifier: Notifier, translator: Translator
    ) -> SelfApprovePlanPresenter:
        return SelfApprovePlanPresenter(
            notifier=notifier,
            translator=translator,
        )

    @provider
    def provide_register_accountant_presenter(
        self,
        notifier: Notifier,
        session: Session,
        translator: Translator,
        dashboard_url_index: GeneralUrlIndex,
    ) -> RegisterAccountantPresenter:
        return RegisterAccountantPresenter(
            notifier=notifier,
            session=session,
            translator=translator,
            dashboard_url_index=dashboard_url_index,
        )

    @provider
    def provide_accountant_invitation_presenter(
        self,
        view: AccountantInvitationEmailView,
        email_configuration: EmailConfiguration,
        translator: Translator,
        invitation_url_index: GeneralUrlIndex,
    ) -> AccountantInvitationPresenter:
        return AccountantInvitationEmailPresenter(
            invitation_view=view,
            email_configuration=email_configuration,
            translator=translator,
            invitation_url_index=invitation_url_index,
        )

    @provider
    def provide_register_member_presenter(
        self, session: Session, translator: Translator
    ) -> RegisterMemberPresenter:
        return RegisterMemberPresenter(session=session, translator=translator)

    @provider
    def provide_register_company_presenter(
        self, session: Session, translator: Translator
    ) -> RegisterCompanyPresenter:
        return RegisterCompanyPresenter(session=session, translator=translator)

    @provider
    def provide_registration_email_presenter(
        self,
        email_sender: MailService,
        address_book: UserAddressBook,
        email_template: RegistrationEmailTemplate,
        url_index: ConfirmationUrlIndex,
        email_configuration: EmailConfiguration,
        translator: Translator,
    ) -> RegistrationEmailPresenter:
        return RegistrationEmailPresenter(
            email_sender=email_sender,
            address_book=address_book,
            member_email_template=email_template,
            company_email_template=email_template,
            url_index=url_index,
            email_configuration=email_configuration,
            translator=translator,
        )

    @provider
    def provide_member_registration_message_presenter(
        self, presenter: RegistrationEmailPresenter
    ) -> MemberRegistrationMessagePresenter:
        return presenter

    @provider
    def provide_company_registration_message_presenter(
        self, presenter: RegistrationEmailPresenter
    ) -> CompanyRegistrationMessagePresenter:
        return presenter

    @provider
    def provide_get_statistics_presenter(
        self,
        translator: Translator,
        plotter: Plotter,
        colors: Colors,
        url_index: PlotsUrlIndex,
    ) -> GetStatisticsPresenter:
        return GetStatisticsPresenter(
            translator=translator, plotter=plotter, colors=colors, url_index=url_index
        )

    @provider
    def provide_list_available_languages_presenter(
        self,
        language_changer_url_index: GeneralUrlIndex,
        language_service: LanguageService,
    ) -> ListAvailableLanguagesPresenter:
        return ListAvailableLanguagesPresenter(
            language_changer_url_index=language_changer_url_index,
            language_service=language_service,
        )

    @provider
    def provide_show_company_work_invite_details_presenter(
        self, url_index: AnswerCompanyWorkInviteUrlIndex, translator: Translator
    ) -> ShowCompanyWorkInviteDetailsPresenter:
        return ShowCompanyWorkInviteDetailsPresenter(url_index, translator)

    @provider
    def provide_send_confirmation_email_presenter(
        self,
        url_index: ConfirmationUrlIndex,
        email_configuration: EmailConfiguration,
        translator: Translator,
    ) -> SendConfirmationEmailPresenter:
        return SendConfirmationEmailPresenter(
            url_index=url_index,
            email_configuration=email_configuration,
            translator=translator,
        )

    @provider
    def provide_get_plan_summary_success_presenter(
        self,
        trans: Translator,
        plan_summary_service: PlanSummaryFormatter,
    ) -> GetPlanSummarySuccessPresenter:
        return GetPlanSummarySuccessPresenter(trans, plan_summary_service)

    @provider
    def provide_get_plan_summary_company_success_presenter(
        self,
        toggle_availability_index: TogglePlanAvailabilityUrlIndex,
        end_coop_url_index: EndCoopUrlIndex,
        request_coop_url_index: RequestCoopUrlIndex,
        trans: Translator,
        plan_summary_service: PlanSummaryFormatter,
    ) -> GetPlanSummaryCompanySuccessPresenter:
        return GetPlanSummaryCompanySuccessPresenter(
            toggle_availability_index,
            end_coop_url_index,
            request_coop_url_index,
            trans,
            plan_summary_service,
        )

    @provider
    def provide_invite_worker_to_company_presenter(
        self, translator: Translator
    ) -> InviteWorkerToCompanyPresenter:
        return InviteWorkerToCompanyPresenter(translator)

    @provider
    def provide_member_purchases_presenter(
        self,
        datetime_service: DatetimeService,
    ) -> MemberPurchasesPresenter:
        return MemberPurchasesPresenter(datetime_service=datetime_service)

    @provider
    def provide_list_drafts_presenter(
        self, draft_url_index: GeneralUrlIndex
    ) -> ListDraftsPresenter:
        return ListDraftsPresenter(
            draft_url_index=draft_url_index,
        )

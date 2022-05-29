from injector import Module, provider

from arbeitszeit.use_cases import (
    AnswerCompanyWorkInvite,
    InviteWorkerToCompanyUseCase,
    ReadWorkerInviteMessage,
    ShowCompanyWorkInviteDetailsUseCase,
)
from arbeitszeit.use_cases.create_cooperation import CreateCooperation
from arbeitszeit.use_cases.get_latest_activated_plans import GetLatestActivatedPlans
from arbeitszeit.use_cases.list_workers import ListWorkers
from arbeitszeit.use_cases.register_accountant import RegisterAccountantUseCase
from arbeitszeit.use_cases.register_company import RegisterCompany
from arbeitszeit.use_cases.register_member import RegisterMemberUseCase
from arbeitszeit.use_cases.show_my_accounts import ShowMyAccounts
from arbeitszeit_flask.database.repositories import MemberRepository
from arbeitszeit_flask.flask_session import FlaskSession
from arbeitszeit_flask.template import (
    TemplateIndex,
    TemplateRenderer,
    UserTemplateRenderer,
)
from arbeitszeit_flask.views import (
    CompanyWorkInviteView,
    Http404View,
    InviteWorkerToCompanyView,
    ReadWorkerInviteMessageView,
)
from arbeitszeit_flask.views.accountant_invitation_email_view import (
    AccountantInvitationEmailViewImpl,
)
from arbeitszeit_flask.views.create_cooperation_view import CreateCooperationView
from arbeitszeit_flask.views.dashboard_view import DashboardView
from arbeitszeit_flask.views.invite_worker_to_company import (
    InviteWorkerGetRequestHandler,
    InviteWorkerPostRequestHandler,
)
from arbeitszeit_flask.views.show_my_accounts_view import ShowMyAccountsView
from arbeitszeit_flask.views.signup_accountant_view import SignupAccountantView
from arbeitszeit_flask.views.signup_company_view import SignupCompanyView
from arbeitszeit_flask.views.signup_member_view import SignupMemberView
from arbeitszeit_web.answer_company_work_invite import (
    AnswerCompanyWorkInviteController,
    AnswerCompanyWorkInvitePresenter,
)
from arbeitszeit_web.controllers.list_workers_controller import ListWorkersController
from arbeitszeit_web.controllers.register_accountant_controller import (
    RegisterAccountantController,
)
from arbeitszeit_web.controllers.show_company_work_invite_details_controller import (
    ShowCompanyWorkInviteDetailsController,
)
from arbeitszeit_web.controllers.show_my_accounts_controller import (
    ShowMyAccountsController,
)
from arbeitszeit_web.create_cooperation import CreateCooperationPresenter
from arbeitszeit_web.email import MailService
from arbeitszeit_web.invite_worker_to_company import (
    InviteWorkerToCompanyController,
    InviteWorkerToCompanyPresenter,
)
from arbeitszeit_web.presenters.accountant_invitation_presenter import (
    AccountantInvitationEmailView,
)
from arbeitszeit_web.presenters.get_latest_activated_plans_presenter import (
    GetLatestActivatedPlansPresenter,
)
from arbeitszeit_web.presenters.list_workers_presenter import ListWorkersPresenter
from arbeitszeit_web.presenters.register_accountant_presenter import (
    RegisterAccountantPresenter,
)
from arbeitszeit_web.presenters.register_company_presenter import (
    RegisterCompanyPresenter,
)
from arbeitszeit_web.presenters.register_member_presenter import RegisterMemberPresenter
from arbeitszeit_web.presenters.show_company_work_invite_details_presenter import (
    ShowCompanyWorkInviteDetailsPresenter,
)
from arbeitszeit_web.presenters.show_my_accounts_presenter import (
    ShowMyAccountsPresenter,
)
from arbeitszeit_web.read_worker_invite_message import (
    ReadWorkerInviteMessageController,
    ReadWorkerInviteMessagePresenter,
)
from arbeitszeit_web.register_company import RegisterCompanyController
from arbeitszeit_web.register_member import RegisterMemberController


class ViewsModule(Module):
    @provider
    def provide_show_company_work_invite_details_view(
        self,
        details_use_case: ShowCompanyWorkInviteDetailsUseCase,
        details_presenter: ShowCompanyWorkInviteDetailsPresenter,
        details_controller: ShowCompanyWorkInviteDetailsController,
        answer_use_case: AnswerCompanyWorkInvite,
        answer_presenter: AnswerCompanyWorkInvitePresenter,
        answer_controller: AnswerCompanyWorkInviteController,
        http_404_view: Http404View,
        template_index: TemplateIndex,
        template_renderer: TemplateRenderer,
    ) -> CompanyWorkInviteView:
        return CompanyWorkInviteView(
            details_use_case=details_use_case,
            details_presenter=details_presenter,
            details_controller=details_controller,
            http_404_view=http_404_view,
            answer_use_case=answer_use_case,
            answer_presenter=answer_presenter,
            answer_controller=answer_controller,
            template_index=template_index,
            template_renderer=template_renderer,
        )

    @provider
    def provide_read_worker_invite_message_view(
        self,
        read_message: ReadWorkerInviteMessage,
        controller: ReadWorkerInviteMessageController,
        presenter: ReadWorkerInviteMessagePresenter,
        template_renderer: TemplateRenderer,
        http_404_view: Http404View,
    ) -> ReadWorkerInviteMessageView:
        return ReadWorkerInviteMessageView(
            read_message,
            controller,
            presenter,
            template_renderer,
            http_404_view,
        )

    @provider
    def provide_http_404_view(
        self, template_renderer: TemplateRenderer, template_index: TemplateIndex
    ) -> Http404View:
        return Http404View(
            template_index=template_index, template_renderer=template_renderer
        )

    @provider
    def provide_invite_worker_to_company_view(
        self,
        post_request_handler: InviteWorkerPostRequestHandler,
        get_request_handler: InviteWorkerGetRequestHandler,
    ) -> InviteWorkerToCompanyView:
        return InviteWorkerToCompanyView(
            post_request_handler=post_request_handler,
            get_request_handler=get_request_handler,
        )

    @provider
    def provide_invite_worker_post_request_handler(
        self,
        use_case: InviteWorkerToCompanyUseCase,
        presenter: InviteWorkerToCompanyPresenter,
        controller: InviteWorkerToCompanyController,
        template_renderer: TemplateRenderer,
        template_index: TemplateIndex,
    ) -> InviteWorkerPostRequestHandler:
        return InviteWorkerPostRequestHandler(
            use_case=use_case,
            presenter=presenter,
            controller=controller,
            template_renderer=template_renderer,
            template_index=template_index,
        )

    @provider
    def provide_invite_worker_get_request_handler(
        self,
        use_case: ListWorkers,
        presenter: ListWorkersPresenter,
        controller: ListWorkersController,
        template_index: TemplateIndex,
        template_renderer: TemplateRenderer,
    ) -> InviteWorkerGetRequestHandler:
        return InviteWorkerGetRequestHandler(
            template_index=template_index,
            template_renderer=template_renderer,
            controller=controller,
            use_case=use_case,
            presenter=presenter,
        )

    @provider
    def provide_show_my_accounts_view(
        self,
        template_renderer: TemplateRenderer,
        controller: ShowMyAccountsController,
        use_case: ShowMyAccounts,
        presenter: ShowMyAccountsPresenter,
    ) -> ShowMyAccountsView:
        return ShowMyAccountsView(template_renderer, controller, use_case, presenter)

    @provider
    def provide_signup_member_view(
        self,
        register_member: RegisterMemberUseCase,
        member_repository: MemberRepository,
        controller: RegisterMemberController,
        register_member_presenter: RegisterMemberPresenter,
        flask_session: FlaskSession,
    ) -> SignupMemberView:
        return SignupMemberView(
            register_member=register_member,
            member_repository=member_repository,
            controller=controller,
            register_member_presenter=register_member_presenter,
            flask_session=flask_session,
        )

    @provider
    def provide_signup_company_view(
        self,
        use_case: RegisterCompany,
        controller: RegisterCompanyController,
        presenter: RegisterCompanyPresenter,
        flask_session: FlaskSession,
    ) -> SignupCompanyView:
        return SignupCompanyView(
            register_company=use_case,
            controller=controller,
            flask_session=flask_session,
            presenter=presenter,
        )

    @provider
    def provide_accountant_invitation_email_view(
        self,
        mail_service: MailService,
        template_renderer: TemplateRenderer,
    ) -> AccountantInvitationEmailView:
        return AccountantInvitationEmailViewImpl(
            mail_service=mail_service,
            template_renderer=template_renderer,
        )

    @provider
    def provide_create_cooperation_view(
        self,
        create_cooperation: CreateCooperation,
        presenter: CreateCooperationPresenter,
        template_renderer: UserTemplateRenderer,
        session: FlaskSession,
    ) -> CreateCooperationView:
        return CreateCooperationView(
            create_cooperation, presenter, template_renderer, session
        )

    @provider
    def provide_dashboard_view(
        self,
        list_workers_use_case: ListWorkers,
        get_latest_plans_use_case: GetLatestActivatedPlans,
        get_latest_plans_presenter: GetLatestActivatedPlansPresenter,
        template_renderer: UserTemplateRenderer,
        flask_session: FlaskSession,
    ) -> DashboardView:
        return DashboardView(
            list_workers_use_case,
            get_latest_plans_use_case,
            get_latest_plans_presenter,
            template_renderer,
            flask_session,
        )

    @provider
    def provide_signup_accountant_view(
        self,
        template_renderer: TemplateRenderer,
        controller: RegisterAccountantController,
        presenter: RegisterAccountantPresenter,
        use_case: RegisterAccountantUseCase,
    ) -> SignupAccountantView:
        return SignupAccountantView(
            template_renderer=template_renderer,
            controller=controller,
            presenter=presenter,
            use_case=use_case,
        )

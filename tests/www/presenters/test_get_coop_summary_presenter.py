from dataclasses import replace
from decimal import Decimal
from uuid import uuid4

from arbeitszeit.use_cases.get_coop_summary import AssociatedPlan, GetCoopSummarySuccess
from arbeitszeit_web.session import UserRole
from arbeitszeit_web.www.presenters.get_coop_summary_presenter import (
    GetCoopSummarySuccessPresenter,
)
from tests.www.base_test_case import BaseTestCase

TESTING_RESPONSE_MODEL = GetCoopSummarySuccess(
    requester_is_coordinator=True,
    coop_id=uuid4(),
    coop_name="coop name",
    coop_definition="coop def\ncoop def2",
    current_coordinator=uuid4(),
    current_coordinator_name="coordinator name",
    plans=[
        AssociatedPlan(
            plan_id=uuid4(),
            plan_name="plan_name",
            plan_individual_price=Decimal("1"),
            plan_coop_price=Decimal(50.005),
            planner_id=uuid4(),
            planner_name="A Cooperating Company Coop.",
        )
    ],
)


class GetCoopSummarySuccessPresenterTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.presenter = self.injector.get(GetCoopSummarySuccessPresenter)
        self.session.login_company(company=uuid4())

    def test_end_coop_button_is_shown_when_requester_is_coordinator(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertTrue(view_model.show_end_coop_button)

    def test_end_coop_button_is_not_shown_when_requester_not_coordinator(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            requester_is_coordinator=False,
        )
        view_model = self.presenter.present(response)
        self.assertFalse(view_model.show_end_coop_button)

    def test_coop_id_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(view_model.coop_id, str(TESTING_RESPONSE_MODEL.coop_id))

    def test_coop_name_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(view_model.coop_name, TESTING_RESPONSE_MODEL.coop_name)

    def test_coop_definition_is_displayed_correctly_as_list_of_strings(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(view_model.coop_definition, ["coop def", "coop def2"])

    def test_coordinator_id_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.current_coordinator_id,
            str(TESTING_RESPONSE_MODEL.current_coordinator),
        )

    def test_coordinator_name_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.current_coordinator_name,
            TESTING_RESPONSE_MODEL.current_coordinator_name,
        )

    def test_link_to_coordinators_company_summary_page_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.current_coordinator_url,
            self.url_index.get_company_summary_url(
                company_id=TESTING_RESPONSE_MODEL.current_coordinator,
                user_role=UserRole.company,
            ),
        )

    def test_first_plans_name_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.plans[0].plan_name, TESTING_RESPONSE_MODEL.plans[0].plan_name
        )

    def test_first_plans_individual_price_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.plans[0].plan_individual_price,
            "1.00",
        )

    def test_first_plans_coop_price_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.plans[0].plan_coop_price,
            "50.01",
        )

    def test_first_plans_end_coop_url_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.plans[0].end_coop_url,
            self.url_index.get_end_coop_url(
                plan_id=TESTING_RESPONSE_MODEL.plans[0].plan_id,
                cooperation_id=TESTING_RESPONSE_MODEL.coop_id,
            ),
        )

    def test_first_plans_planner_name_is_displayed_correctly(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.plans[0].planner_name,
            "A Cooperating Company Coop.",
        )

    def test_url_to_first_plans_planner_company_summary_page_is_displayed_correctly(
        self,
    ):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.plans[0].planner_url,
            self.url_index.get_company_summary_url(
                user_role=UserRole.company,
                company_id=TESTING_RESPONSE_MODEL.plans[0].planner_id,
            ),
        )

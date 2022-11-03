from decimal import Decimal
from typing import Dict

from arbeitszeit.repositories import PlanDraftRepository
from tests.data_generators import PlanGenerator
from tests.request import FakeRequest

from .flask import ViewTestCase


class AuthenticatedCompanyTestsForGet(ViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.plan_generator = self.injector.get(PlanGenerator)
        self.company = self.login_company()

    def test_get_200_without_url_parameter(
        self,
    ) -> None:
        url = "/company/create_draft"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_200_with_existing_expired_plan_as_url_parameter(
        self,
    ) -> None:
        plan = self.plan_generator.create_plan()
        url = f"/company/create_draft?expired_plan_id={str(plan.id)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class AuthenticatedCompanyTestsForPost(ViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.plan_generator = self.injector.get(PlanGenerator)
        self.plan_draft_repository = self.injector.get(PlanDraftRepository)
        self.form = self.injector.get(FakeRequest)
        self.company = self.login_company()

    def test_post_user_canceling_leads_to_302_and_no_draft_gets_created(self) -> None:
        test_data = self._create_form_data()
        response = self.client.post("/company/create_draft", data=test_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self._count_drafts_of_company())

    def test_post_user_saving_draft_leads_to_302_and_draft_gets_created(self) -> None:
        self.assertFalse(self._count_drafts_of_company())
        test_data = self._create_form_data(action="save_draft")
        response = self.client.post("/company/create_draft", data=test_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self._count_drafts_of_company(),
            1,
        )

    def _create_form_data(self, action: str = "cancel") -> Dict:
        return dict(
            prd_name="test name",
            description="test description",
            timeframe=14,
            prd_unit="1 piece",
            prd_amount=10,
            costs_p=Decimal("10.5"),
            costs_r=Decimal("15"),
            costs_a=Decimal("20"),
            productive_or_public=True,
            action=action,
        )

    def _count_drafts_of_company(self) -> int:
        return len(
            list(self.plan_draft_repository.all_drafts_of_company(self.company.id))
        )

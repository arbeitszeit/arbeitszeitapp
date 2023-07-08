from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from uuid import uuid4

from arbeitszeit.entities import ProductionCosts
from arbeitszeit.plan_summary import PlanSummary, PlanSummaryService
from arbeitszeit.use_cases.calculate_fic_and_update_expired_plans import (
    CalculateFicAndUpdateExpiredPlans,
)
from tests.data_generators import CompanyGenerator, CooperationGenerator, PlanGenerator
from tests.datetime_service import FakeDatetimeService
from tests.use_cases.dependency_injection import get_dependency_injector


class PlanSummaryServiceTests(TestCase):
    def setUp(self) -> None:
        self.injector = get_dependency_injector()
        self.service = self.injector.get(PlanSummaryService)
        self.plan_generator = self.injector.get(PlanGenerator)
        self.coop_generator = self.injector.get(CooperationGenerator)
        self.company_generator = self.injector.get(CompanyGenerator)
        self.planner = self.company_generator.create_company_entity()
        self.plan = self.plan_generator.create_plan(planner=self.planner.id)
        assert self.planner
        summary = self.service.get_summary_from_plan(self.plan.id)
        assert summary is not None
        self.summary: PlanSummary = summary
        self.payout_use_case = self.injector.get(CalculateFicAndUpdateExpiredPlans)
        self.datetime_service = self.injector.get(FakeDatetimeService)

    def test_that_no_summary_is_returned_when_plan_id_does_not_exist(self) -> None:
        summary = self.service.get_summary_from_plan(uuid4())
        assert not summary

    def test_that_correct_planner_id_is_shown(self) -> None:
        self.assertEqual(self.summary.plan_id, self.plan.id)

    def test_that_correct_planner_name_is_shown(self) -> None:
        self.assertEqual(self.summary.planner_name, self.planner.name)

    def test_that_correct_active_status_is_shown_when_plan_is_active(self) -> None:
        plan = self.plan_generator.create_plan()
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertTrue(summary.is_active)

    def test_that_correct_production_costs_are_shown(self) -> None:
        plan = self.plan_generator.create_plan(
            costs=ProductionCosts(
                means_cost=Decimal(1),
                labour_cost=Decimal(2),
                resource_cost=Decimal(3),
            )
        )
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertEqual(summary.means_cost, Decimal(1))
        self.assertEqual(summary.labour_cost, Decimal(2))
        self.assertEqual(summary.resources_cost, Decimal(3))

    def test_that_correct_price_per_unit_of_zero_is_shown_when_plan_is_public_service(
        self,
    ) -> None:
        plan = self.plan_generator.create_plan(
            is_public_service=True,
            costs=ProductionCosts(
                means_cost=Decimal(1),
                labour_cost=Decimal(2),
                resource_cost=Decimal(3),
            ),
        )
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertEqual(summary.price_per_unit, Decimal(0))

    def test_that_correct_price_per_unit_is_shown_when_plan_is_productive(self) -> None:
        plan = self.plan_generator.create_plan(
            is_public_service=False,
            amount=2,
            costs=ProductionCosts(
                means_cost=Decimal(1),
                labour_cost=Decimal(2),
                resource_cost=Decimal(3),
            ),
        )
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertEqual(summary.price_per_unit, Decimal(3))

    def test_that_correct_product_name_is_shown(self) -> None:
        self.assertEqual(self.summary.product_name, self.plan.prd_name)

    def test_that_correct_product_description_is_shown(self) -> None:
        self.assertEqual(self.summary.description, self.plan.description)

    def test_that_correct_product_unit_is_shown(self) -> None:
        self.assertEqual(self.summary.production_unit, self.plan.prd_unit)

    def test_that_correct_amount_is_shown(self) -> None:
        plan = self.plan_generator.create_plan(amount=123)
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertEqual(summary.amount, 123)

    def test_that_correct_public_service_is_shown(self) -> None:
        plan = self.plan_generator.create_plan(is_public_service=True)
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertTrue(summary.is_public_service)

    def test_that_correct_availability_is_shown(self) -> None:
        plan = self.plan_generator.create_plan()
        assert plan.is_available
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertTrue(summary.is_available)

    def test_that_no_cooperation_is_shown_when_plan_is_not_cooperating(self) -> None:
        plan = self.plan_generator.create_plan(cooperation=None)
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertFalse(summary.is_cooperating)
        self.assertIsNone(summary.cooperation)

    def test_that_correct_cooperation_is_shown(self) -> None:
        coop = self.coop_generator.create_cooperation()
        plan = self.plan_generator.create_plan(cooperation=coop)
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertTrue(summary.is_cooperating)
        self.assertEqual(summary.cooperation, coop.id)

    def test_that_zero_active_days_is_shown_if_plan_is_not_active_yet(self) -> None:
        plan = self.plan_generator.create_plan(approved=False)
        self.payout_use_case()
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertEqual(summary.active_days, 0)

    def test_that_zero_active_days_is_shown_if_plan_is_active_since_less_than_one_day(
        self,
    ) -> None:
        plan = self.plan_generator.create_plan()
        self.payout_use_case()
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertEqual(summary.active_days, 0)

    def test_that_one_active_days_is_shown_if_plan_is_active_since_25_hours(
        self,
    ) -> None:
        self.datetime_service.freeze_time(datetime(2000, 1, 1))
        plan = self.plan_generator.create_plan()
        self.datetime_service.freeze_time(datetime(2000, 1, 2, hour=1))
        self.payout_use_case()
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertEqual(summary.active_days, 1)

    def test_that_a_plans_timeframe_is_shown_as_active_days_if_plan_is_expired(
        self,
    ) -> None:
        timeframe = 7
        self.datetime_service.freeze_time(datetime(2000, 1, 1))
        plan = self.plan_generator.create_plan(
            timeframe=timeframe,
        )
        self.datetime_service.freeze_time(datetime(2000, 1, 11))
        self.payout_use_case()
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertEqual(summary.active_days, timeframe)

    def test_that_creation_date_is_shown(self) -> None:
        self.assertEqual(self.summary.creation_date, self.plan.plan_creation_date)

    def test_that_approval_date_is_shown_if_it_exists(self) -> None:
        assert self.plan.approval_date
        self.assertEqual(self.summary.approval_date, self.plan.approval_date)

    def test_that_expiration_date_is_shown_if_it_exists(self) -> None:
        plan = self.plan_generator.create_plan(timeframe=5)
        self.payout_use_case()
        assert plan.expiration_date
        summary = self.service.get_summary_from_plan(plan.id)
        assert summary
        self.assertTrue(summary.expiration_date)

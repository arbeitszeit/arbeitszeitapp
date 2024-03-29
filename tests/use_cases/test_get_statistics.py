from decimal import Decimal
from typing import Union
from unittest import TestCase

from arbeitszeit.records import ProductionCosts
from arbeitszeit.use_cases.get_statistics import GetStatistics
from arbeitszeit.use_cases.register_hours_worked import (
    RegisterHoursWorked,
    RegisterHoursWorkedRequest,
)
from tests.data_generators import (
    CompanyGenerator,
    CooperationGenerator,
    MemberGenerator,
    PlanGenerator,
    TransactionGenerator,
)
from tests.datetime_service import FakeDatetimeService

from .dependency_injection import get_dependency_injector

Number = Union[int, Decimal]


def production_costs(p: Number, r: Number, a: Number) -> ProductionCosts:
    return ProductionCosts(
        Decimal(p),
        Decimal(r),
        Decimal(a),
    )


class GetStatisticsTester(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.injector = get_dependency_injector()
        self.use_case = self.injector.get(GetStatistics)
        self.company_generator = self.injector.get(CompanyGenerator)
        self.member_generator = self.injector.get(MemberGenerator)
        self.cooperation_generator = self.injector.get(CooperationGenerator)
        self.transaction_generator = self.injector.get(TransactionGenerator)
        self.datetime_service = self.injector.get(FakeDatetimeService)
        self.plan_generator = self.injector.get(PlanGenerator)
        self.register_hours_worked = self.injector.get(RegisterHoursWorked)

    def test_that_values_are_zero_if_repositories_are_empty(self) -> None:
        stats = self.use_case()
        assert stats.registered_companies_count == 0
        assert stats.registered_members_count == 0
        assert stats.active_plans_count == 0
        assert stats.active_plans_public_count == 0
        assert stats.avg_timeframe == 0
        assert stats.planned_work == 0
        assert stats.planned_resources == 0
        assert stats.planned_means == 0

    def test_counting_of_companies(self) -> None:
        self.company_generator.create_company_record()
        self.company_generator.create_company_record()
        stats = self.use_case()
        assert stats.registered_companies_count == 2

    def test_counting_of_members(self) -> None:
        self.member_generator.create_member()
        self.member_generator.create_member()
        stats = self.use_case()
        assert stats.registered_members_count == 2

    def test_counting_of_cooperations(self) -> None:
        number_of_coops = 2
        for _ in range(number_of_coops):
            self.cooperation_generator.create_cooperation()
        stats = self.use_case()
        assert stats.cooperations_count == number_of_coops

    def test_counting_of_certificates_when_certs_are_zero(self) -> None:
        stats = self.use_case()
        assert stats.certificates_count == 0

    def test_counting_of_certificates_when_two_members_have_received_certs(
        self,
    ) -> None:
        num_transactions = 2
        for _ in range(num_transactions):
            self.plan_generator.create_plan(
                costs=ProductionCosts(
                    labour_cost=Decimal(10),
                    means_cost=Decimal(0),
                    resource_cost=Decimal(0),
                )
            )
            worker = self.member_generator.create_member()
            workplace = self.company_generator.create_company(workers=[worker])
            assert not self.register_hours_worked(
                RegisterHoursWorkedRequest(
                    company_id=workplace,
                    worker_id=worker,
                    hours_worked=Decimal(10),
                )
            ).is_rejected
        stats = self.use_case()
        assert stats.certificates_count == num_transactions * Decimal(10)

    def test_available_product_is_positive_number_when_amount_on_prd_account_is_negative(
        self,
    ) -> None:
        company = self.company_generator.create_company_record()
        self.transaction_generator.create_transaction(
            receiving_account=company.product_account, amount_received=Decimal(-10)
        )
        stats = self.use_case()
        assert stats.available_product == Decimal(10)

    def test_correct_available_product_is_shown_when_two_companies_have_received_prd_debit(
        self,
    ) -> None:
        num_companies = 2
        for _ in range(num_companies):
            company = self.company_generator.create_company_record()
            self.transaction_generator.create_transaction(
                receiving_account=company.product_account, amount_received=Decimal(-22)
            )
        stats = self.use_case()
        assert stats.available_product == num_companies * Decimal(22)

    def test_counting_of_active_plans(self) -> None:
        self.plan_generator.create_plan()
        self.plan_generator.create_plan()
        stats = self.use_case()
        assert stats.active_plans_count == 2

    def test_counting_of_plans_that_are_both_active_and_public(self) -> None:
        self.plan_generator.create_plan(
            is_public_service=True,
        )
        self.plan_generator.create_plan(
            is_public_service=True,
        )
        stats = self.use_case()
        assert stats.active_plans_public_count == 2

    def test_that_inactive_and_productive_plans_are_ignored_when_counting_active_and_public_plans(
        self,
    ) -> None:
        self.plan_generator.create_plan(
            is_public_service=False,
        )
        self.plan_generator.create_plan(
            is_public_service=True,
        )
        stats = self.use_case()
        assert stats.active_plans_public_count == 1

    def test_average_calculation_of_two_active_plan_timeframes(self) -> None:
        self.plan_generator.create_plan(timeframe=3)
        self.plan_generator.create_plan(timeframe=7)
        stats = self.use_case()
        assert stats.avg_timeframe == 5

    def test_adding_up_work_of_two_plans(self) -> None:
        self.plan_generator.create_plan(
            costs=production_costs(3, 1, 1),
        )
        self.plan_generator.create_plan(
            costs=production_costs(2, 1, 1),
        )
        stats = self.use_case()
        assert stats.planned_work == 5

    def test_adding_up_resources_of_two_plans(self) -> None:
        self.plan_generator.create_plan(
            costs=production_costs(1, 3, 1),
        )
        self.plan_generator.create_plan(
            costs=production_costs(1, 2, 1),
        )
        stats = self.use_case()
        assert stats.planned_resources == 5

    def test_adding_up_means_of_two_plans(self) -> None:
        self.plan_generator.create_plan(
            costs=production_costs(1, 1, 3),
        )
        self.plan_generator.create_plan(
            costs=production_costs(1, 1, 2),
        )
        stats = self.use_case()
        assert stats.planned_means == 5

    def test_that_payout_factor_is_available_even_with_no_plans_in_approved(
        self,
    ) -> None:
        stats = self.use_case()
        assert stats.payout_factor is not None

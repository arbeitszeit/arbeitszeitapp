from dataclasses import dataclass

from injector import inject

from arbeitszeit.datetime_service import DatetimeService
from arbeitszeit.entities import Company, Plan, ProductionCosts
from arbeitszeit.repositories import PlanRepository


@dataclass
class PlanProposal:
    costs: ProductionCosts
    product_name: str
    production_unit: str
    production_amount: int
    description: str
    timeframe_in_days: int
    is_public_service: bool


@inject
@dataclass
class CreatePlan:
    plan_repository: PlanRepository
    datetime_service: DatetimeService

    def __call__(self, company: Company, plan_proposal: PlanProposal) -> Plan:
        return self.plan_repository.create_plan(
            planner=company,
            costs=plan_proposal.costs,
            product_name=plan_proposal.product_name,
            production_unit=plan_proposal.production_unit,
            amount=plan_proposal.production_amount,
            description=plan_proposal.description,
            timeframe_in_days=plan_proposal.timeframe_in_days,
            is_public_service=plan_proposal.is_public_service,
            creation_timestamp=self.datetime_service.now(),
        )

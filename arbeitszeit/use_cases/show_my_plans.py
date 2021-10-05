from dataclasses import dataclass
from typing import List
from uuid import UUID

from injector import inject

from arbeitszeit.entities import Plan
from arbeitszeit.repositories import PlanRepository


@dataclass
class ShowMyPlansRequest:
    company_id: UUID


@dataclass
class ShowMyPlansResponse:
    all_plans: List[Plan]
    non_active_plans: List[Plan]
    active_plans: List[Plan]
    expired_plans: List[Plan]


@inject
@dataclass
class ShowMyPlansUseCase:
    plan_repository: PlanRepository

    def __call__(self, request: ShowMyPlansRequest) -> ShowMyPlansResponse:
        all_plans = [
            plan
            for plan in self.plan_repository.get_all_plans_for_company(
                request.company_id
            )
        ]
        non_active_plans = [
            plan
            for plan in self.plan_repository.get_non_active_plans_for_company(
                request.company_id
            )
        ]
        active_plans = [
            plan
            for plan in self.plan_repository.get_active_plans_for_company(
                request.company_id
            )
        ]
        expired_plans = [
            plan
            for plan in self.plan_repository.get_expired_plans_for_company(
                request.company_id
            )
        ]
        return ShowMyPlansResponse(
            all_plans=all_plans,
            non_active_plans=non_active_plans,
            active_plans=active_plans,
            expired_plans=expired_plans,
        )

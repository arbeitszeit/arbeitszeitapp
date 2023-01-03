from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID


@dataclass
class SocialAccounting:
    id: UUID
    account: Account

    def get_name(self) -> str:
        return "Social Accounting"


@dataclass
class Member:
    id: UUID
    name: str
    email: str
    account: Account
    registered_on: datetime
    confirmed_on: Optional[datetime]

    def accounts(self) -> List[Account]:
        return [self.account]

    def get_name(self) -> str:
        return self.name


@dataclass
class Company:
    id: UUID
    email: str
    name: str
    means_account: Account
    raw_material_account: Account
    work_account: Account
    product_account: Account
    registered_on: datetime
    confirmed_on: Optional[datetime]

    def accounts(self) -> List[Account]:
        return [
            self.means_account,
            self.raw_material_account,
            self.work_account,
            self.product_account,
        ]

    def get_name(self) -> str:
        return self.name


class AccountTypes(Enum):
    p = "p"
    r = "r"
    a = "a"
    prd = "prd"
    member = "member"
    accounting = "accounting"


@dataclass
class Account:
    id: UUID
    account_type: AccountTypes


@dataclass
class Cooperation:
    id: UUID
    creation_date: datetime
    name: str
    definition: str
    coordinator: Company


@dataclass
class ProductionCosts:
    labour_cost: Decimal
    resource_cost: Decimal
    means_cost: Decimal

    def total_cost(self) -> Decimal:
        return self.labour_cost + self.resource_cost + self.means_cost

    def __truediv__(self, other: Union[int, float]) -> ProductionCosts:
        denominator = Decimal(other)
        return ProductionCosts(
            labour_cost=self.labour_cost / denominator,
            resource_cost=self.resource_cost / denominator,
            means_cost=self.means_cost / denominator,
        )

    def __add__(self, other: ProductionCosts) -> ProductionCosts:
        return ProductionCosts(
            labour_cost=self.labour_cost + other.labour_cost,
            resource_cost=self.resource_cost + other.resource_cost,
            means_cost=self.means_cost + other.means_cost,
        )


@dataclass
class PlanDraft:
    id: UUID
    creation_date: datetime
    planner: Company
    production_costs: ProductionCosts
    product_name: str
    unit_of_distribution: str
    amount_produced: int
    description: str
    timeframe: int
    is_public_service: bool

    @property
    def expected_sales_value(self) -> Decimal:
        """
        For productive plans, sales value should equal total cost.
        Public services are not expected to sell,
        they give away their product for free.
        """
        return (
            self.production_costs.total_cost()
            if not self.is_public_service
            else Decimal(0)
        )


@dataclass
class Plan:
    id: UUID
    plan_creation_date: datetime
    planner: UUID
    production_costs: ProductionCosts
    prd_name: str
    prd_unit: str
    prd_amount: int
    description: str
    timeframe: int
    is_public_service: bool
    approval_date: Optional[datetime]
    approval_reason: Optional[str]
    is_active: bool
    expired: bool
    activation_date: Optional[datetime]
    active_days: Optional[int]
    payout_count: int
    requested_cooperation: Optional[UUID]
    cooperation: Optional[UUID]
    is_available: bool
    hidden_by_user: bool

    @property
    def expected_sales_value(self) -> Decimal:
        """
        For productive plans, sales value should equal total cost.
        Public services are not expected to sell,
        they give away their product for free.
        """
        return (
            self.production_costs.total_cost()
            if not self.is_public_service
            else Decimal(0)
        )

    @property
    def is_approved(self) -> bool:
        return self.approval_date is not None

    @property
    def expiration_date(self) -> Optional[datetime]:
        if not self.activation_date:
            return None
        exp_date = self.activation_date + timedelta(days=int(self.timeframe))
        return exp_date


class PurposesOfPurchases(Enum):
    means_of_prod = "means_of_prod"
    raw_materials = "raw_materials"
    consumption = "consumption"


@dataclass
class Purchase:
    purchase_date: datetime
    plan: UUID
    buyer: UUID
    is_buyer_a_member: bool
    price_per_unit: Decimal
    amount: int
    purpose: PurposesOfPurchases


@dataclass
class Transaction:
    """
    The amount received by a transaction can differ from the amount sent.
    This is e.g. the case when a product is paid. Then the amount sent is defined by
    the current coop_price, while the amount received (by the prd-account of the company)
    is defined by the originally planned costs for the product.
    """

    id: UUID
    date: datetime
    sending_account: UUID
    receiving_account: UUID
    amount_sent: Decimal
    amount_received: Decimal
    purpose: str

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class CompanyWorkInvite:
    id: UUID
    company: Company
    member: Member


@dataclass
class Accountant:
    id: UUID
    email_address: str
    name: str


@dataclass
class PayoutFactor:
    calculation_date: datetime
    value: Decimal

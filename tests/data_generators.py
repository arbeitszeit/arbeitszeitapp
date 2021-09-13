"""The classes in this module should only provide instances of
entities. Never should these entities automatically be added to a
repository.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union
from uuid import uuid4

from injector import inject

from arbeitszeit.entities import (
    Account,
    AccountTypes,
    Company,
    Member,
    Plan,
    ProductionCosts,
    Purchase,
    PurposesOfPurchases,
    SocialAccounting,
    Transaction,
)
from arbeitszeit.repositories import (
    AccountRepository,
    CompanyRepository,
    MemberRepository,
    PlanRepository,
    TransactionRepository,
)
from arbeitszeit.use_cases import (
    CreateOffer,
    CreateOfferRequest,
    CreateOfferResponse,
    SeekApproval,
)
from tests.datetime_service import FakeDatetimeService


@inject
@dataclass
class OfferGenerator:
    plan_generator: PlanGenerator
    company_generator: CompanyGenerator
    _create_offer: CreateOffer

    def create_offer(
        self,
        *,
        name="Product name",
        description="",
        plan_id=str(uuid4()),
        seller=None,
        price_per_unit=3,
    ) -> CreateOfferResponse:
        if seller is None:
            seller = self.company_generator.create_company().id
        return self._create_offer(
            CreateOfferRequest(
                name=name,
                description=description,
                plan_id=plan_id,
                seller=seller,
                price_per_unit=price_per_unit,
            )
        )


@inject
@dataclass
class MemberGenerator:
    account_generator: AccountGenerator
    email_generator: EmailGenerator
    member_repository: MemberRepository

    def create_member(self, *, email: Optional[str] = None) -> Member:
        if not email:
            email = self.email_generator.get_random_email()
        assert email is not None
        return self.member_repository.create_member(
            email=email,
            name="Member name",
            password="password",
            account=self.account_generator.create_account(
                account_type=AccountTypes.member
            ),
        )


@inject
@dataclass
class CompanyGenerator:
    account_generator: AccountGenerator
    company_repository: CompanyRepository
    email_generator: EmailGenerator

    def create_company(
        self, *, email: Optional[str] = None, name: str = "Company Name"
    ) -> Company:
        if email is None:
            email = self.email_generator.get_random_email()
        return self.company_repository.create_company(
            email=email,
            name=name,
            password="password",
            means_account=self.account_generator.create_account(
                account_type=AccountTypes.p
            ),
            resource_account=self.account_generator.create_account(
                account_type=AccountTypes.r
            ),
            labour_account=self.account_generator.create_account(
                account_type=AccountTypes.a
            ),
            products_account=self.account_generator.create_account(
                account_type=AccountTypes.prd
            ),
        )


@inject
@dataclass
class SocialAccountingGenerator:
    account_generator: AccountGenerator

    def create_social_accounting(self) -> SocialAccounting:
        return SocialAccounting(
            account=self.account_generator.create_account(
                account_type=AccountTypes.accounting
            ),
        )


@inject
@dataclass
class AccountGenerator:
    account_repository: AccountRepository

    def create_account(self, account_type) -> Account:
        return self.account_repository.create_account(account_type)


class EmailGenerator:
    def get_random_email(self):
        return str(uuid4()) + "@cp.org"


@inject
@dataclass
class PlanGenerator:
    company_generator: CompanyGenerator
    datetime_service: FakeDatetimeService
    plan_repository: PlanRepository
    seek_approval: SeekApproval

    def create_plan(
        self,
        *,
        id=None,
        plan_creation_date=None,
        planner=None,
        timeframe=None,
        approved=False,
        activation_date: Optional[datetime] = None,
        amount: int = 100,
        costs: Optional[ProductionCosts] = None,
        is_public_service=False,
        product_name="Produkt A",
        description="Beschreibung für Produkt A.",
        production_unit="500 Gramm",
    ) -> Plan:
        if costs is None:
            costs = ProductionCosts(Decimal(1), Decimal(1), Decimal(1))
        costs = costs
        if plan_creation_date is None:
            plan_creation_date = self.datetime_service.now_minus_two_days()
        if planner is None:
            planner = self.company_generator.create_company()
        if timeframe is None:
            timeframe = 14
        plan = self.plan_repository.create_plan(
            id=id,
            planner=planner,
            costs=costs,
            product_name=product_name,
            production_unit=production_unit,
            amount=amount,
            description=description,
            timeframe_in_days=timeframe,
            is_public_service=is_public_service,
            creation_timestamp=plan_creation_date,
        )
        if approved:
            self.seek_approval(plan.id)
        if activation_date:
            self.plan_repository.activate_plan(plan, activation_date)
        return plan


@inject
@dataclass
class PurchaseGenerator:
    plan_generator: PlanGenerator
    member_generator: MemberGenerator
    company_generator: CompanyGenerator
    datetime_service: FakeDatetimeService

    def create_purchase(
        self,
        buyer: Union[Member, Company],
        purchase_date=None,
        amount=1,
    ) -> Purchase:
        if purchase_date is None:
            purchase_date = self.datetime_service.now_minus_one_day()
        return Purchase(
            purchase_date=purchase_date,
            plan=self.plan_generator.create_plan(),
            buyer=buyer,
            price_per_unit=Decimal(10),
            amount=amount,
            purpose=PurposesOfPurchases.consumption,
        )


@inject
@dataclass
class TransactionGenerator:
    account_generator: AccountGenerator
    transaction_repository: TransactionRepository
    datetime_service: FakeDatetimeService

    def create_transaction(
        self,
        sending_account_type=AccountTypes.p,
        receiving_account_type=AccountTypes.prd,
        sending_account=None,
        receiving_account=None,
    ) -> Transaction:
        return self.transaction_repository.create_transaction(
            date=self.datetime_service.now_minus_one_day(),
            sending_account=self.account_generator.create_account(
                account_type=sending_account_type
            )
            if None
            else sending_account,
            receiving_account=self.account_generator.create_account(
                account_type=receiving_account_type
            )
            if None
            else receiving_account,
            amount=Decimal(10),
            purpose="Test Verw.zweck",
        )

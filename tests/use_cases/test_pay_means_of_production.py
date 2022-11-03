from datetime import datetime, timedelta
from decimal import Decimal
from unittest import TestCase
from uuid import uuid4

from arbeitszeit.entities import Company, ProductionCosts, PurposesOfPurchases
from arbeitszeit.price_calculator import calculate_price
from arbeitszeit.use_cases import (
    GetCompanyTransactions,
    PayMeansOfProduction,
    PayMeansOfProductionRequest,
)
from arbeitszeit.use_cases.update_plans_and_payout import UpdatePlansAndPayout
from arbeitszeit_web.get_company_transactions import GetCompanyTransactionsResponse
from tests.data_generators import CompanyGenerator, CooperationGenerator, PlanGenerator
from tests.datetime_service import FakeDatetimeService

from .dependency_injection import get_dependency_injector, injection_test
from .repositories import (
    AccountRepository,
    PlanCooperationRepository,
    PurchaseRepository,
    TransactionRepository,
)


@injection_test
def test_reject_payment_if_plan_is_expired(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    datetime_service: FakeDatetimeService,
    update_plans_and_payout: UpdatePlansAndPayout,
):
    datetime_service.freeze_time(datetime(2000, 1, 1))
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(timeframe=1)
    update_plans_and_payout()
    datetime_service.freeze_time(datetime(2001, 1, 1))
    update_plans_and_payout()
    purpose = PurposesOfPurchases.means_of_prod
    pieces = 5
    plan.expired = True
    response = pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )
    assert response.is_rejected
    assert response.rejection_reason == response.RejectionReason.plan_is_not_active


@injection_test
def test_payment_is_rejected_when_purpose_is_consumption(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(activation_date=datetime.min)
    purpose = PurposesOfPurchases.consumption
    response = pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, 5, purpose)
    )
    assert response.is_rejected
    assert response.rejection_reason == response.RejectionReason.invalid_purpose


@injection_test
def test_reject_payment_trying_to_pay_public_service(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    datetime_service: FakeDatetimeService,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        is_public_service=True, activation_date=datetime_service.now_minus_one_day()
    )
    purpose = PurposesOfPurchases.means_of_prod
    response = pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, 5, purpose)
    )
    assert response.is_rejected
    assert (
        response.rejection_reason == response.RejectionReason.cannot_buy_public_service
    )


@injection_test
def test_reject_payment_trying_to_pay_own_product(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    datetime_service: FakeDatetimeService,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day(), planner=sender
    )
    purpose = PurposesOfPurchases.means_of_prod
    response = pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, 5, purpose)
    )
    assert response.is_rejected
    assert response.rejection_reason == response.RejectionReason.buyer_is_planner


@injection_test
def test_balance_of_buyer_of_means_of_prod_reduced(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    account_repository: AccountRepository,
    datetime_service: FakeDatetimeService,
    plan_cooperation_repository: PlanCooperationRepository,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day()
    )
    purpose = PurposesOfPurchases.means_of_prod
    pieces = 5

    pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )

    price_total = pieces * calculate_price(
        plan_cooperation_repository.get_cooperating_plans(plan.id)
    )
    assert account_repository.get_account_balance(sender.means_account) == -price_total


@injection_test
def test_balance_of_buyer_of_raw_materials_reduced(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    account_repository: AccountRepository,
    datetime_service: FakeDatetimeService,
    plan_cooperation_repository: PlanCooperationRepository,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day()
    )
    purpose = PurposesOfPurchases.raw_materials
    pieces = 5

    pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )

    price_total = pieces * calculate_price(
        plan_cooperation_repository.get_cooperating_plans(plan.id)
    )
    assert (
        account_repository.get_account_balance(sender.raw_material_account)
        == -price_total
    )


@injection_test
def test_balance_of_seller_increased(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    account_repository: AccountRepository,
    datetime_service: FakeDatetimeService,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        costs=ProductionCosts(
            labour_cost=Decimal(1),
            means_cost=Decimal(1),
            resource_cost=Decimal(1),
        ),
        amount=5,
    )
    purpose = PurposesOfPurchases.raw_materials
    pieces = 5
    assert account_repository.get_account_balance(
        plan.planner.product_account
    ) == Decimal("-3")
    pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )

    assert account_repository.get_account_balance(
        plan.planner.product_account
    ) == Decimal("0")


@injection_test
def test_balance_of_seller_increased_correctly_when_plan_is_in_cooperation(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    account_repository: AccountRepository,
    datetime_service: FakeDatetimeService,
    cooperation_generator: CooperationGenerator,
):
    coop = cooperation_generator.create_cooperation()
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day(),
        amount=50,
        cooperation=coop,
    )
    plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day(),
        amount=200,
        cooperation=coop,
    )

    purpose = PurposesOfPurchases.raw_materials
    pieces = 5

    balance_before_transaction = account_repository.get_account_balance(
        plan.planner.product_account
    )

    pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )

    assert account_repository.get_account_balance(
        plan.planner.product_account
    ) == balance_before_transaction + (
        plan.production_costs.total_cost() / Decimal(plan.prd_amount) * 5
    )


@injection_test
def test_correct_transaction_added_if_means_of_production_were_paid(
    pay_means_of_production: PayMeansOfProduction,
    transaction_repository: TransactionRepository,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    datetime_service: FakeDatetimeService,
    plan_cooperation_repository: PlanCooperationRepository,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day()
    )
    purpose = PurposesOfPurchases.means_of_prod
    pieces = 5
    transactions_before_payment = len(transaction_repository.transactions)
    pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )
    price_total = pieces * calculate_price(
        plan_cooperation_repository.get_cooperating_plans(plan.id)
    )
    assert len(transaction_repository.transactions) == transactions_before_payment + 1
    assert (
        transaction_repository.transactions[-1].sending_account == sender.means_account
    )
    assert (
        transaction_repository.transactions[-1].receiving_account
        == plan.planner.product_account
    )
    assert transaction_repository.transactions[-1].amount_sent == price_total
    assert transaction_repository.transactions[-1].amount_received == price_total


@injection_test
def test_correct_transaction_added_if_raw_materials_were_paid(
    pay_means_of_production: PayMeansOfProduction,
    transaction_repository: TransactionRepository,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    datetime_service: FakeDatetimeService,
    plan_cooperation_repository: PlanCooperationRepository,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day()
    )
    purpose = PurposesOfPurchases.raw_materials
    pieces = 5
    transactions_before_payment = len(transaction_repository.transactions)
    pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )
    price_total = pieces * calculate_price(
        plan_cooperation_repository.get_cooperating_plans(plan.id)
    )
    assert len(transaction_repository.transactions) == transactions_before_payment + 1
    assert (
        transaction_repository.transactions[-1].sending_account
        == sender.raw_material_account
    )
    assert (
        transaction_repository.transactions[-1].receiving_account
        == plan.planner.product_account
    )
    assert transaction_repository.transactions[-1].amount_sent == price_total
    assert transaction_repository.transactions[-1].amount_received == price_total


@injection_test
def test_correct_purchase_added_if_means_of_production_were_paid(
    pay_means_of_production: PayMeansOfProduction,
    purchase_repository: PurchaseRepository,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    datetime_service: FakeDatetimeService,
    plan_cooperation_repository: PlanCooperationRepository,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day()
    )
    purpose = PurposesOfPurchases.means_of_prod
    pieces = 5
    pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )
    purchase_added = purchase_repository.purchases[0]
    assert len(purchase_repository.purchases) == 1
    assert purchase_added.plan == plan.id
    assert purchase_added.price_per_unit == calculate_price(
        plan_cooperation_repository.get_cooperating_plans(plan.id)
    )
    assert purchase_added.amount == pieces
    assert purchase_added.purpose == PurposesOfPurchases.means_of_prod
    assert purchase_added.buyer == sender.id
    assert purchase_added.plan == plan.id
    assert purchase_added.is_buyer_a_member == False


@injection_test
def test_correct_purchase_added_if_raw_materials_were_paid(
    pay_means_of_production: PayMeansOfProduction,
    purchase_repository: PurchaseRepository,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
    datetime_service: FakeDatetimeService,
    plan_cooperation_repository: PlanCooperationRepository,
):
    sender = company_generator.create_company()
    plan = plan_generator.create_plan(
        activation_date=datetime_service.now_minus_one_day()
    )
    purpose = PurposesOfPurchases.raw_materials
    pieces = 5
    pay_means_of_production(
        PayMeansOfProductionRequest(sender.id, plan.id, pieces, purpose)
    )
    purchase_added = purchase_repository.purchases[0]
    assert len(purchase_repository.purchases) == 1
    assert purchase_added.plan == plan.id
    assert purchase_added.price_per_unit == calculate_price(
        plan_cooperation_repository.get_cooperating_plans(plan.id)
    )
    assert purchase_added.amount == pieces
    assert purchase_added.purpose == PurposesOfPurchases.raw_materials
    assert purchase_added.buyer == sender.id
    assert purchase_added.plan == plan.id
    assert purchase_added.is_buyer_a_member == False


@injection_test
def test_plan_not_found_rejects_payment(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
) -> None:
    buyer = company_generator.create_company()
    response = pay_means_of_production(
        PayMeansOfProductionRequest(
            buyer=buyer.id,
            plan=uuid4(),
            amount=1,
            purpose=PurposesOfPurchases.means_of_prod,
        )
    )
    assert response.is_rejected
    assert response.rejection_reason == response.RejectionReason.plan_not_found


@injection_test
def test_plan_found_accepts_payment(
    pay_means_of_production: PayMeansOfProduction,
    company_generator: CompanyGenerator,
    plan_generator: PlanGenerator,
) -> None:
    buyer = company_generator.create_company()
    plan = plan_generator.create_plan(activation_date=datetime.min)
    response = pay_means_of_production(
        PayMeansOfProductionRequest(
            buyer=buyer.id,
            plan=plan.id,
            amount=1,
            purpose=PurposesOfPurchases.means_of_prod,
        )
    )
    assert not response.is_rejected
    assert response.rejection_reason is None


class TestSuccessfulPayment(TestCase):
    def setUp(self) -> None:
        self.injector = get_dependency_injector()
        self.company_generator = self.injector.get(CompanyGenerator)
        self.plan_generator = self.injector.get(PlanGenerator)
        self.buyer = self.company_generator.create_company()
        self.planner = self.company_generator.create_company()
        self.plan = self.plan_generator.create_plan(
            planner=self.planner, activation_date=datetime.min
        )
        self.pay_means_of_production = self.injector.get(PayMeansOfProduction)
        self.get_company_transactions = self.injector.get(GetCompanyTransactions)
        self.datetime_service = self.injector.get(FakeDatetimeService)
        self.transaction_time = datetime(2020, 10, 1, 22, 30)
        self.datetime_service.freeze_time(self.transaction_time)
        self.planner_transactions_before_payment = len(
            self.get_company_transactions(self.planner.id).transactions
        )
        self.response = self.pay_means_of_production(
            PayMeansOfProductionRequest(
                buyer=self.buyer.id,
                plan=self.plan.id,
                amount=1,
                purpose=PurposesOfPurchases.means_of_prod,
            )
        )
        self.datetime_service.freeze_time(self.transaction_time + timedelta(days=1))

    def test_transaction_shows_up_in_transaction_listing_for_buyer(self) -> None:
        transaction_info = self.get_buyer_transaction_infos(self.buyer)
        self.assertEqual(len(transaction_info.transactions), 1)

    def test_transaction_shows_up_in_transaction_listing_for_planner(self) -> None:
        transaction_info = self.get_company_transactions(self.planner.id)
        self.assertEqual(
            len(transaction_info.transactions),
            self.planner_transactions_before_payment + 1,
        )

    def test_transaction_info_of_buyer_shows_transaction_timestamp(self) -> None:
        transaction_info = self.get_company_transactions(self.buyer.id)
        self.assertEqual(transaction_info.transactions[0].date, self.transaction_time)

    def test_transaction_info_of_planner_shows_transaction_timestamp(self) -> None:
        transaction_info = self.get_company_transactions(self.planner.id)
        self.assertEqual(transaction_info.transactions[-1].date, self.transaction_time)

    def get_buyer_transaction_infos(
        self, user: Company
    ) -> GetCompanyTransactionsResponse:
        return self.get_company_transactions(user.id)

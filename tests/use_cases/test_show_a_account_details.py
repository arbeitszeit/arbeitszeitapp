from datetime import datetime
from decimal import Decimal

from arbeitszeit.entities import SocialAccounting
from arbeitszeit.transactions import TransactionTypes
from arbeitszeit.use_cases.show_a_account_details import ShowAAccountDetailsUseCase
from tests.data_generators import (
    CompanyGenerator,
    MemberGenerator,
    TransactionGenerator,
)

from .dependency_injection import injection_test


@injection_test
def test_no_transactions_returned_when_no_transactions_took_place(
    show_a_account_details: ShowAAccountDetailsUseCase,
    member_generator: MemberGenerator,
    company_generator: CompanyGenerator,
):
    member_generator.create_member_entity()
    company = company_generator.create_company_entity()

    response = show_a_account_details(company.id)
    assert not response.transactions


@injection_test
def test_balance_is_zero_when_no_transactions_took_place(
    show_a_account_details: ShowAAccountDetailsUseCase,
    member_generator: MemberGenerator,
    company_generator: CompanyGenerator,
):
    member_generator.create_member_entity()
    company = company_generator.create_company_entity()

    response = show_a_account_details(company.id)
    assert response.account_balance == 0


@injection_test
def test_company_id_is_returned(
    show_p_account_details: ShowAAccountDetailsUseCase,
    member_generator: MemberGenerator,
    company_generator: CompanyGenerator,
):
    member_generator.create_member_entity()
    company = company_generator.create_company_entity()

    response = show_p_account_details(company.id)
    assert response.company_id == company.id


@injection_test
def test_that_no_info_is_generated_after_selling_of_consumer_product(
    show_a_account_details: ShowAAccountDetailsUseCase,
    member_generator: MemberGenerator,
    company_generator: CompanyGenerator,
    transaction_generator: TransactionGenerator,
):
    member = member_generator.create_member_entity()
    company = company_generator.create_company_entity()

    transaction_generator.create_transaction(
        sending_account=member.account,
        receiving_account=company.product_account,
        amount_sent=Decimal(10),
        amount_received=Decimal(8.5),
    )

    response = show_a_account_details(company.id)
    assert len(response.transactions) == 0


@injection_test
def test_that_no_info_is_generated_when_company_sells_p(
    show_a_account_details: ShowAAccountDetailsUseCase,
    company_generator: CompanyGenerator,
    transaction_generator: TransactionGenerator,
):
    company1 = company_generator.create_company_entity()
    company2 = company_generator.create_company_entity()

    transaction_generator.create_transaction(
        sending_account=company1.means_account,
        receiving_account=company2.product_account,
        amount_sent=Decimal(10),
        amount_received=Decimal(8.5),
    )

    response = show_a_account_details(company2.id)
    assert not response.transactions


@injection_test
def test_that_no_info_is_generated_when_credit_for_r_is_granted(
    show_a_account_details: ShowAAccountDetailsUseCase,
    company_generator: CompanyGenerator,
    transaction_generator: TransactionGenerator,
    social_accounting: SocialAccounting,
):
    company = company_generator.create_company_entity()

    transaction_generator.create_transaction(
        sending_account=social_accounting.account.id,
        receiving_account=company.raw_material_account,
        amount_sent=Decimal(10),
        amount_received=Decimal(8.5),
    )

    response = show_a_account_details(company.id)
    assert len(response.transactions) == 0


@injection_test
def test_that_correct_info_is_generated_when_credit_for_wages_is_granted(
    show_a_account_details: ShowAAccountDetailsUseCase,
    company_generator: CompanyGenerator,
    transaction_generator: TransactionGenerator,
    social_accounting: SocialAccounting,
):
    company = company_generator.create_company_entity()

    transaction_generator.create_transaction(
        sending_account=social_accounting.account.id,
        receiving_account=company.work_account,
        amount_sent=Decimal(10),
        amount_received=Decimal(8.5),
    )

    response = show_a_account_details(company.id)
    assert len(response.transactions) == 1
    assert response.transactions[0].transaction_volume == Decimal(8.5)
    assert response.transactions[0].purpose is not None
    assert isinstance(response.transactions[0].date, datetime)
    assert (
        response.transactions[0].transaction_type == TransactionTypes.credit_for_wages
    )
    assert response.account_balance == Decimal(8.5)


@injection_test
def test_that_correct_info_is_generated_after_company_transfering_work_certificates(
    show_a_account_details: ShowAAccountDetailsUseCase,
    company_generator: CompanyGenerator,
    member_generator: MemberGenerator,
    transaction_generator: TransactionGenerator,
):
    company1 = company_generator.create_company_entity()
    member = member_generator.create_member_entity()

    trans = transaction_generator.create_transaction(
        sending_account=company1.work_account,
        receiving_account=member.account,
        amount_sent=Decimal(10),
        amount_received=Decimal(8.5),
    )

    response = show_a_account_details(company1.id)
    transaction = response.transactions[0]
    assert transaction.transaction_type == TransactionTypes.payment_of_wages
    assert transaction.transaction_volume == -trans.amount_sent
    assert response.account_balance == -trans.amount_sent


@injection_test
def test_that_plotting_info_is_empty_when_no_transactions_occurred(
    show_a_account_details: ShowAAccountDetailsUseCase,
    member_generator: MemberGenerator,
    company_generator: CompanyGenerator,
):
    member_generator.create_member_entity()
    company = company_generator.create_company_entity()

    response = show_a_account_details(company.id)
    assert not response.plot.timestamps
    assert not response.plot.accumulated_volumes


@injection_test
def test_that_plotting_info_is_generated_after_transfer_of_work_certificates(
    show_a_account_details: ShowAAccountDetailsUseCase,
    company_generator: CompanyGenerator,
    member_generator: MemberGenerator,
    transaction_generator: TransactionGenerator,
):
    worker = member_generator.create_member_entity()
    own_company = company_generator.create_company_entity(workers=[worker])

    transaction_generator.create_transaction(
        sending_account=own_company.work_account,
        receiving_account=worker.account,
        amount_sent=Decimal(10),
        amount_received=Decimal(8.5),
    )

    response = show_a_account_details(own_company.id)
    assert response.plot.timestamps
    assert response.plot.accumulated_volumes


@injection_test
def test_that_correct_plotting_info_is_generated_after_transferring_of_work_certs_to_two_workers(
    show_a_account_details: ShowAAccountDetailsUseCase,
    company_generator: CompanyGenerator,
    member_generator: MemberGenerator,
    transaction_generator: TransactionGenerator,
):
    worker1 = member_generator.create_member_entity()
    worker2 = member_generator.create_member_entity()
    own_company = company_generator.create_company_entity(workers=[worker1, worker2])

    trans1 = transaction_generator.create_transaction(
        sending_account=own_company.work_account,
        receiving_account=worker1.account,
        amount_sent=Decimal(10),
        amount_received=Decimal(5),
    )

    trans2 = transaction_generator.create_transaction(
        sending_account=own_company.work_account,
        receiving_account=worker2.account,
        amount_sent=Decimal(10),
        amount_received=Decimal(10),
    )

    response = show_a_account_details(own_company.id)
    assert len(response.plot.timestamps) == 2
    assert len(response.plot.accumulated_volumes) == 2

    assert trans1.date in response.plot.timestamps
    assert trans2.date in response.plot.timestamps

    assert trans1.amount_sent * (-1) in response.plot.accumulated_volumes
    assert (
        trans1.amount_sent * (-1) + trans2.amount_sent * (-1)
    ) in response.plot.accumulated_volumes


@injection_test
def test_that_plotting_info_is_generated_in_the_correct_order_after_transfer_of_certs_to_three_workers(
    show_a_account_details: ShowAAccountDetailsUseCase,
    company_generator: CompanyGenerator,
    member_generator: MemberGenerator,
    transaction_generator: TransactionGenerator,
):
    worker1 = member_generator.create_member_entity()
    worker2 = member_generator.create_member_entity()
    worker3 = member_generator.create_member_entity()
    own_company = company_generator.create_company_entity(
        workers=[worker1, worker2, worker3]
    )

    trans1 = transaction_generator.create_transaction(
        sending_account=own_company.work_account,
        receiving_account=worker1.account,
        amount_sent=Decimal(10),
        amount_received=Decimal(1),
    )

    trans2 = transaction_generator.create_transaction(
        sending_account=own_company.work_account,
        receiving_account=worker2.account,
        amount_sent=Decimal(10),
        amount_received=Decimal(2),
    )

    trans3 = transaction_generator.create_transaction(
        sending_account=own_company.work_account,
        receiving_account=worker3.account,
        amount_sent=Decimal(10),
        amount_received=Decimal(3),
    )

    response = show_a_account_details(own_company.id)
    assert response.plot.timestamps[0] == trans1.date
    assert response.plot.timestamps[2] == trans3.date

    assert response.plot.accumulated_volumes[0] == trans1.amount_sent * (-1)
    assert response.plot.accumulated_volumes[2] == (
        trans1.amount_sent * (-1)
        + trans2.amount_sent * (-1)
        + trans3.amount_sent * (-1)
    )


@injection_test
def test_that_correct_plotting_info_is_generated_after_receiving_of_work_certificates_from_social_accounting(
    show_a_account_details: ShowAAccountDetailsUseCase,
    company_generator: CompanyGenerator,
    transaction_generator: TransactionGenerator,
    social_accounting: SocialAccounting,
):
    company = company_generator.create_company_entity()
    trans = transaction_generator.create_transaction(
        sending_account=social_accounting.account.id,
        receiving_account=company.work_account,
        amount_sent=Decimal(10),
        amount_received=Decimal(8.5),
    )

    response = show_a_account_details(company.id)
    assert response.plot.timestamps
    assert response.plot.accumulated_volumes

    assert len(response.plot.timestamps) == 1
    assert len(response.plot.accumulated_volumes) == 1

    assert trans.date in response.plot.timestamps
    assert trans.amount_received in response.plot.accumulated_volumes

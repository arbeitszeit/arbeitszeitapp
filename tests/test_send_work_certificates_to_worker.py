import pytest
from arbeitszeit.use_cases import send_work_certificates_to_worker
from arbeitszeit.entities import AccountTypes
from tests.dependency_injection import injection_test
from tests.repositories import CompanyWorkerRepository, TransactionRepository
from tests.data_generators import CompanyGenerator, MemberGenerator
from arbeitszeit.errors import WorkerDoesNotExist, WorkerNotAtCompany


@injection_test
def test_that_after_transfer_balances_of_worker_and_company_are_correct(
    company_worker_repository: CompanyWorkerRepository,
    transaction_repository: TransactionRepository,
    company_generator: CompanyGenerator,
    member_generator: MemberGenerator,
):
    company = company_generator.create_company()
    worker = member_generator.create_member()
    company_worker_repository.add_worker_to_company(company, worker)
    amount_to_transfer = 50
    send_work_certificates_to_worker(
        company_worker_repository,
        transaction_repository,
        company,
        worker,
        amount_to_transfer,
    )
    assert company.work_account.balance == -amount_to_transfer
    assert worker.account.balance == amount_to_transfer


@injection_test
def test_that_error_is_raised_if_money_is_sent_to_nonexisting_worker(
    company_worker_repository: CompanyWorkerRepository,
    transaction_repository: TransactionRepository,
    company_generator: CompanyGenerator,
):
    company = company_generator.create_company()
    worker = None
    amount_to_transfer = 50
    with pytest.raises(WorkerDoesNotExist):
        send_work_certificates_to_worker(
            company_worker_repository,
            transaction_repository,
            company,
            worker,
            amount_to_transfer,
        )


@injection_test
def test_that_error_is_raised_if_money_is_sent_to_worker_not_working_in_company(
    company_worker_repository: CompanyWorkerRepository,
    transaction_repository: TransactionRepository,
    company_generator: CompanyGenerator,
    member_generator: MemberGenerator,
):
    company = company_generator.create_company()
    worker1 = member_generator.create_member()
    company_worker_repository.add_worker_to_company(company, worker1)
    worker2 = member_generator.create_member()
    amount_to_transfer = 50
    with pytest.raises(WorkerNotAtCompany):
        send_work_certificates_to_worker(
            company_worker_repository,
            transaction_repository,
            company,
            worker2,
            amount_to_transfer,
        )


@injection_test
def test_that_after_transfer_one_transaction_is_added(
    company_worker_repository: CompanyWorkerRepository,
    transaction_repository: TransactionRepository,
    company_generator: CompanyGenerator,
    member_generator: MemberGenerator,
):
    company = company_generator.create_company()
    worker = member_generator.create_member()
    company_worker_repository.add_worker_to_company(company, worker)
    amount_to_transfer = 50
    send_work_certificates_to_worker(
        company_worker_repository,
        transaction_repository,
        company,
        worker,
        amount_to_transfer,
    )
    assert len(transaction_repository.transactions) == 1


@injection_test
def test_that_after_transfer_correct_transaction_is_added(
    company_worker_repository: CompanyWorkerRepository,
    transaction_repository: TransactionRepository,
    company_generator: CompanyGenerator,
    member_generator: MemberGenerator,
):
    company = company_generator.create_company()
    worker = member_generator.create_member()
    company_worker_repository.add_worker_to_company(company, worker)
    amount_to_transfer = 50
    send_work_certificates_to_worker(
        company_worker_repository,
        transaction_repository,
        company,
        worker,
        amount_to_transfer,
    )
    transaction = transaction_repository.transactions[0]
    assert transaction.amount == amount_to_transfer
    assert transaction.account_from.account_type == AccountTypes.a
    assert transaction.account_to.account_type == AccountTypes.member

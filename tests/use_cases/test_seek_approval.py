from datetime import datetime

from arbeitszeit.use_cases import SeekApproval
from tests.data_generators import PlanGenerator
from tests.datetime_service import FakeDatetimeService

from .dependency_injection import injection_test


@injection_test
def test_that_any_plan_will_be_approved(
    plan_generator: PlanGenerator,
    seek_approval: SeekApproval,
):
    new_plan = plan_generator.create_plan()
    approval_response = seek_approval(new_plan.id)
    assert approval_response.is_approved


@injection_test
def test_that_true_is_returned(
    plan_generator: PlanGenerator,
    seek_approval: SeekApproval,
):
    new_plan = plan_generator.create_plan()
    approval_response = seek_approval(new_plan.id)
    assert approval_response.is_approved is True


@injection_test
def test_that_approval_date_has_correct_day_of_month(
    plan_generator: PlanGenerator,
    seek_approval: SeekApproval,
    datetime_service: FakeDatetimeService,
):
    datetime_service.freeze_time(datetime(year=2021, month=5, day=3))
    new_plan = plan_generator.create_plan()
    seek_approval(new_plan.id)
    assert new_plan.approval_date
    assert 3 == new_plan.approval_date.day

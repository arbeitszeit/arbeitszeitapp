from datetime import datetime, timedelta

from arbeitszeit.use_cases.query_private_consumptions import QueryPrivateConsumptions
from tests.use_cases.base_test_case import BaseTestCase


class TestQueryPrivateConsumptions(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.query_consumptions = self.injector.get(QueryPrivateConsumptions)
        self.control_thresholds.set_allowed_overdraw_of_member_account(10000)

    def test_that_no_consumption_is_returned_when_searching_an_empty_repo(self) -> None:
        member = self.member_generator.create_member()
        results = list(self.query_consumptions(member))
        assert not results

    def test_that_correct_consumptions_are_returned(self) -> None:
        expected_plan = self.plan_generator.create_plan().id
        member = self.member_generator.create_member()
        self.purchase_generator.create_private_consumption(
            consumer=member, plan=expected_plan
        )
        results = list(self.query_consumptions(member))
        assert len(results) == 1
        assert results[0].plan_id == expected_plan

    def test_that_consumptions_are_returned_in_correct_order(self) -> None:
        self.datetime_service.freeze_time(datetime(2000, 1, 1))
        first_plan = self.plan_generator.create_plan().id
        second_plan = self.plan_generator.create_plan().id
        member = self.member_generator.create_member()
        self.purchase_generator.create_private_consumption(
            consumer=member, plan=first_plan
        )
        self.datetime_service.advance_time(timedelta(days=1))
        self.purchase_generator.create_private_consumption(
            consumer=member, plan=second_plan
        )
        results = list(self.query_consumptions(member))
        assert results[0].plan_id == second_plan
        assert results[1].plan_id == first_plan

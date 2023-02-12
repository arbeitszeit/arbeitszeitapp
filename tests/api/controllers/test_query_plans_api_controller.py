from arbeitszeit.use_cases.query_plans import PlanFilter, PlanSorting
from arbeitszeit_web.api_controllers.query_plans_api_controller import (
    QueryPlansApiController,
)
from tests.controllers.base_test_case import BaseTestCase
from tests.request import FakeRequest


class ControllerTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.controller = self.injector.get(QueryPlansApiController)
        self.request = self.injector.get(FakeRequest)

    def test_that_by_default_a_request_gets_returned_which_sorts_by_activation(self):
        use_case_request = self.controller.get_request(self.request)
        self.assertEqual(use_case_request.sorting_category, PlanSorting.by_activation)

    def test_that_by_default_a_request_gets_returned_which_filters_by_plan_id(self):
        use_case_request = self.controller.get_request(self.request)
        self.assertEqual(use_case_request.filter_category, PlanFilter.by_plan_id)

    def test_that_by_default_a_request_gets_returned_without_query_string(self):
        use_case_request = self.controller.get_request(self.request)
        self.assertIsNone(use_case_request.query_string)

    def test_that_by_default_a_use_case_request_with_offset_0_gets_returned_if_offset_query_string_was_empty(
        self,
    ):
        assert not self.request.query_string().get("offset")
        use_case_request = self.controller.get_request(self.request)
        self.assertEqual(use_case_request.offset, 0)

    def test_that_by_default_a_use_case_request_with_limit_30_gets_returned_if_limit_query_string_was_empty(
        self,
    ):
        assert not self.request.query_string().get("limit")
        use_case_request = self.controller.get_request(self.request)
        self.assertEqual(use_case_request.limit, 30)

    def test_correct_offset_gets_returned_if_it_was_set_in_query_string(self):
        expected_offset = 8
        self.request.set_arg(arg="offset", value=str(expected_offset))
        use_case_request = self.controller.get_request(self.request)
        self.assertEqual(use_case_request.offset, expected_offset)

    def test_correct_limit_gets_returned_if_it_was_set_in_query_string(self):
        expected_limit = 7
        self.request.set_arg(arg="limit", value=str(expected_limit))
        use_case_request = self.controller.get_request(self.request)
        self.assertEqual(use_case_request.limit, expected_limit)

    def test_both_correct_limit_and_offset_get_returned_if_specified_in_query_string(
        self,
    ):
        expected_limit = 7
        self.request.set_arg(arg="limit", value=str(expected_limit))
        expected_offset = 8
        self.request.set_arg(arg="offset", value=str(expected_offset))
        use_case_request = self.controller.get_request(self.request)
        self.assertEqual(use_case_request.limit, expected_limit)
        self.assertEqual(use_case_request.offset, expected_offset)

    def test_controller_raises_value_error_if_offset_query_string_has_letters(self):
        self.request.set_arg(arg="offset", value="123abc")
        with self.assertRaises(ValueError):
            self.controller.get_request(self.request)

    def test_controller_raises_value_error_if_offset_query_string_is_negative_number(
        self,
    ):
        self.request.set_arg(arg="offset", value="-123")
        with self.assertRaises(ValueError):
            self.controller.get_request(self.request)

    def test_controller_raises_value_error_if_limit_query_string_has_letters(self):
        self.request.set_arg(arg="limit", value="123abc")
        with self.assertRaises(ValueError):
            self.controller.get_request(self.request)

    def test_controller_raises_value_error_if_limit_query_string_is_negative_number(
        self,
    ):
        self.request.set_arg(arg="limit", value="-123")
        with self.assertRaises(ValueError):
            self.controller.get_request(self.request)


class ExpectedInputsTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.controller = self.injector.get(QueryPlansApiController)
        self.inputs = self.controller.get_expected_inputs()

    def test_controller_has_two_expected_inputs(self):
        self.assertEqual(len(self.inputs), 2)

    def test_first_expected_input_is_offset(self):
        input = self.inputs[0]
        self.assertEqual(input.name, "offset")

    def test_input_offset_has_correct_parameters(self):
        input = self.inputs[0]
        self.assertEqual(input.name, "offset")
        self.assertEqual(input.type, str)
        self.assertEqual(input.description, "The query offset.")
        self.assertEqual(input.default, 0)

    def test_second_expected_input_is_limit(self):
        input = self.inputs[1]
        self.assertEqual(input.name, "limit")

    def test_input_limit_has_correct_parameters(self):
        input = self.inputs[1]
        self.assertEqual(input.name, "limit")
        self.assertEqual(input.type, str)
        self.assertEqual(input.description, "The query limit.")
        self.assertEqual(input.default, 30)

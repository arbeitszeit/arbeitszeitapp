from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from arbeitszeit.entities import PayoutFactor
from arbeitszeit.use_cases.get_statistics import StatisticsResponse
from arbeitszeit_web.presenters.get_statistics_presenter import GetStatisticsPresenter
from tests.datetime_service import FakeDatetimeService

from ..translator import FakeTranslator
from .dependency_injection import get_dependency_injector

TESTING_RESPONSE_MODEL = StatisticsResponse(
    registered_companies_count=5,
    registered_members_count=30,
    cooperations_count=10,
    certificates_count=Decimal("50"),
    available_product=Decimal("20.5"),
    active_plans_count=6,
    active_plans_public_count=2,
    avg_timeframe=Decimal("30.5"),
    planned_work=Decimal("500.23"),
    planned_resources=Decimal("400.1"),
    planned_means=Decimal("215.23"),
    payout_factor=PayoutFactor(
        calculation_date=datetime(2020, 1, 1, 10), value=Decimal("0.74516")
    ),
)


class GetStatisticsPresenterTests(TestCase):
    def setUp(self) -> None:
        self.injector = get_dependency_injector()
        self.datetime_service = self.injector.get(FakeDatetimeService)
        self.translator = self.injector.get(FakeTranslator)
        self.presenter = self.injector.get(GetStatisticsPresenter)

    def test_planned_resources_hours_are_truncated_at_2_digits_after_comma(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            planned_resources=Decimal(400.13131313),
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.planned_resources_hours,
            self.translator.gettext("%.2f hours") % Decimal("400.13"),
        )

    def test_planned_work_hours_are_truncated_at_2_digits_after_comma(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            planned_work=Decimal(523.12123123123),
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.planned_work_hours,
            self.translator.gettext("%.2f hours") % Decimal("523.12"),
        )

    def test_planned_means_hours_are_truncated_at_2_digits_after_comma(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            planned_means=Decimal(123.12315),
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.planned_means_hours,
            self.translator.gettext("%s hours") % Decimal("123.12"),
        )

    def test_registered_companies_count_is_displayed_correctly_as_number(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            registered_companies_count=6,
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.registered_companies_count,
            "6",
        )

    def test_registered_members_count_is_displayed_correctly_as_number(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            registered_members_count=32,
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.registered_members_count,
            "32",
        )

    def test_coop_count_is_displayed_correctly_as_number(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            cooperations_count=11,
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.cooperations_count,
            "11",
        )

    def test_certificates_count_is_displayed_correctly_as_number(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            certificates_count=Decimal(50.5),
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.certificates_count,
            "50.50",
        )

    def test_available_prdocut_is_displayed_correctly_as_number(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            available_product=Decimal(2.504),
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.available_product,
            "2.50",
        )

    def test_active_plans_count_is_displayed_correctly_as_number(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            active_plans_count=7,
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.active_plans_count,
            "7",
        )

    def test_active_plans_public_count_is_displayed_correctly_as_number(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            active_plans_public_count=2,
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.active_plans_public_count,
            "2",
        )

    def test_average_timeframe_days_are_truncated_at_2_digits_after_comma(self):
        response = replace(
            TESTING_RESPONSE_MODEL,
            avg_timeframe=Decimal(31.2125321),
        )
        view_model = self.presenter.present(response)
        self.assertEqual(
            view_model.average_timeframe_days,
            self.translator.gettext("%.2f days") % 31.21,
        )

    def test_that_plot_url_for_certificates_with_correct_args_is_returned(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertIn(
            str(TESTING_RESPONSE_MODEL.certificates_count),
            view_model.barplot_for_certificates_url,
        )
        self.assertIn(
            str(TESTING_RESPONSE_MODEL.available_product),
            view_model.barplot_for_certificates_url,
        )

    def test_that_plot_url_for_means_of_productions_with_correct_args_is_returned(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertIn(
            str(TESTING_RESPONSE_MODEL.planned_means),
            view_model.barplot_means_of_production_url,
        )
        self.assertIn(
            str(TESTING_RESPONSE_MODEL.planned_resources),
            view_model.barplot_means_of_production_url,
        )
        self.assertIn(
            str(TESTING_RESPONSE_MODEL.planned_work),
            view_model.barplot_means_of_production_url,
        )

    def test_that_plot_url_for_plans_with_correct_args_is_returned(self):
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertIn(
            str(
                TESTING_RESPONSE_MODEL.active_plans_count
                - TESTING_RESPONSE_MODEL.active_plans_public_count
            ),
            view_model.barplot_plans_url,
        )
        self.assertIn(
            str(TESTING_RESPONSE_MODEL.active_plans_public_count),
            view_model.barplot_plans_url,
        )

    def test_that_payout_factor_is_correctly_shown_when_it_exists(self):
        assert TESTING_RESPONSE_MODEL.payout_factor is not None
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.payout_factor,
            round(TESTING_RESPONSE_MODEL.payout_factor.value, 2).__str__(),
        )

    def test_that_correct_message_is_shown_when_payout_factor_does_not_exist(self):
        uc_response = replace(TESTING_RESPONSE_MODEL, payout_factor=None)
        view_model = self.presenter.present(uc_response)
        self.assertEqual(
            view_model.payout_factor,
            self.translator.gettext("Not found."),
        )

    def test_that_payout_factor_explanation_is_correctly_shown_when_payout_factor_exists(
        self,
    ):
        assert TESTING_RESPONSE_MODEL.payout_factor is not None
        expected_timestamp = self.datetime_service.format_datetime(
            TESTING_RESPONSE_MODEL.payout_factor.calculation_date,
            zone="Europe/Berlin",
            fmt="%d.%m.%Y %H:%M",
        )
        view_model = self.presenter.present(TESTING_RESPONSE_MODEL)
        self.assertEqual(
            view_model.payout_factor_explanation,
            self.translator.gettext("Payout factor (%(timestamp)s)")
            % dict(timestamp=expected_timestamp),
        )

    def test_that_correct_payout_factor_explanation_is_shown_when_payout_factor_does_not_exist(
        self,
    ):
        uc_response = replace(TESTING_RESPONSE_MODEL, payout_factor=None)
        view_model = self.presenter.present(uc_response)
        self.assertEqual(
            view_model.payout_factor_explanation,
            self.translator.gettext("Not found."),
        )

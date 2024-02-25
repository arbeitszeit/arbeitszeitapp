from datetime import datetime, timedelta
from functools import partial
from uuid import uuid4

from arbeitszeit import records
from tests.data_generators import EmailGenerator
from tests.datetime_service import FakeDatetimeService

from ..flask import FlaskTestCase


class PasswordResetRequestResultTests(FlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.email_generator = self.injector.get(EmailGenerator)
        self.datetime_service = self.injector.get(FakeDatetimeService)

    def _generateResetToken(self) -> str:
        return str(uuid4())

    def _record_has_expected_email(
        self, expected_email: str, record: records.PasswordResetRequest
    ) -> bool:
        return record.email_address == expected_email

    def test_querying_password_reset_request_by_email(self) -> None:
        email_address = self.email_generator.get_random_email()
        reset_token = self._generateResetToken()

        self.database_gateway.create_email_address(
            address=email_address,
            confirmed_on=self.datetime_service.now_minus_ten_days(),
        )
        self.database_gateway.create_password_reset_request(
            email_address=email_address,
            reset_token=reset_token,
            created_at=self.datetime_service.now(),
        )

        result_records = list(
            self.database_gateway.get_password_reset_requests().with_email_address(
                email_address
            )
        )
        assert len(result_records) == 1
        assert result_records[0].reset_token == str(reset_token)
        assert all(
            map(partial(self._record_has_expected_email, email_address), result_records)
        )

    def test_multiple_password_reset_requests_can_exist_for_given_email(self) -> None:
        email_address = self.email_generator.get_random_email()
        self.database_gateway.create_email_address(
            address=email_address,
            confirmed_on=self.datetime_service.now_minus_ten_days(),
        )
        self.database_gateway.create_password_reset_request(
            email_address=email_address,
            reset_token=self._generateResetToken(),
            created_at=self.datetime_service.now(),
        )
        self.database_gateway.create_password_reset_request(
            email_address=email_address,
            reset_token=self._generateResetToken(),
            created_at=self.datetime_service.now(),
        )
        self.database_gateway.create_password_reset_request(
            email_address=email_address,
            reset_token=self._generateResetToken(),
            created_at=self.datetime_service.now(),
        )

        result_records = list(
            self.database_gateway.get_password_reset_requests().with_email_address(
                email_address
            )
        )
        assert len(result_records) == 3
        assert all(
            map(partial(self._record_has_expected_email, email_address), result_records)
        )

    def test_querying_password_reset_requests_after_datetime_threshold(self) -> None:
        email_address = self.email_generator.get_random_email()
        self.database_gateway.create_email_address(
            address=email_address,
            confirmed_on=self.datetime_service.now_minus_ten_days(),
        )
        self.datetime_service.freeze_time(datetime(2021, 2, 13, hour=10))

        self.database_gateway.create_password_reset_request(
            email_address=email_address,
            reset_token=self._generateResetToken(),
            created_at=self.datetime_service.now(),
        )

        self.datetime_service.advance_time(timedelta(hours=1))
        self.database_gateway.create_password_reset_request(
            email_address=email_address,
            reset_token=self._generateResetToken(),
            created_at=self.datetime_service.now(),
        )

        self.datetime_service.advance_time(timedelta(minutes=1))
        self.database_gateway.create_password_reset_request(
            email_address=email_address,
            reset_token=self._generateResetToken(),
            created_at=self.datetime_service.now(),
        )

        self.datetime_service.advance_time(timedelta(minutes=1))
        self.database_gateway.create_password_reset_request(
            email_address=email_address,
            reset_token=self._generateResetToken(),
            created_at=self.datetime_service.now(),
        )

        result_records = list(
            self.database_gateway.get_password_reset_requests()
            .with_email_address(email_address)
            .with_creation_date_after(
                self.datetime_service.now() - timedelta(minutes=30)
            )
        )

        assert len(result_records) == 3
        assert all(
            map(partial(self._record_has_expected_email, email_address), result_records)
        )

import click
from flask_babel import force_locale

from arbeitszeit.use_cases.send_accountant_registration_token import (
    SendAccountantRegistrationTokenUseCase,
)
from arbeitszeit.use_cases.update_plans_and_payout import UpdatePlansAndPayout
from arbeitszeit_flask.database import commit_changes
from arbeitszeit_flask.dependency_injection import with_injection


@commit_changes
@with_injection()
def update_and_payout(
    payout: UpdatePlansAndPayout,
) -> None:
    """
    Run every hour on production server or call manually from CLI `flask payout`.
    """
    payout()


@click.argument("email_address")
@commit_changes
@with_injection()
def invite_accountant(
    email_address: str, use_case: SendAccountantRegistrationTokenUseCase
) -> None:
    with force_locale("de"):
        use_case.send_accountant_registration_token(
            SendAccountantRegistrationTokenUseCase.Request(email=email_address)
        )

from dataclasses import dataclass

from arbeitszeit.use_cases.log_in_member import LogInMemberUseCase
from arbeitszeit_web.api_presenters.interfaces import JsonBoolean, JsonDict, JsonValue
from arbeitszeit_web.api_presenters.response_errors import Unauthorized
from arbeitszeit_web.session import Session


@dataclass
class LoginMemberApiPresenter:
    @dataclass
    class ViewModel:
        success: bool

    @classmethod
    def get_schema(cls) -> JsonValue:
        return JsonDict(
            members=dict(success=JsonBoolean()),
            schema_name="LoginMemberResponse",
        )

    session: Session

    def create_view_model(self, response: LogInMemberUseCase.Response) -> ViewModel:
        if response.is_logged_in:
            assert response.user_id
            self.session.login_member(member=response.user_id, remember=False)
            return self.ViewModel(success=True)
        else:
            if (
                response.rejection_reason
                == LogInMemberUseCase.RejectionReason.unknown_email_address
            ):
                raise Unauthorized(message="Unknown email adress.")
            else:
                raise Unauthorized(message="Invalid password.")

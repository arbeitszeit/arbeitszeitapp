from dataclasses import dataclass

from arbeitszeit.use_cases.register_productive_consumption import (
    RegisterProductiveConsumptionResponse as UseCaseResponse,
)
from arbeitszeit_web.api.presenters.interfaces import JsonBoolean, JsonObject, JsonValue
from arbeitszeit_web.api.response_errors import Forbidden, NotFound


@dataclass
class LiquidMeansConsumptionPresenter:
    @dataclass
    class ViewModel:
        success: bool

    @classmethod
    def get_schema(cls) -> JsonValue:
        return JsonObject(
            members=dict(success=JsonBoolean()),
            name="LiquidMeansConsumptionResponse",
        )

    def create_view_model(self, response: UseCaseResponse) -> ViewModel:
        if not response.is_rejected:
            return self.ViewModel(success=True)
        match response.rejection_reason:
            case UseCaseResponse.RejectionReason.plan_not_found:
                raise NotFound(message="Plan does not exist.")
            case UseCaseResponse.RejectionReason.plan_is_not_active:
                raise NotFound(message="The specified plan has expired.")
            case UseCaseResponse.RejectionReason.cannot_consume_public_service:
                raise Forbidden(message="Companies cannot acquire public products.")
            case UseCaseResponse.RejectionReason.consumer_is_planner:
                raise Forbidden(message="Companies cannot acquire their own products.")
            case _:
                raise NotFound(message="Unknown error.")

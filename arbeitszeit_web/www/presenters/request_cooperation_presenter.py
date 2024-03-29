from dataclasses import dataclass
from typing import List

from arbeitszeit.use_cases.request_cooperation import RequestCooperationResponse
from arbeitszeit_web.translator import Translator


@dataclass
class RequestCooperationViewModel:
    notifications: List[str]
    is_error: bool


@dataclass
class RequestCooperationPresenter:
    translator: Translator

    def present(
        self, use_case_response: RequestCooperationResponse
    ) -> RequestCooperationViewModel:
        view_model = self._create_view_model(use_case_response)
        return view_model

    def _create_view_model(
        self, use_case_response: RequestCooperationResponse
    ) -> RequestCooperationViewModel:
        notifications = []
        if not use_case_response.is_rejected:
            is_error = False
            notifications.append(self.translator.gettext("Request has been sent."))
        else:
            is_error = True
            if (
                use_case_response.rejection_reason
                == RequestCooperationResponse.RejectionReason.plan_not_found
            ):
                notifications.append(self.translator.gettext("Plan not found."))
            elif (
                use_case_response.rejection_reason
                == RequestCooperationResponse.RejectionReason.cooperation_not_found
            ):
                notifications.append(self.translator.gettext("Cooperation not found."))
            elif (
                use_case_response.rejection_reason
                == RequestCooperationResponse.RejectionReason.plan_inactive
            ):
                notifications.append(self.translator.gettext("Plan not active."))
            elif use_case_response.rejection_reason in (
                RequestCooperationResponse.RejectionReason.plan_has_cooperation,
                RequestCooperationResponse.RejectionReason.plan_is_already_requesting_cooperation,
            ):
                notifications.append(
                    self.translator.gettext(
                        "Plan is already cooperating or requested a cooperation."
                    )
                )
            elif (
                use_case_response.rejection_reason
                == RequestCooperationResponse.RejectionReason.plan_is_public_service
            ):
                notifications.append(
                    self.translator.gettext("Public plans cannot cooperate.")
                )
            elif (
                use_case_response.rejection_reason
                == RequestCooperationResponse.RejectionReason.requester_is_not_planner
            ):
                notifications.append(
                    self.translator.gettext(
                        "Only the creator of a plan can request a cooperation."
                    )
                )
        return RequestCooperationViewModel(
            notifications=notifications, is_error=is_error
        )

from typing import Dict, Protocol

from arbeitszeit.user_action import UserAction


class UserActionResolver(Protocol):
    def resolve_user_action_reference(self, action: UserAction) -> str:
        ...

    def resolve_user_action_name(self, action: UserAction) -> str:
        ...


class UserActionResolverImpl:
    def resolve_user_action_name(self, action: UserAction) -> str:
        user_action_to_label: Dict[UserAction, str] = {
            UserAction.answer_invite: "Betriebsbeitritt akzeptieren oder ablehnen",
            UserAction.answer_cooperation_request: "Kooperationsanfrage akzeptieren oder ablehnen",
        }
        return user_action_to_label[action]

    def resolve_user_action_reference(self, action: UserAction) -> str:
        # TODO: Implement proper resolving of user action hyperlinks
        return ""
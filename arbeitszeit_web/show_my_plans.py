from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

from arbeitszeit.use_cases.show_my_plans import ShowMyPlansResponse


@dataclass
class NonActivePlansRow:
    id: str
    prd_name: str
    description: str
    means_cost: str
    resource_cost: str
    labour_cost: str
    prd_amount: str
    price_per_unit: str
    type_of_plan: str
    plan_creation_date: str


@dataclass
class NonActivePlansTable:
    rows: List[NonActivePlansRow]


@dataclass
class ActivePlansRow:
    prd_name: str
    id: str
    description: str
    means_cost: str
    resource_cost: str
    labour_cost: str
    prd_amount: str
    price_per_unit: str
    type_of_plan: str
    activation_date: str
    expiration_date: str
    expiration_relative: str
    edit: str


@dataclass
class ActivePlansTable:
    title: str
    show: bool
    message: str
    headings: Dict[str, Dict[str, str]]
    rows: List[ActivePlansRow]
    sequence: Tuple[str]


@dataclass
class ExpiredPlansRow:
    id: str
    prd_name: str
    description: str
    means_cost: str
    resource_cost: str
    labour_cost: str
    prd_amount: str
    price_per_unit: str
    type_of_plan: str
    plan_creation_date: str
    renewed: bool


@dataclass
class ExpiredPlansTable:
    rows: List[ExpiredPlansRow]


@dataclass
class ShowMyPlansViewModel:
    notifications: List[str]
    show_non_active_plans: bool
    non_active_plans: NonActivePlansTable
    active_plans: ActivePlansTable
    show_expired_plans: bool
    expired_plans: ExpiredPlansTable

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


base_sequence = (
    "prd_name",
    "id",
    "description",
    "means_cost",
    "resource_cost",
    "labour_cost",
    "prd_amount",
    "price_per_unit",
    "type_of_plan",
)
base_plans_headings_de_DE = {
    "prd_name": {"text": "Produkt", "abbr": ""},
    "id": {"text": "Plan-ID", "abbr": ""},
    "description": {"text": "Beschr.", "abbr": ""},
    "means_cost": {"text": "p", "abbr": "Kosten Produktionsmittel"},
    "resource_cost": {"text": "r", "abbr": "Kosten Rohstoffe"},
    "labour_cost": {"text": "a", "abbr": "Kosten Arbeit"},
    "prd_amount": {"text": "Einh.", "abbr": "Einheiten"},
    "price_per_unit": {"text": "Stückpr.", "abbr": ""},
    "type_of_plan": {"text": "Art", "abbr": ""},
}

active_plans_title_de_DE = "Aktuelle Pläne"
active_plans_title = active_plans_title_de_DE
active_plans_message_de_DE = "Du hast keine aktiven Pläne."
active_plans_message = active_plans_message_de_DE
active_plans_addon_headings_de_DE = {
    "activation_date": {"text": "Plan aktiv seit", "abbr": ""},
    "expiration_date": {"text": "Plan-Ende", "abbr": ""},
    "expiration_relative": {"text": "Endet in", "abbr": ""},
    "edit": {
        "text": "Anb.",
        "abbr": "Produkt im Marketplace anbieten",
    },
}
active_plans_headings_de_DE = {
    **base_plans_headings_de_DE,
    **active_plans_addon_headings_de_DE,
}
active_plans_headings = active_plans_headings_de_DE
active_plans_sequence_addon = (
    "activation_date",
    "expiration_date",
    "expiration_relative",
    "edit",
)
active_plans_sequence = (*base_sequence, *active_plans_sequence_addon)


class ShowMyPlansPresenter:
    def present(self, response: ShowMyPlansResponse) -> ShowMyPlansViewModel:

        if not response.all_plans:
            notifications = ["Du hast keine Pläne."]
        else:
            notifications = []

        return ShowMyPlansViewModel(
            notifications=notifications,
            show_non_active_plans=bool(response.non_active_plans),
            non_active_plans=NonActivePlansTable(
                rows=[
                    NonActivePlansRow(
                        id=f"{plan.id}",
                        prd_name=f"{plan.prd_name}",
                        description=f"{plan.description}",
                        means_cost=f"{plan.means_cost}",
                        resource_cost=f"{plan.resource_cost}",
                        labour_cost=f"{plan.labour_cost}",
                        prd_amount=f"{plan.prd_amount}",
                        price_per_unit=f"{plan.price_per_unit} Std.",
                        type_of_plan=self.__get_type_of_plan(plan.is_public_service),
                        plan_creation_date=self.__format_date(plan.plan_creation_date),
                    )
                    for plan in response.non_active_plans
                ],
            ),
            active_plans=ActivePlansTable(
                headings=active_plans_headings,
                message=active_plans_message,
                rows=[
                    ActivePlansRow(
                        prd_name=self.__to_str(plan.prd_name),
                        id=self.__to_str(plan.id),
                        description=self.__to_str(plan.description),
                        means_cost=self.__to_str(plan.means_cost),
                        resource_cost=self.__to_str(plan.resource_cost),
                        labour_cost=self.__to_str(plan.labour_cost),
                        prd_amount=self.__to_str(plan.prd_amount),
                        price_per_unit=self.__to_str(
                            plan.price_per_unit, suffix=" Std."
                        ),
                        type_of_plan=self.__get_type_of_plan(plan.is_public_service),
                        activation_date=self.__format_date(plan.activation_date),
                        expiration_date=self.__format_date(plan.expiration_date),
                        expiration_relative=self.__to_str(
                            plan.expiration_relative, suffix="d"
                        ),
                        edit="CREATE",
                    )
                    for plan in response.active_plans
                ],
                sequence=active_plans_sequence,
                show=bool(response.active_plans),
                title=active_plans_title,
            ),
            show_expired_plans=bool(response.expired_plans),
            expired_plans=ExpiredPlansTable(
                rows=[
                    ExpiredPlansRow(
                        id=f"{plan.id}",
                        prd_name=f"{plan.prd_name}",
                        description=f"{plan.description}",
                        means_cost=f"{plan.means_cost}",
                        resource_cost=f"{plan.resource_cost}",
                        labour_cost=f"{plan.labour_cost}",
                        prd_amount=f"{plan.prd_amount}",
                        price_per_unit=f"{plan.price_per_unit} Std.",
                        type_of_plan=self.__get_type_of_plan(plan.is_public_service),
                        plan_creation_date=self.__format_date(plan.plan_creation_date),
                        renewed=plan.renewed,
                    )
                    for plan in response.expired_plans
                ],
            ),
        )

    @staticmethod
    def __to_str(value, prefix="", suffix="") -> str:
        return f"{prefix}{value}{suffix}"

    @staticmethod
    def __get_type_of_plan(is_public_service: bool) -> str:
        return "Öffentlich" if is_public_service else "Produktiv"

    @staticmethod
    def __format_date(date: Optional[datetime]) -> str:
        return f"{date.strftime('%d.%m.%y')}" if date else "–"

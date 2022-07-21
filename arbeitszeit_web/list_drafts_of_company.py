from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from arbeitszeit.use_cases import ListDraftsResponse
from arbeitszeit_web.url_index import DraftUrlIndex


@dataclass
class ResultTableRow:
    id: str
    creation_date: str
    product_name: str
    description: List[str]
    details_url: str


@dataclass
class ResultsTable:
    rows: List[ResultTableRow]


@dataclass
class ListDraftsViewModel:
    results: ResultsTable
    show_results: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ListDraftsPresenter:
    draft_url_index: DraftUrlIndex

    def present(self, response: ListDraftsResponse) -> ListDraftsViewModel:
        show_results = bool(response.results)
        results = ResultsTable(
            rows=[
                ResultTableRow(
                    id=str(result.id),
                    creation_date=self.__format_date(result.creation_date),
                    product_name=result.product_name,
                    description=result.description.splitlines(),
                    details_url=self.draft_url_index.get_draft_summary_url(result.id),
                )
                for result in response.results
            ]
        )
        return ListDraftsViewModel(results=results, show_results=show_results)

    def __format_date(self, date: Optional[datetime]) -> str:
        return f"{date.strftime('%d.%m.%y')}" if date else "–"

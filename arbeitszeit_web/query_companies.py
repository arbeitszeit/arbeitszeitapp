from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Protocol

from injector import inject

from arbeitszeit.use_cases.query_companies import (
    CompanyFilter,
    CompanyQueryResponse,
    QueryCompaniesRequest,
)
from arbeitszeit_web.session import Session
from arbeitszeit_web.translator import Translator
from arbeitszeit_web.url_index import UrlIndex

from .notification import Notifier


class QueryCompaniesFormData(Protocol):
    def get_query_string(self) -> str:
        ...

    def get_category_string(self) -> str:
        ...


@dataclass
class QueryCompaniesRequestImpl(QueryCompaniesRequest):
    query: Optional[str]
    filter_category: CompanyFilter

    def get_query_string(self) -> Optional[str]:
        return self.query

    def get_filter_category(self) -> CompanyFilter:
        return self.filter_category


class QueryCompaniesController:
    def import_form_data(
        self, form: Optional[QueryCompaniesFormData]
    ) -> QueryCompaniesRequest:
        if form is None:
            filter_category = CompanyFilter.by_name
            query = None
        else:
            query = form.get_query_string().strip() or None
            if form.get_category_string() == "Email":
                filter_category = CompanyFilter.by_email
            else:
                filter_category = CompanyFilter.by_name
        return QueryCompaniesRequestImpl(query=query, filter_category=filter_category)


@dataclass
class ResultTableRow:
    company_id: str
    company_name: str
    company_email: str
    company_summary_url: str


@dataclass
class ResultsTable:
    rows: List[ResultTableRow]


@dataclass
class QueryCompaniesViewModel:
    results: ResultsTable
    show_results: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@inject
@dataclass
class QueryCompaniesPresenter:
    user_notifier: Notifier
    url_index: UrlIndex
    translator: Translator
    session: Session

    def present(self, response: CompanyQueryResponse) -> QueryCompaniesViewModel:
        if not response.results:
            self.user_notifier.display_warning(self.translator.gettext("No results"))
        return QueryCompaniesViewModel(
            show_results=bool(response.results),
            results=ResultsTable(
                rows=[
                    ResultTableRow(
                        company_id=str(result.company_id),
                        company_name=result.company_name,
                        company_email=result.company_email,
                        company_summary_url=self.url_index.get_company_summary_url(
                            user_role=self.session.get_user_role(),
                            company_id=result.company_id,
                        ),
                    )
                    for result in response.results
                ],
            ),
        )

    def get_empty_view_model(self) -> QueryCompaniesViewModel:
        return QueryCompaniesViewModel(
            results=ResultsTable(rows=[]),
            show_results=False,
        )

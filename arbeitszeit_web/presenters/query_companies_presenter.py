from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from arbeitszeit.use_cases.query_companies import CompanyQueryResponse
from arbeitszeit_web.notification import Notifier
from arbeitszeit_web.pagination import DEFAULT_PAGE_SIZE, Pagination, Paginator
from arbeitszeit_web.request import Request
from arbeitszeit_web.session import Session, UserRole
from arbeitszeit_web.translator import Translator
from arbeitszeit_web.url_index import UrlIndex


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
    pagination: Pagination

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QueryCompaniesPresenter:
    user_notifier: Notifier
    url_index: UrlIndex
    translator: Translator
    session: Session

    def present(
        self, response: CompanyQueryResponse, request: Request
    ) -> QueryCompaniesViewModel:
        if not response.results:
            self.user_notifier.display_warning(self.translator.gettext("No results"))
        paginator = self._create_paginator(
            request,
            total_results=response.total_results,
            current_offset=response.request.get_offset() or 0,
        )
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
            pagination=Pagination(
                is_visible=paginator.page_count > 1,
                pages=paginator.get_pages(),
            ),
        )

    def get_empty_view_model(self) -> QueryCompaniesViewModel:
        return QueryCompaniesViewModel(
            results=ResultsTable(rows=[]),
            show_results=False,
            pagination=Pagination(is_visible=False, pages=[]),
        )

    def _create_paginator(
        self, request: Request, total_results: int, current_offset: int
    ) -> Paginator:
        return Paginator(
            base_url=self._get_pagination_base_url(),
            query_arguments=dict(request.query_string().items()),
            page_size=DEFAULT_PAGE_SIZE,
            total_results=total_results,
            current_offset=current_offset,
        )

    def _get_pagination_base_url(self) -> str:
        return (
            self.url_index.get_member_query_companies_url()
            if self.session.get_user_role() == UserRole.member
            else self.url_index.get_company_query_companies_url()
        )

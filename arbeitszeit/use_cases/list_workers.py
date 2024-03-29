from dataclasses import dataclass
from typing import List
from uuid import UUID

from arbeitszeit.records import EmailAddress, Member
from arbeitszeit.repositories import DatabaseGateway


@dataclass
class ListedWorker:
    id: UUID
    name: str
    email: str


@dataclass
class ListWorkersResponse:
    workers: List[ListedWorker]


@dataclass
class ListWorkersRequest:
    company: UUID


@dataclass
class ListWorkers:
    database: DatabaseGateway

    def __call__(self, request: ListWorkersRequest) -> ListWorkersResponse:
        if not self.database.get_companies().with_id(request.company):
            return ListWorkersResponse(workers=[])
        members = self.database.get_members().working_at_company(request.company)
        return ListWorkersResponse(
            workers=[
                self._create_worker_response_model(member, mail)
                for member, mail in members.joined_with_email_address()
            ]
        )

    def _create_worker_response_model(
        self, member: Member, email: EmailAddress
    ) -> ListedWorker:
        return ListedWorker(
            id=member.id,
            name=member.name,
            email=email.address,
        )

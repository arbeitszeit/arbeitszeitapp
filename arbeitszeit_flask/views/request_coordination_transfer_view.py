from dataclasses import dataclass
from uuid import UUID

from flask import Response, render_template

from arbeitszeit.use_cases.request_coordination_transfer import (
    RequestCoordinationTransferUseCase,
)
from arbeitszeit_flask import types
from arbeitszeit_flask.forms import RequestCoordinationTransferForm
from arbeitszeit_web.www.controllers.request_coordination_transfer_controller import (
    RequestCoordinationTransferController,
)
from arbeitszeit_web.www.navbar import NavbarItem
from arbeitszeit_web.www.presenters.request_coordination_transfer_presenter import (
    RequestCoordinationTransferPresenter,
)


@dataclass
class RequestCoordinationTransferView:
    presenter: RequestCoordinationTransferPresenter
    controller: RequestCoordinationTransferController
    use_case: RequestCoordinationTransferUseCase

    def respond_to_get(
        self, form: RequestCoordinationTransferForm, coop_id: UUID
    ) -> types.Response:
        navbar_items = self.presenter.create_navbar_items(coop_id=coop_id)
        return self._create_response(navbar_items=navbar_items, form=form, status=200)

    def respond_to_post(
        self, form: RequestCoordinationTransferForm, coop_id: UUID
    ) -> types.Response:
        navbar_items = self.presenter.create_navbar_items(coop_id=coop_id)
        if not form.validate():
            return self._create_response(
                navbar_items=navbar_items, form=form, status=400
            )
        uc_request = self.controller.import_form_data(form)
        if not uc_request:
            return self._create_response(
                navbar_items=navbar_items, form=form, status=400
            )
        else:
            uc_response = self.use_case.request_transfer(uc_request)
            self.presenter.present_use_case_response(uc_response)
            return self._create_response(
                navbar_items=navbar_items, form=form, status=200
            )

    def _create_response(
        self,
        form: RequestCoordinationTransferForm,
        navbar_items: list[NavbarItem],
        status: int,
    ) -> types.Response:
        return Response(
            render_template(
                "company/request_coordination_transfer.html",
                form=form,
                navbar_items=navbar_items,
            ),
            status=status,
        )

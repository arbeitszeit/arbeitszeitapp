from dataclasses import dataclass
from uuid import UUID

from arbeitszeit.use_cases.pay_consumer_product import PayConsumerProductRequest
from arbeitszeit_web.forms import PayConsumerProductForm
from arbeitszeit_web.translator import Translator


@dataclass
class PayConsumerProductController:
    class FormError(Exception):
        pass

    translator: Translator

    def import_form_data(
        self, current_user: UUID, form: PayConsumerProductForm
    ) -> PayConsumerProductRequest:
        try:
            plan_id = UUID(form.plan_id_field().get_value())
        except ValueError:
            form.plan_id_field().attach_error(
                self.translator.gettext("Plan ID is invalid.")
            )
            raise self.FormError()
        try:
            amount = int(form.amount_field().get_value())
            if amount <= 0:
                form.amount_field().attach_error(
                    self.translator.gettext("Must be a number larger than zero.")
                )
                raise self.FormError()
        except ValueError:
            form.amount_field().attach_error(
                self.translator.gettext("This is not an integer.")
            )
            raise self.FormError()
        return PayConsumerProductRequest(
            buyer=current_user, plan=plan_id, amount=amount
        )
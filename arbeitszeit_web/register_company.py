from typing import Protocol

from arbeitszeit.use_cases import RegisterCompanyRequest


class RegisterForm(Protocol):
    def get_email_string(self) -> str:
        ...

    def get_name_string(self) -> str:
        ...

    def get_password_string(self) -> str:
        ...


class RegisterCompanyController:
    def create_request(
        self,
        register_form: RegisterForm,
    ) -> RegisterCompanyRequest:
        return RegisterCompanyRequest(
            email=register_form.get_email_string(),
            name=register_form.get_name_string(),
            password=register_form.get_password_string(),
        )

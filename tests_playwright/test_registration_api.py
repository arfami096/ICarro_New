import allure
import pytest

API_URL = "https://ilcarro-backend.herokuapp.com/v1/user/registration/usernamepassword"


@pytest.mark.api
@pytest.mark.regression
@allure.epic("iCarro Platform")
@allure.feature("User Registration API")
@allure.story("Server-side Contract & Input Validation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("API: Регистрация с пробелами в username — проверка ответа 400 Bad Request")
@allure.description(
    """
    **Проверка серверного контракта эндпоинта /v1/user/registration/usernamepassword**

    Цель: Отправить POST-запрос с пробелами (`"   "`) в поле `username` напрямую в бэкенд, 
    минуя UI-валидацию, и убедиться, что сервер корректно отклоняет данные (статус 400).
    """
)
def test_api_registration_whitespace_username(page):
    payload = {
        "username": "   ",
        "password": "Password123!",
        "firstName": "John",
        "lastName": "Smith"
    }

    with allure.step("Подготовка и прикрепление JSON-пейлоада к отчету"):
        allure.attach(
            str(payload),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Отправка POST-запроса на ручку регистрации"):
        response = page.request.post(API_URL, data=payload)
        response_json = response.json()

        allure.attach(
            str(response_json),
            name="Response JSON Body",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step(f"Проверка статус-кода ответа (ожидается 400, получен {response.status})"):
        assert response.status == 400, (
            f"Ожидался статус 400 Bad Request, но сервер вернул {response.status}. "
            f"Тело ответа: {response_json}"
        )
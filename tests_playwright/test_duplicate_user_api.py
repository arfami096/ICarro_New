import allure
import pytest
from data.data_generator import UserGenerator

API_URL = "https://ilcarro-backend.herokuapp.com/v1/user/registration/usernamepassword"


@pytest.mark.api
@pytest.mark.regression
@allure.epic("iCarro Platform")
@allure.feature("User Registration API")
@allure.story("Duplicate Handling")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("API: Попытка повторной регистрации существующего пользователя (Duplicate)")
def test_api_registration_duplicate(page):
    user = UserGenerator.get_random_user()
    payload = {
        "username": user.email,
        "password": user.password,
        "firstName": user.name,
        "lastName": user.last_name,
    }

    with allure.step("Первичная регистрация пользователя"):
        first_response = page.request.post(API_URL, data=payload)
        assert first_response.status in [200, 201], f"Не удалось создать базового юзера: {first_response.status}"

    with allure.step("Попытка зарегистрировать дубликат с тем же username/email"):
        duplicate_response = page.request.post(API_URL, data=payload)
        response_json = duplicate_response.json()

        allure.attach(
            str(response_json),
            name="Duplicate Response JSON",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Проверка статус-кода для дубликата (ожидается 400 или 409)"):
        assert duplicate_response.status in [400, 409], (
            f"Ожидался код 400 или 409 при дубликате, но получен {duplicate_response.status}. "
            f"Тело: {response_json}"
        )
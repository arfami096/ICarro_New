import allure
from data.data_generator import UserGenerator

API_REG_URL = "https://ilcarro-backend.herokuapp.com/v1/user/registration/usernamepassword"
API_LOGIN_URL = "https://ilcarro-backend.herokuapp.com/v1/user/login/usernamepassword"


@allure.epic("iCarro Platform")
@allure.feature("User Registration & Verification")
@allure.story("Post-condition check")
@allure.title("API: Регистрация нового юзера с последующей проверкой авторизации (Post-condition)")
@allure.severity(allure.severity_level.BLOCKER)
def test_registration_and_immediate_login_check(page):
    user = UserGenerator.get_random_user()
    payload = {
        "username": user.email,
        "password": user.password,
        "firstName": user.name,
        "lastName": user.last_name,
    }

    with allure.step("1. Регистрируем нового пользователя через API"):
        reg_response = page.request.post(API_REG_URL, data=payload)
        assert reg_response.status in [200, 201], f"Ошибка регистрации: {reg_response.status}"

    with allure.step("2. Проверяем Post-condition: пытаемся залогиниться под созданным юзером"):
        login_payload = {
            "username": user.email,
            "password": user.password,
        }
        login_response = page.request.post(API_LOGIN_URL, data=login_payload)
        login_data = login_response.json()

        allure.attach(
            str(login_data),
            name="Login Response after Registration",
            attachment_type=allure.attachment_type.JSON
        )

        assert login_response.status == 200, (
            f"Не удалось авторизоваться под созданным пользователем! Статус: {login_response.status}"
        )
        assert "accessToken" in login_data or "token" in login_data, (
            "В ответе логина отсутствует токен авторизации!"
        )
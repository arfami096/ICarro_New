import pytest
import allure

API_URL = "https://ilcarro-backend.herokuapp.com/v1/user/registration/usernamepassword"


@allure.epic("API Compliance & Bug Tracking")
@allure.feature("Registration Validation Mismatches")
@allure.story("UI vs Backend Min Length Mismatch")
@allure.severity(allure.severity_level.NORMAL)
@allure.issue("BUG-UI-01", "UI says minimum 6 symbols, but backend requires 8")
@pytest.mark.parametrize("length", [6, 7])
def test_ui_backend_min_length_mismatch(page, length):
    """
    Проверка расхождения между UI и Backend по минимальной длине пароля:
    На UI отображается 'минимум 6 символов', но бэкенд возвращает 400 Bad Request,
    так как на самом деле требует минимум 8 символов.
    """
    with allure.step(f"Генерация пароля длиной {length} символов"):
        password = "Aa1!" + "a" * (length - 4)
        payload = {
            "username": f"test_min_mismatch_{length}_{hash(password)}@test.com",
            "password": password,
            "firstName": "John",
            "lastName": "Smith"
        }

    with allure.step("Отправка POST-запроса на регистрацию"):
        response = page.request.post(API_URL, data=payload)
        response_json = response.json() if response.status != 500 else response.text

    with allure.step(f"Проверка ответа бэкенда (сейчас ожидает 400 из-за бага, требуют 8 символов)"):
        # Если разработчики починят UI или Backend (сделают честные 6 символов),
        # этот ассерт упадет, и мы узнаем, что баг исправлен!
        assert response.status == 400, (
            f"Ожидался статус 400 (фактическое поведение бэкенда: требуется минимум 8 символов), "
            f"но пришел {response_json}. Возможно, баг BUG-UI-01 исправлен!"
        )


@allure.epic("API Compliance & Bug Tracking")
@allure.feature("Security & Input Constraints")
@allure.story("Missing Max Length Validation")
@allure.severity(allure.severity_level.MINOR)
@allure.issue("BUG-SEC-02", "Missing max length validation on password (accepts 500+ chars)")
def test_password_max_length_absence(page):
    """
    Проверка отсутствия ограничения максимальной длины пароля (Max Length):
    Бэкенд успешно принимает пароль из 500 символов и возвращает 200 OK.
    """
    with allure.step("Генерация пароля из 500 символов"):
        long_password = "Aa1!" + "a" * 496
        payload = {
        "username": f"test_max_absence_{hash(long_password)}@test.com",
            "password": long_password,
            "firstName": "John",
            "lastName": "Smith"
        }

    with allure.step("Отправка POST-запроса с паролем из 500 символов"):
        response = page.request.post(API_URL, data=payload)
        response_json = response.json() if response.status != 500 else response.text

    with allure.step("Фиксация поведения бэкенда (прием пароля из 500 символов)"):
        # Если добавят ограничение maxLength (например, 128), статус станет 400,
        # и этот тест просигнализирует об изменениях.
        assert response.status == 200, (
            f"Ожидался статус 200 (текущее поведение бэкенда без ограничения длины), "
            f"но получен {response.status}. Ответ: {response_json}"
        )
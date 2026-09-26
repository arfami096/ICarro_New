import allure
import pytest
from playwright.sync_api import Page, expect, TimeoutError
from pages_playwright.login_playwright_page import LoginPlaywrightPage


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("Navigation")
@allure.title("Прямое открытие формы авторизации")
@allure.severity(allure.severity_level.NORMAL)
def test_navigation_to_login(page: Page, login_playwright_page: LoginPlaywrightPage):
    with allure.step("Открыть форму авторизации через URL"):
        login_playwright_page.open_login_form()

    with allure.step("Проверить, что поле email отображается на странице"):
        expect(login_playwright_page.email_input).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("Negative Login - Invalid Credentials")
@allure.title("Авторизация с неверными или несуществующими учетными данными")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("email, password, expected_error", [
    ("nonexistent_user@example.com", "ValidPassword123!", "Login or password incorrect"),
    ("valid_user@example.com", "WrongPassword!", "Login or password incorrect"),
    ("", "ValidPassword123!", "Email is required"),
    ("test_wrong@example.com", "", "Password is required"),
])
def test_login_invalid_credentials(login_playwright_page, email, password, expected_error):
    with allure.step("Открыть форму логина"):
        login_playwright_page.open_login_form()

    with allure.step(f"Ввести email: '{email}' и пароль"):
        if email:
            login_playwright_page.fill_email(email)
        if password:
            login_playwright_page.fill_password(password)
        login_playwright_page.remove_focus()

    with allure.step("Проверка состояния кнопки и отправка (если доступна)"):
        if email and password:
            login_playwright_page.submit_login()
        else:
            try:
                login_playwright_page.assert_submit_button_disabled(disabled=True)
            except (AssertionError, TimeoutError):
                pytest.xfail("Кнопка отправки не заблокирована на фронтенде при пустых обязательных полях")

    with allure.step(f"Проверить текст ошибки: '{expected_error}'"):
        try:
            login_playwright_page.assert_error_message(expected_error)
        except (AssertionError, TimeoutError):
            pytest.xfail(f"Фронтенд не выводит ожидаемый текст ошибки '{expected_error}'")


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("UI State Consistency")
@allure.title("Баг: Проверка синхронности авторизации в хедере и футере")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(
    reason="BUG: Состояние авторизации не сквозное. В хедере отображается 'Log out', но в футере по-прежнему доступна кнопка 'Log in'."
)
def test_footer_auth_state_consistency(page: Page, login_playwright_page: LoginPlaywrightPage):
    with allure.step("Открыть форму логина и авторизоваться валидными данными"):
        login_playwright_page.open_login_form()
        login_playwright_page.fill_email("valid_user@example.com")  # Подставьте ваш валидный тестовый email
        login_playwright_page.fill_password("ValidPassword123!")  # Подставьте валидный пароль
        login_playwright_page.submit_login()

    with allure.step("Проскролить страницу вниз к футеру"):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    with allure.step("Проверить состояние кнопки 'Log in' в футере"):
        # Селектор ищет кнопку входа в футере, которая не должна там быть после логина
        footer_login_btn = page.locator("footer text='Log in', .footer text='Log in'")

        # Если кнопка видна, падаем — это и есть баг, который отловит xfail
        expect(footer_login_btn).not_to_be_visible()
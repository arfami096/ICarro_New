import re

import allure
import pytest
from playwright.sync_api import Page, expect, TimeoutError
from pages_playwright.login_playwright_page import LoginPlaywrightPage
import os
from dotenv import load_dotenv

load_dotenv()

# Читаем переменные из .env (подставьте те ключи, которые у вас записаны в файле .env)
VALID_EMAIL = os.getenv("USER_EMAIL")       # или "USER_EMAIL", в зависимости от того, как вы назвали переменную в .env
VALID_PASSWORD = os.getenv("USER_PASSWORD") # или "USER_PASSWORD"


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
@allure.story("Positive Login")
@allure.title("Успешная авторизация с валидными учетными данными")
@allure.severity(allure.severity_level.BLOCKER)
def test_successful_login(page: Page, login_playwright_page: LoginPlaywrightPage):
    with allure.step("Открыть форму логина"):
        login_playwright_page.open_login_form()

    with allure.step("Ввести валидный email и пароль"):
        login_playwright_page.fill_email(VALID_EMAIL)
        login_playwright_page.fill_password(VALID_PASSWORD)

    with allure.step("Кликнуть кнопку отправки формы"):
        login_playwright_page.submit_login()

    with allure.step("Закрыть модальное окно успешного входа (нажать 'OK')"):
        ok_button = page.locator("button:text('OK')").or_(page.locator("text='OK'"))
        if ok_button.is_visible(timeout=5000):
            ok_button.click()

    with allure.step("Проверить успешность входа (появление кнопки Log out)"):
        logout_btn = page.locator("text='Log out'").or_(page.locator("button:has-text('Log out')"))
        expect(logout_btn).to_be_visible(timeout=5000)


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("Negative Login - Invalid Credentials")
@allure.title("Авторизация с неверными, пустыми данными и некорректным форматом email")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("email, password, expected_error, should_submit", [
    ("nonexistent_user@example.com", "ValidPassword123!", "Login or password incorrect", True),
    ("valid_user@example.com", "WrongPassword!", "Login or password incorrect", True),
    ("", "ValidPassword123!", "Email is required", False),
    ("test_wrong@example.com", "", "Password is required", False),
    ("plain-string-without-at", "ValidPassword123!", "Wrong email format", False),
])
def test_login_invalid_credentials(login_playwright_page, email, password, expected_error, should_submit):
    with allure.step("Открыть форму логина"):
        login_playwright_page.open_login_form()

    with allure.step(f"Ввести email: '{email}' и пароль"):
        # Кликаем и заполняем поля с учетом возможных пустых значений для активации валидации
        login_playwright_page.email_input.click()
        if email:
            login_playwright_page.fill_email(email)

        login_playwright_page.password_input.click()
        if password:
            login_playwright_page.fill_password(password)

        login_playwright_page.remove_focus()

    with allure.step("Проверка состояния кнопки и отправка"):
        if should_submit:
            login_playwright_page.submit_login()
        else:
            login_playwright_page.assert_submit_button_disabled(disabled=True)

    with allure.step(f"Проверить текст ошибки: '{expected_error}'"):
        login_playwright_page.assert_error_message(expected_error)


@pytest.mark.ui
@pytest.mark.security
@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("Security & Input Sanitization")
@allure.title("Senior+: Проверка устойчивости формы к XSS инъекциям в поле email")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_security_xss_resilience(login_playwright_page: LoginPlaywrightPage):
    xss_payload = "<script>alert('xss_test')</script>"

    with allure.step("Открыть форму логина"):
        login_playwright_page.open_login_form()

    with allure.step("Ввести потенциально опасный XSS-пайлоад в поле email"):
        login_playwright_page.fill_email(xss_payload)
        login_playwright_page.fill_password("ValidPassword123!")
        login_playwright_page.remove_focus()

    with allure.step("Убедиться, что приложение экранирует ввод и выдает ошибку формата"):
        login_playwright_page.assert_error_message("Wrong email format")


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("UI State Consistency")
@allure.title("Баг: Проверка синхронности авторизации в хедере и футере")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(
    reason="BUG-001: Состояние авторизации не сквозное. В хедере 'Log out', но в футере доступна кнопка 'Log in'."
)
def test_footer_auth_state_consistency(page: Page, login_playwright_page: LoginPlaywrightPage):
    with allure.step("Открыть форму логина и авторизоваться валидными данными"):
        login_playwright_page.open_login_form()
        login_playwright_page.fill_email("VALID_EMAIL")
        login_playwright_page.fill_password("VALID_PASSWORD")
        login_playwright_page.submit_login()

    with allure.step("Проскролить страницу вниз к футеру"):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    with allure.step("Проверить состояние кнопки 'Log in' в футере"):
        footer_login_btn = page.locator("footer text='Log in', .footer text='Log in'")
        expect(footer_login_btn).not_to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("Session Management & Modals")
@allure.title("Senior+: Проверка персистентности сессии при обновлении страницы до закрытия модального окна успеха")
@allure.description("""
    **Описание тест-кейса:**
    Проверка поведения сессии, если пользователь выполнил успешный логин, дождался модального окна об успехе ("Logged in success"), 
    но **не нажал кнопку "OK"**, а сразу сделал перезагрузку страницы (`page.reload()`).

    **Ожидаемый баг / Поведение:**
    Зафиксировано, что при таком сценарии пользователя сбрасывает обратно на форму логина, хотя токен/хедер уже фиксируют состояние 'Log out'.
""")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(
    reason="BUG: Рефреш страницы до подтверждения модального окна успеха сбрасывает стейт сессии, несмотря на изменение хедера."
)
def test_session_refresh_before_modal_close(page: Page, login_playwright_page: LoginPlaywrightPage):
    with allure.step("Открыть форму логина и авторизоваться"):
        login_playwright_page.open_login_form()
        login_playwright_page.fill_email("VALID_EMAIL")
        login_playwright_page.fill_password("VALID_PASSWORD")
        login_playwright_page.submit_login()

    with allure.step("Дождаться появления модального окна успеха, но НЕ нажимать OK, а сделать page.reload()"):
        success_modal = page.locator("text='Logged in success', div:has-text('Logged in success')")
        expect(success_modal).to_be_visible()
        page.reload(wait_until="networkidle")

    with allure.step("Проверить, что сессия сохранилась (ожидаем падение на баге или срабатывание xfail)"):
        logout_btn = page.locator("text='Log out'").or_(page.locator("button:has-text('Log out')"))
        expect(logout_btn).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("Session Management & Modals")
@allure.title("Успешная сессия и сохранение авторизации после рефреша на странице поиска (с закрытием модалки)")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_session_persistence_after_modal_dismiss(page: Page, login_playwright_page: LoginPlaywrightPage):
    with allure.step("Авторизоваться"):
        login_playwright_page.open_login_form()
        login_playwright_page.fill_email(VALID_EMAIL)
        login_playwright_page.fill_password(VALID_PASSWORD)
        login_playwright_page.submit_login()

    with allure.step("Закрыть модальное окно успешного входа (нажать 'OK') и дождаться перехода на страницу поиска"):
        ok_button = page.locator("button:text('OK')").or_(page.locator("text='OK'"))

        # Кликаем по кнопке OK и одновременно ждем, пока изменится URL на /search
        with page.expect_navigation(url=re.compile(r".*search.*")):
            ok_button.click()

    with allure.step("Обновить страницу (page.reload)"):
        page.reload(wait_until="networkidle")

    with allure.step("Проверить, что сессия полностью стабильна и пользователь авторизован"):
        logout_btn = page.locator("text='Log out'").or_(page.locator("button:has-text('Log out')"))
        expect(logout_btn).to_be_visible(timeout=5000)
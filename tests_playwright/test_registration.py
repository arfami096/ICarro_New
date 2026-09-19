import re
import allure
import pytest
from playwright.sync_api import Page, expect
from data.data_generator import UserGenerator
from pages_playwright.registration_playwright_page import RegistrationPlaywrightPage


@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Navigation")
@allure.title("Навигация со страницы на форму регистрации")
@allure.severity(allure.severity_level.NORMAL)
def test_navigation_to_registration(reg_playwright_page, page: Page):
    with allure.step("Открыть главную страницу приложения"):
        reg_playwright_page.open_main_page()

    with allure.step("Кликнуть на кнопку регистрации в навигационном меню"):
        reg_playwright_page.click_registration_button_in_menu()

    with allure.step("Проверить, что текущий URL содержит /register"):
        expect(page).to_have_url(re.compile(r".*/register"))


@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Positive Registration")
@allure.title("Успешная регистрация нового пользователя (End-to-End)")
@allure.severity(allure.severity_level.BLOCKER)
def test_registration_success(reg_playwright_page):
    user = UserGenerator.get_random_user()

    with allure.step("Открыть форму регистрации"):
        reg_playwright_page.open_registration_form()

    with allure.step(f"Заполнить форму валидными данными: {user.email}"):
        reg_playwright_page.fill_registration_form(user)
        reg_playwright_page.set_policy_checkbox(True)

    with allure.step("Отправить форму регистрации"):
        reg_playwright_page.submit_registration()

    with allure.step("Проверить успешный тост/сообщение и закрытие модалки/окна"):
        reg_playwright_page.assert_confirmation_text("Registered")
        reg_playwright_page.assert_confirmation_text_1("You are logged in success")
        reg_playwright_page.close_window()


@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Negative Registration - Fields Validation")
@allure.title("Валидация обязательных полей и некорректных форматов")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("field_name, invalid_value, expected_error", [
    ("name", "", "Name is required"),
    ("name", "A", "Name must be at least 2 characters"),  # Пример расширенной бизнес-логики
    ("last_name", "", "Last name is required"),
    ("email", "tonygmail.com", "Wrong email format"),
    ("email", " tony@gmail.com ", "Wrong email format"),  # Пробелы внутри/вокруг email
    ("email", "", "Email is required"),
    ("password", "P123$", "Password must contain minimum 6 symbols"),
    ("password", "", "Password is required")
])
def test_registration_negative_fields(reg_playwright_page, field_name, invalid_value, expected_error):
    kwargs = {field_name: invalid_value}
    user = UserGenerator.get_random_user(**kwargs)

    with allure.step("Открыть форму регистрации"):
        reg_playwright_page.open_registration_form()

    with allure.step(f"Заполнить форму невалидным значением для '{field_name}': '{invalid_value}'"):
        reg_playwright_page.fill_registration_form(user)
        reg_playwright_page.set_policy_checkbox(True)
        reg_playwright_page.remove_focus()

    with allure.step(f"Проверить текст ошибки '{expected_error}'"):
        reg_playwright_page.assert_error_message(expected_error)

    with allure.step("Строгая проверка: кнопка Submit заблокирована при наличии ошибок валидации"):
        reg_playwright_page.assert_submit_button_disabled(disabled=True)


@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Negative Registration - Checkbox")
@allure.title("Проверка обязательности чекбокса пользовательского соглашения")
@allure.severity(allure.severity_level.NORMAL)
def test_registration_without_check_box(reg_playwright_page):
    user = UserGenerator.get_random_user()

    with allure.step("Открыть форму и заполнить валидные данные"):
        reg_playwright_page.open_registration_form()
        reg_playwright_page.fill_registration_form(user)
        reg_playwright_page.set_policy_checkbox(True)

    with allure.step("Снять чекбокс пользовательского соглашения"):
        reg_playwright_page.set_policy_checkbox(False)
        reg_playwright_page.remove_focus()

    with allure.step("Проверить ошибку и блокировку отправки"):
        reg_playwright_page.assert_error_message("You must accept the terms")
        reg_playwright_page.assert_submit_button_disabled(disabled=True)


@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Edge Cases & Sanitization")
@allure.title("Проверка обработки пробелов (whitespace) и UX-санитизации полей")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "name, last_name, email, password, test_type, expected",
    [
        ("   ", "Smith", "valid@test.com", "Password123!", "error", "Name is required"),
        ("John", "   ", "valid@test.com", "Password123!", "error", "Last name is required"),
        ("John", "Smith", "   ", "Password123!", "error", "Email is required"),
        ("John", "Smith", "valid@test.com", "   ", "error", "Password must contain minimum 6 symbols"),
        (" John ", " Smith ", "valid@test.com", "Password123!", "success", "Registration is completed"),
        ("John", "Smith", " test@gmail.com ", "Password123!", "error", "Wrong email format"),
    ],
    ids=[
        "spaces_in_name",
        "spaces_in_lastname",
        "spaces_in_email",
        "spaces_in_password",
        "trim_leading_trailing_spaces",
        "spaces_inside_email"
    ]
)
def test_registration_whitespace_handling(
        reg_playwright_page: RegistrationPlaywrightPage,
        name: str,
        last_name: str,
        email: str,
        password: str,
        test_type: str,
        expected: str
):
    with allure.step("Открыть форму регистрации"):
        reg_playwright_page.open_registration_form()

    with allure.step("Ввести данные с учетом пробельных сценариев"):
        reg_playwright_page.fill_name(name)
        reg_playwright_page.fill_last_name(last_name)
        reg_playwright_page.fill_email(email)
        reg_playwright_page.fill_password(
            "Password123!" if password == "error_case" or password == "Password123!" else password)
        # Если в тесте передан кастомный пароль (например пробелы), устанавливаем его:
        if password.strip() == "" or password.isspace():
            reg_playwright_page.fill_password(password)

        reg_playwright_page.set_policy_checkbox(True)
        reg_playwright_page.remove_focus()

    if test_type == "error":
        with allure.step(f"Ожидаем ошибку валидации: '{expected}'"):
            reg_playwright_page.assert_error_message(expected)
            reg_playwright_page.assert_submit_button_disabled(disabled=True)
    elif test_type == "success":
        with allure.step("Отправить форму с триммированными данными"):
            reg_playwright_page.submit_registration()
        with allure.step(f"Ожидаем подтверждение: '{expected}'"):
            reg_playwright_page.assert_confirmation_text(expected)
import allure
import pytest
from playwright.async_api import Page

from data.data_generator import UserGenerator
from pages_playwright.registration_playwright_page import RegistrationPlaywrightPage


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Keyboard / UX")
@allure.title("Отправка формы регистрации нажатием клавиши Enter из последнего поля")
@allure.severity(allure.severity_level.NORMAL)
def test_registration_submit_by_enter_key(reg_playwright_page: RegistrationPlaywrightPage, page: Page):
    user = UserGenerator.get_random_user()

    with allure.step("Открыть форму регистрации"):
        reg_playwright_page.open_registration_form()

    with allure.step("Заполнить все поля формы"):
        reg_playwright_page.fill_registration_form(user)
        reg_playwright_page.set_policy_checkbox(True)

    with allure.step("Нажать клавишу Enter в поле пароля"):
        reg_playwright_page.password_input.press("Enter")

    with allure.step("Проверить успешность регистрации"):
        reg_playwright_page.assert_confirmation_text("Registered")
        reg_playwright_page.assert_confirmation_text_1("You are logged in success")
        reg_playwright_page.close_window()
from playwright.sync_api import Page, expect
import allure
from pages_playwright.base_playwright_page import BasePlaywrightPage


class LoginPlaywrightPage(BasePlaywrightPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("[name='username']")
        self.password_input = page.locator("[name='password']")
        self.login_btn = page.locator("button[type='submit']")
        self.error_message = page.locator(".error")

    @allure.step("Открытие страницы логина")
    def open_login_form(self):
        self.open_url("/login")
        return self

    @allure.step("Ввод email: {email}")
    def fill_email(self, email: str):
        self.email_input.fill("")
        self.email_input.press_sequentially(email, delay=30)
        return self

    @allure.step("Ввод пароля")
    def fill_password(self, password: str):
        self.password_input.fill("")
        self.password_input.press_sequentially(password, delay=30)
        return self

    @allure.step("Отправка формы логина")
    def submit_login(self):
        self.login_btn.click()
        return self

    @allure.step("Проверка текста ошибки")
    def assert_error_message(self, expected_error: str):
        expect(self.error_message).toBeVisible(timeout=5000)
        expect(self.error_message).toHaveText(expected_error)
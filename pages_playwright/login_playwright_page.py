from playwright.sync_api import Page, expect
import allure
from pages_playwright.base_playwright_page import BasePlaywrightPage


class LoginPlaywrightPage(BasePlaywrightPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("[name='username']")
        self.password_input = page.locator("[name='password']")
        self.login_btn = page.locator("button[type='submit']")
        self.error_message = page.locator(".error, .error-message, mat-error, .alert-danger, div[style*='color: red']")

    @allure.step("Убрать фокус с полей ввода")
    def remove_focus(self):
        self.page.locator("body").click(position={"x": 0, "y": 0})
        return self

    @allure.step("Проверка состояния кнопки отправки (disabled={disabled})")
    def assert_submit_button_disabled(self, disabled: bool = True):
        if disabled:
            expect(self.login_btn).to_be_disabled()
        else:
            expect(self.login_btn).to_be_enabled()
        return self


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

    @allure.step("Проверка сообщения об ошибке: {expected_error}")
    def assert_error_message(self, expected_error: str):
        # Ищем любой видимый элемент, содержащий текст ошибки
        error_locator = self.page.locator(f":text('{expected_error}')")
        expect(error_locator.first).to_be_visible(timeout=5000)

    @allure.step("Убрать фокус с полей ввода")
    def remove_focus(self):
        # Клик по заголовку или любому пустому месту страницы убирает фокус
        self.page.locator("body").click(position={"x": 0, "y": 0})
        return self

    @allure.step("Проверка состояния кнопки отправки (disabled={disabled})")
    def assert_submit_button_disabled(self, disabled: bool = True):
        if disabled:
            expect(self.login_btn).to_be_disabled()
        else:
            expect(self.login_btn).to_be_enabled()
        return self
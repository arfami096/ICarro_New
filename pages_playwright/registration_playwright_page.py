from playwright.sync_api import Page, expect
import allure
from pages_playwright.base_playwright_page import BasePlaywrightPage


class RegistrationPlaywrightPage(BasePlaywrightPage):
    def __init__(self, page: Page):
        super().__init__(page)

        # --- ЛОКАТОРЫ ---
        self.nav_registration_btn = page.locator("[href='/register']").first
        self.name_input = page.locator("[name='firstName']")
        self.last_name_input = page.locator("[name='lastName']")
        self.email_input = page.locator("[name='username']")
        self.password_input = page.locator("input[type='password']")
        self.policy_checkbox = page.locator("#terms-of-use")

        self.error_message = page.locator(".error")

        self.submit_btn = page.locator("button[type='submit']")
        self.ok_btn = page.locator("//*[contains(text(), 'OK')]")

        self.confirmation_text_locator = page.locator("h3")
        self.confirmation_text_1_locator = page.locator("p")

    # --- НАВИГАЦИЯ ---
    @allure.step("Открытие главной страницы")
    def open_main_page(self):
        self.open_url()
        return self

    @allure.step("Клик по кнопке регистрации в меню")
    def click_registration_button_in_menu(self):
        self.nav_registration_btn.click()
        return self

    def get_current_url(self) -> str:
        return self.page.url

    @allure.step("Открытие страницы регистрации")
    def open_registration_form(self):
        self.open_url("/register")
        return self

    # --- ДЕЙСТВИЯ С ФОРМОЙ ---
    @allure.step("Ввод имени: {name}")
    def fill_name(self, name: str):
        self.name_input.press_sequentially(name, delay=30)
        return self

    @allure.step("Ввод фамилии: {last_name}")
    def fill_last_name(self, last_name: str):
        self.last_name_input.press_sequentially(last_name, delay=30)
        return self

    @allure.step("Ввод email: {email}")
    def fill_email(self, email: str):
        self.email_input.press_sequentially(email, delay=30)
        return self

    @allure.step("Ввод пароля")
    def fill_password(self, password: str):
        self.password_input.press_sequentially(password, delay=30)
        return self

    @allure.step("Установка чекбокса 'Terms of use' в состояние: {state}")
    def set_policy_checkbox(self, state: bool):
        is_checked = self.policy_checkbox.is_checked()
        if is_checked != state:
            self.policy_checkbox.click()
        return self

    @allure.step("Заполнение формы регистрации")
    def fill_registration_form(self, user):
        self.fill_name(user.name)
        self.fill_last_name(user.last_name)
        self.fill_email(user.email)
        self.fill_password(user.password)
        return self

    @allure.step("Снятие фокуса с полей (триггер onBlur)")
    def remove_focus(self):
        self.page.locator("h1.title").click()
        return self

    @allure.step("Отправка формы регистрации")
    def submit_registration(self):
        self.submit_btn.click()
        return self

    @allure.step("Закрытие окна")
    def close_window(self):
        self.ok_btn.click()
        return self

    # --- ПРОВЕРКИ И АССЕРТЫ (PLAYWRIGHT EXPECT) ---
    def assert_confirmation_text(self, expected_text: str):
        expect(self.confirmation_text_locator).to_be_visible(timeout=5000)
        expect(self.confirmation_text_locator).to_have_text(expected_text)

    def assert_confirmation_text_1(self, expected_text: str):
        expect(self.confirmation_text_1_locator).to_be_visible(timeout=5000)
        expect(self.confirmation_text_1_locator).to_have_text(expected_text)

    def assert_error_message(self, expected_error: str):
        expect(self.error_message.first).to_be_visible(timeout=5000)
        expect(self.error_message.first).to_have_text(expected_error)

    def assert_submit_button_disabled(self, disabled: bool = True):
        if disabled:
            expect(self.submit_btn).to_be_disabled()
        else:
            expect(self.submit_btn).to_be_enabled()
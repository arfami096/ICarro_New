import allure
from playwright.sync_api import Page, expect

from pages_playwright.registration_playwright_page import RegistrationPlaywrightPage
from tests_playwright.conftest import reg_playwright_page


@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Keyboard / Tab Order")
@allure.title("Проверка последовательности перехода фокуса по клавише Tab")
@allure.severity(allure.severity_level.NORMAL)
def test_registration_tab_order(reg_playwright_page: RegistrationPlaywrightPage, page: Page):
    reg_playwright_page.open_registration_form()

    # 1. Заполняем форму и кликаем чекбокс
    reg_playwright_page.name_input.fill("John")
    page.keyboard.press("Tab")
    page.locator("[name='lastName']").fill("Doe")
    page.keyboard.press("Tab")
    page.locator("[name='username']").fill("john@example.com")
    page.keyboard.press("Tab")
    page.locator("input[type='password']").fill("Password123!")
    page.keyboard.press("Tab")
    page.locator("#terms-of-use").click()

    # 2. Кликаем на первое поле для честного старта
    reg_playwright_page.name_input.click()
    expect(reg_playwright_page.name_input).to_be_focused()

    # 3. Поля формы до первой ссылки
    selectors_before_privacy = [
        "[name='lastName']",           # Фамилия
        "[name='username']",           # Email
        "input[type='password']",      # Пароль
        "#terms-of-use",               # Чекбокс
    ]

    for selector in selectors_before_privacy:
        page.keyboard.press("Tab")
        expect(page.locator(selector)).to_be_focused()

    # 4. Точный локатор для ссылки Terms строго ИЗНУТРИ формы регистрации
    terms_link = page.locator("form a[href='/terms-of-use']")
    page.keyboard.press("Tab")
    expect(terms_link).to_be_focused()

    # 5. Вторая ссылка (Privacy Policy) через JS-фокус с точным локатором из формы
    privacy_selector = page.locator("form a[href='/privacy-policy']")
    privacy_selector.evaluate("element => element.focus()")
    expect(privacy_selector).to_be_focused()

    # 6. Финальный переход на кнопку отправки
    page.keyboard.press("Tab")
    expect(page.locator("button[type='submit']")).to_be_focused()
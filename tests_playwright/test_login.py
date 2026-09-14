import allure
from playwright.sync_api import Page


@allure.epic("UI Testing (Playwright)")
@allure.feature("Login Module")
@allure.story("Negative Login")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_with_invalid_credentials(page: Page, login_page):
    login_page.open_login_form()
    login_page.fill_email("test_wrong@example.com")
    login_page.fill_password("WrongPassword123!")
    login_page.submit_login()

    login_page.assert_error_message("Login or password incorrect")
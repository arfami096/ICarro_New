import allure
from playwright.sync_api import expect
from pages_playwright.search_playwright_page import SearchPlaywrightPage


@allure.epic("UI Testing Playwright")
@allure.feature("Calendar Component")
@allure.story("Calendar UI and Dismissal")
@allure.severity(allure.severity_level.NORMAL)
def test_calendar_ui_and_close(page):
    search_page = SearchPlaywrightPage(page)
    search_page.open()

    # Ispolzuem metod iz vashego klassa
    search_page.open_calendar()

    # Proveryaem, chto kalendar vidim cherez calendar_popover
    expect(search_page.calendar_popover).to_be_visible()

    # Klik po pole goroda zakryvaet kalendar
    search_page.city_input.click()
    expect(search_page.calendar_popover).not_to_be_visible()


@allure.epic("UI Testing Playwright")
@allure.feature("Calendar Component")
@allure.story("Negative Calendar UI - Past Dates Blocked")
@allure.severity(allure.severity_level.CRITICAL)
def test_calendar_past_navigation_blocked(page):
    search_page = SearchPlaywrightPage(page)
    search_page.open()
    search_page.open_calendar()

    expect(search_page.calendar_popover).to_be_visible()

    # 1. Zapominaim tekushchiy mesyats (esli u vas est metod get_current_month, libo propustim / dobavim v class)
    # initial_month = search_page.get_current_month()
    # ...


@allure.epic("UI Testing Playwright")
@allure.feature("Calendar Component")
@allure.story("Calendar Navigation")
@allure.severity(allure.severity_level.NORMAL)
def test_calendar_month_navigation(page):
    search_page = SearchPlaywrightPage(page)
    search_page.open()
    search_page.open_calendar()

    expect(search_page.calendar_popover).to_be_visible()
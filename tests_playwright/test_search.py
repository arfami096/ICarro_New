import allure
import pytest
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Search Module")
@allure.story("Positive Search")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_car_by_city(page: Page, search_playwright_page):
    search_playwright_page.open()
    search_playwright_page.fill_city("Tel Aviv")

    # Perehodim na sleduyushchiy mesyats i vyбираем безопасные даты (например, 10 и 15 числа)
    search_playwright_page.select_dates_in_next_month(10, 15)

    search_playwright_page.submit_search()

    search_playwright_page.assert_results_are_present()
    assert search_playwright_page.get_cars_count() > 0, "Spisok avtomobiley pust"


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Search Module")
@allure.story("Negative Search")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(reason="Фронтенд блокирует поиск для несуществующего города (требует выбор из autocomplete списка)")
def test_search_non_existent_city(page: Page, search_playwright_page):
    search_playwright_page.open()
    search_playwright_page.fill_city("NonExistentCity12345")

    # Выбираем даты через календарь
    search_playwright_page.select_dates_in_calendar(25, 27)

    search_playwright_page.submit_search()
    search_playwright_page.assert_no_results()
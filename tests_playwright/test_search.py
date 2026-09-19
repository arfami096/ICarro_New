import allure
import pytest
from playwright.sync_api import Page


@allure.epic("UI Testing (Playwright)")
@allure.feature("Search Module")
@allure.story("Positive Search")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_car_by_city(page: Page, search_playwright_page):
    # ИСПРАВЛЕНО: заменено с open_search_page() на open()
    search_playwright_page.open()
    search_playwright_page.fill_city("Tel Aviv")

    # Выбираем даты кликом по календарю (например, 20-е и 25-е числа текущего месяца)
    search_playwright_page.select_dates_in_calendar(20, 25)

    search_playwright_page.submit_search()

    search_playwright_page.assert_results_are_present()
    assert search_playwright_page.get_cars_count() > 0, "Список автомобилей пуст"


@allure.epic("UI Testing (Playwright)")
@allure.feature("Search Module")
@allure.story("Negative Search")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(reason="Фронтенд блокирует поиск для несуществующего города (требует выбор из autocomplete списка)")
def test_search_non_existent_city(page: Page, search_playwright_page):
    search_playwright_page.open()
    search_playwright_page.fill_city("NonExistentCity12345")

    # Выбираем даты через календарь
    search_playwright_page.select_dates_in_calendar(20, 25)

    search_playwright_page.submit_search()
    search_playwright_page.assert_no_results()
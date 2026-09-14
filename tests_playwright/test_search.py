import allure
from playwright.sync_api import Page


@allure.epic("UI Testing (Playwright)")
@allure.feature("Search Module")
@allure.story("Positive Search")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_car_by_city(page: Page, search_page):
    search_page.open_search_page()
    search_page.fill_city("Tel Aviv")
    search_page.submit_search()

    search_page.assert_results_are_present()
    assert search_page.get_cars_count() > 0, "Список автомобилей пуст"


@allure.epic("UI Testing (Playwright)")
@allure.feature("Search Module")
@allure.story("Negative Search")
@allure.severity(allure.severity_level.NORMAL)
def test_search_non_existent_city(page: Page, search_page):
    search_page.open_search_page()
    search_page.fill_city("NowhereCity12345")
    search_page.submit_search()

    search_page.assert_no_results()
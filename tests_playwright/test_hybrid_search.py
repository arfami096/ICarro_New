import allure
import pytest
from data.data_generator import CarGenerator, SearchDataGenerator
from pages_playwright.login_playwright_page import LoginPlaywrightPage
from pages_playwright.search_playwright_page import SearchPlaywrightPage


@pytest.mark.ui
@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known UI Bug: The secondary filtering/search form after initial search is broken and does not respond to interaction.",
    strict=False
)
@allure.epic("UI/API Hybrid Testing Playwright")
@allure.feature("Search functionality")
@allure.story("API Setup -> Broken UI Filter Interaction -> API Teardown")
@allure.severity(allure.severity_level.BLOCKER)
def test_hybrid_car_search_broken_form(page, auth_api):
    login_page = LoginPlaywrightPage(page)
    search_page = SearchPlaywrightPage(page)

    with allure.step("API: Podgotovka testovyh dannyh (sozdanie mashiny)"):
        target_city = SearchDataGenerator.get_random_city()
        car_obj = CarGenerator.get_random_car(city=target_city)
        serial_number = car_obj.reg_number

        car_payload = {
            "serialNumber": serial_number,
            "manufacture": car_obj.manufacture,
            "model": car_obj.model,
            "year": str(car_obj.year),
            "fuel": car_obj.fuel,
            "seats": int(car_obj.seats),
            "carClass": car_obj.car_class,
            "pricePerDay": float(car_obj.price),
            "about": car_obj.about,
            "city": car_obj.city
        }

        response = auth_api.add_car(car_payload)
        assert response.status_code == 200, f"Oshibka prerikvizita: {response.text}"

    try:
        with allure.step(f"UI: Vvod goroda ({target_city}) i dat v formy poiska"):
            search_page.open()
            search_page.fill_city(target_city)
            search_page.select_dates_in_calendar(21, 25)
            search_page.submit_search()

        with allure.step("UI: Popytka vzaimodeistvovat so slomannoy formoy filtracii (nav-tab filter)"):
            # Vzaimodeistvuem so slomannym elementom, gde nichego ne proishodit
            search_page.interact_with_broken_filter_form()

    finally:
        with allure.step(f"API (Teardown): Udalenie testovoy mashiny {serial_number}"):
            auth_api.delete_car(serial_number)
import allure
from data.data_generator import CarGenerator, SearchDataGenerator
from pages_playwright.login_playwright_page import LoginPlaywrightPage
from pages_playwright.search_playwright_page import SearchPlaywrightPage


@allure.epic("UI/API Hybrid Testing Playwright")
@allure.feature("Search functionality")
@allure.story("API Setup -> UI Search -> API Teardown")
@allure.severity(allure.severity_level.BLOCKER)
def test_hybrid_car_search(page, auth_api):
    login_page = LoginPlaywrightPage(page)
    search_page = SearchPlaywrightPage(page)

    with allure.step("API: Подготовка тестовых данных (создание машины)"):
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

        # Отправляем запрос через фикстуру API
        response = auth_api.add_car(car_payload)
        assert response.status_code == 200, f"Ошибка пререквизита: {response.text}"

    # Оборачиваем UI-логику в try..finally, чтобы машина гарантированно удалилась при падении теста
    try:
        with allure.step(f"UI: Поиск машины в городе {target_city}"):
            search_page.open()
            search_page.fill_city(target_city)
            # Выбираем будущие активные дни в календаре (21 и 25 число)
            search_page.select_dates_in_calendar(21, 25)
            search_page.submit_search()

        with allure.step("UI: Проверка отображения результатов поиска"):
            search_page.assert_results_are_present()
            with allure.step("UI: Проверка отображения результатов поиска"):
                search_page.assert_results_are_present()
                # Проверяем созданную машину по ее уникальному серийному номеру (рег. номеру)
                search_page.assert_car_present_by_serial_number(serial_number)

    finally:
        with allure.step(f"API (Teardown): Удаление тестовой машины {serial_number}"):
            auth_api.delete_car(serial_number)
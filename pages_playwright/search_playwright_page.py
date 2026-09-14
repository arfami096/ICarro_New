from playwright.sync_api import Page, expect
import allure
from pages_playwright.base_playwright_page import BasePlaywrightPage


class SearchPlaywrightPage(BasePlaywrightPage):
    def __init__(self, page: Page):
        super().__init__(page)
        # --- ЛОКАТОРЫ ФОРМЫ ПОИСКА ---
        self.city_input = page.locator("#city")
        self.dates_input = page.locator("#dates")  # или селектор поля выбора дат
        self.yalla_btn = page.locator("button[type='submit']")

        # --- ЛОКАТОРЫ РЕЗУЛЬТАТОВ (КАРТОЧЕК МАШИН) ---
        self.car_cards = page.locator(".car-container, .car-card, [data-testid='car-item']")
        self.no_results_message = page.locator(".no-results, text=No cars found")

    # --- НАВИГАЦИЯ ---
    @allure.step("Открытие страницы поиска")
    def open_search_page(self):
        self.open_url("/search")
        return self

    # --- ДЕЙСТВИЯ С ФОРМОЙ ПОИСКА ---
    @allure.step("Ввод города: {city}")
    def fill_city(self, city: str):
        self.city_input.fill("")
        self.city_input.press_sequentially(city, delay=30)
        return self

    @allure.step("Выбор дат: {dates_range}")
    def fill_dates(self, dates_range: str):
        self.dates_input.fill("")
        self.dates_input.press_sequentially(dates_range, delay=30)
        return self

    @allure.step("Клик по кнопке поиска (Yalla!)")
    def submit_search(self):
        self.yalla_btn.click()
        return self

    @allure.step("Выполнение полного поиска по городу: {city}")
    def search_car_by_city(self, city: str):
        self.fill_city(city)
        self.submit_search()
        return self

    # --- ПРОВЕРКИ РЕЗУЛЬТАТОВ ВЫДАЧИ ---
    @allure.step("Получение количества найденных автомобилей")
    def get_cars_count(self) -> int:
        return self.car_cards.count()

    @allure.step("Проверка, что список машин отображается")
    def assert_results_are_present(self):
        expect(self.car_cards.first).toBeVisible(timeout=5000)
        return self

    @allure.step("Проверка наличия автомобиля с названием: {car_name}")
    def assert_car_present_by_name(self, car_name: str):
        car_element = self.page.locator(f"text={car_name}")
        expect(car_element).toBeVisible(timeout=5000)
        return self

    @allure.step("Проверка сообщения об отсутствии результатов")
    def assert_no_results(self):
        expect(self.no_results_message).toBeVisible(timeout=5000)
        return self
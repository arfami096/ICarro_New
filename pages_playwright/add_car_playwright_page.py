from playwright.sync_api import Page, expect
import allure
from pages_playwright.base_playwright_page import BasePlaywrightPage


class AddCarPlaywrightPage(BasePlaywrightPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.city_input = page.locator("#city")
        self.manufacture_input = page.locator("#make")
        self.model_input = page.locator("#model")
        self.year_input = page.locator("#year")
        self.seats_input = page.locator("#seats")
        self.serial_number_input = page.locator("#serialNumber")
        self.price_input = page.locator("#price")
        self.submit_btn = page.locator("button[type='submit']")

    @allure.step("Открытие страницы добавления автомобиля")
    def open_add_car_page(self):
        self.open_url("/let-car-work")
        return self

    @allure.step("Посимвольное заполнение формы автомобиля")
    def fill_car_form(self, car_data):
        self.city_input.press_sequentially(car_data.city, delay=30)
        self.manufacture_input.press_sequentially(car_data.manufacture, delay=30)
        self.model_input.press_sequentially(car_data.model, delay=30)
        self.year_input.press_sequentially(str(car_data.year), delay=30)
        self.seats_input.press_sequentially(str(car_data.seats), delay=30)
        self.serial_number_input.press_sequentially(car_data.serial_number, delay=30)
        self.price_input.press_sequentially(str(car_data.price), delay=30)
        return self

    @allure.step("Отправка формы добавления автомобиля")
    def submit(self):
        self.submit_btn.click()
        return self
import os

from playwright.sync_api import Page, expect
import allure
from pages_playwright.base_playwright_page import BasePlaywrightPage


class AddCarPlaywrightPage(BasePlaywrightPage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Точные локаторы на основе реального DOM
        self.city_input = page.locator("#city")
        self.manufacture_input = page.locator("[name='manufacture']")
        self.model_input = page.locator("[name='model']")
        self.year_input = page.locator("[name='year']")

        # Выпадающие списки (стандартные HTML <select>)
        self.fuel_select = page.locator("select[name='fuel']")
        self.gear_select = page.locator("select[name='gear']")
        self.wd_select = page.locator("select[name='wheelsDrive']")
        self.car_class_select = page.locator("[name='carClass']")

        self.doors_input = page.locator("[name='doors']")
        self.seats_input = page.locator("[name='seats']")
        self.serial_number_input = page.locator("[name='serialNumber']")
        self.price_input = page.locator("[name='pricePerDay']")
        self.about_input = page.locator("[name='about']")

        self.submit_btn = page.locator("button[type='submit']")

    # В файле pages_playwright/add_car_playwright_page.py

    @allure.step("Открытие страницы добавления автомобиля")
    def open_add_car_page(self):
        # Используем прямой переход по URL, так как сессия/куки после логина уже сохранены в браузере
        self.open_url("/let-car-work")
        return self



    @allure.step("Заполнение формы автомобиля")
    def fill_car_form(self, car_data):
        # 1. Город (с автокомплитом по data-testid)
        self.city_input.click()
        self.city_input.press_sequentially(car_data.city, delay=30)
        try:
            dropdown_item = self.page.locator("mat-option, .dropdown-item, div[role='option']").first
            dropdown_item.wait_for(state="visible", timeout=3000)
            dropdown_item.click()
        except Exception:
            pass

        # 2. Текстовые поля
        self.manufacture_input.press_sequentially(car_data.manufacture, delay=30)
        self.model_input.press_sequentially(car_data.model, delay=30)
        self.year_input.press_sequentially(str(car_data.year), delay=30)

        # 3. Выпадающие списки (используем select_option, так как это теги <select>)
        # Обратите внимание на значения value в HTML: petrol, auto, FWD и т.д.
        try:
            self.fuel_select.select_option(value=car_data.fuel.lower())
        except Exception:
            self.fuel_select.select_option(label=car_data.fuel)

        try:
            gear_val = "auto" if "aut" in car_data.gear.lower() else "manual"
            self.gear_select.select_option(value=gear_val)
        except Exception:
            self.gear_select.select_option(label=car_data.gear)

        try:
            self.wd_select.select_option(value=car_data.wd)
        except Exception:
            pass

        # Car class — это инпут, а не селект в этом DOM!
        if hasattr(car_data, 'car_class'):
            self.car_class_select.press_sequentially(car_data.car_class, delay=30)

        # 4. Числовые поля и серийный номер
        if hasattr(car_data, 'doors') and car_data.doors:
            self.doors_input.press_sequentially(str(car_data.doors), delay=30)

        self.seats_input.press_sequentially(str(car_data.seats), delay=30)
        self.serial_number_input.press_sequentially(str(car_data.reg_number), delay=30)
        self.price_input.press_sequentially(str(car_data.price), delay=30)

        return self

    @allure.step("Отправка формы добавления автомобиля")
    def submit(self):
        # Перехватываем ответ от API при клике
        with self.page.expect_response("**/v1/cars**", timeout=5000) as response_info:
            expect(self.submit_btn).not_to_be_disabled(timeout=5000)
            self.submit_btn.click()

        response = response_info.value
        print(f"\n[DEBUG API] Status: {response.status}")
        print(f"[DEBUG API] Body: {response.text()}")
        return self

    @property
    def global_message_locator(self):
        # Ищем элемент, который содержит текст успешного ответа в DOM
        return self.page.locator("text='Car added successfully', .cdk-dialog-container, .modal-body, .message")

    @allure.step("Получение текста глобального сообщения")
    def get_global_message_text(self) -> str:
        return self.global_message_locator.inner_text().strip()

    @allure.step("Получение ошибок валидации формы")
    def get_form_errors(self) -> list:
        error_locators = self.page.locator(".error, mat-error, .alert-danger")
        return [error_locators.nth(i).inner_text() for i in range(error_locators.count()) if
                error_locators.nth(i).is_visible()]

    @allure.step("Загрузка фотографии автомобиля")
    def upload_photo(self, photo_path: str):
        if photo_path and os.path.exists(photo_path):
            self.page.locator("#photo-file").set_input_files(photo_path)
        return self
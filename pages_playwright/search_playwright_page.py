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
        self.no_results_message = page.locator(".no-results, :text('No cars found')")

        self.calendar_popover = page.locator(".daterange-popover, .rdrCalendar")
        self.next_month_btn = page.locator(".rdrNextButton")

    # --- НАВИГАЦИЯ ---
    @allure.step("Открытие страницы поиска")
    def open(self):
        self.open_url("/search")
        return self

    # --- ДЕЙСТВИЯ С ФОРМОЙ ПОИСКА ---
    @allure.step("Ввод города с подтверждением: {city}")
    def fill_city(self, city: str):
        # Очищаем поле и вводим название города побуквенно с небольшой задержкой
        self.city_input.click()
        self.city_input.fill("")
        self.city_input.press_sequentially(city, delay=100)

        # Даем время появиться выпадающему списку подсказок и выбираем первый вариант
        try:
            # Ждем появления элементов выпадающего списка (например, div или li в выпадайке)
            dropdown_option = self.page.locator(".pac-item, .dropdown-menu li, div[role='option'], ul li").first
            dropdown_option.wait_for(state="visible", timeout=4000)
            dropdown_option.click()
        except Exception:
            # Запасной вариант: если выпадайки нет, используем клавиатуру для подтверждения
            self.page.keyboard.press("ArrowDown")
            self.page.keyboard.press("Enter")

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
        expect(self.car_cards.first).to_be_visible(timeout=5000)
        return self

    @allure.step("Проверка наличия автомобиля с названием: {car_name}")
    def assert_car_present_by_name(self, car_name: str):
        car_element = self.page.locator(f"text={car_name}")
        expect(car_element).to_be_visible(timeout=5000)
        return self

    @allure.step("Проверка сообщения об отсутствии результатов")
    def assert_no_results(self):
        expect(self.no_results_message).to_be_visible(timeout=5000)
        return self

    # --- РАБОТА С КАЛЕНДАРЕМ ---
    @allure.step("Открытие календаря кликом по полю дат")
    def open_calendar(self):
        self.dates_input.click()
        expect(self.calendar_popover).to_be_visible(timeout=3000)
        return self

    @allure.step("Выбор дня в календаре: {day_number}")
    def click_day(self, day_number: int):
        xpath = f"//button[contains(@class, 'rdrDay') and not(contains(@class, 'rdrDayPassive')) and not(contains(@class, 'rdrDayDisabled')) and .//*[text()='{day_number}']]"
        day_locator = self.page.locator(xpath)
        day_locator.first.click()
        return self

    @allure.step("Выбор диапазона дат через календарь (на текущий месяц)")
    def select_dates_in_calendar(self, start_day: int, end_day: int):
        self.open_calendar()
        self.click_day(start_day)
        self.click_day(end_day)
        return self

    @allure.step("Получение текущего отображаемого месяца в календаре")
    def get_current_month(self) -> str:
        month_locator = self.page.locator(".rdrMonthName, .rdrMonth")
        return month_locator.first.inner_text().strip()

    @allure.step("Клик по кнопке следующего месяца")
    def click_next_month(self):
        next_btn = self.page.locator(".rdrNextButton")
        next_btn.click()
        return self

    @allure.step("Клик по кнопке предыдущего месяца")
    def click_prev_month(self):
        # Исправлена опечатка в селекторе (.rdrPprevButton -> .rdrPrevButton)
        prev_btn = self.page.locator(".rdrPrevButton")
        prev_btn.click()
        return self

    @allure.step("Ожидание смены месяца в календаре")
    def wait_for_month_to_change(self, old_month: str):
        month_locator = self.page.locator(".rdrMonthName, .rdrMonth").first
        expect(month_locator).not_to_have_text(old_month, timeout=5000)
        return self

    @allure.step("Проверка наличия автомобиля по серийному номеру в ссылке: {serial_number}")
    def assert_car_present_by_serial_number(self, serial_number: str):
        # Ищем ссылку, в URL которой содержится серийный номер
        car_element = self.page.locator(f"a[href*='/cars/{serial_number}']")
        expect(car_element).to_be_visible(timeout=5000)
        return self
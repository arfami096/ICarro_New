import os
import allure
import pytest
from playwright.sync_api import expect, TimeoutError

from pages_playwright.login_playwright_page import LoginPlaywrightPage
from pages_playwright.add_car_playwright_page import AddCarPlaywrightPage
from data.data_generator import CarGenerator

VALID_EMAIL = os.getenv("USER_EMAIL")
VALID_PASSWORD = os.getenv("USER_PASSWORD")
PHOTO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "car.jpg"))


@allure.epic("UI Testing Playwright")
@allure.feature("Add Car Page (Let the car work)")
@allure.story("Positive Add Car")
@allure.severity(allure.severity_level.BLOCKER)
def test_add_car_success(page):
    login_page = LoginPlaywrightPage(page)
    add_car_page = AddCarPlaywrightPage(page)

    with allure.step("Пререквизит: Авторизация"):
        login_page.open_login_form()
        login_page.fill_email(VALID_EMAIL)
        login_page.fill_password(VALID_PASSWORD)
        login_page.submit_login()

        # Закрываем модальное окно успешного входа, если оно появилось
        try:
            modal_ok_btn = page.locator(
                "div.modal-dialog button, div.modal-content button, .dialog-container button, button:has-text('Ok')")
            if modal_ok_btn.is_visible(timeout=3000):
                modal_ok_btn.first.click()
        except Exception:
            pass

        # Ждем, пока оверлей модалки пропадет с экрана
        overlay = page.locator("div.modal-overlay")
        if overlay.is_visible():
            overlay.wait_for(state="hidden", timeout=5000)

        # Гарантируем, что токен успел записаться в localStorage перед переходом к созданию машины
        page.wait_for_function("() => window.localStorage.getItem('token') !== null", timeout=5000)

    # Генерация данных автомобиля
    car = CarGenerator.get_random_car(photo_path=PHOTO_PATH)

    with allure.step("Заполнение формы добавления машины"):
        add_car_page.open_add_car_page()
        add_car_page.fill_car_form(car)
        add_car_page.upload_photo(car.photo_path)

        # Ожидаем успешного ответа от API при сабмите формы
        with page.expect_response(lambda response: "/v1/cars" in response.url and response.status == 200,
                                  timeout=10000) as response_info:
            add_car_page.submit()

    with allure.step("Проверка успешного ответа от сервера"):
        response = response_info.value
        assert response.status == 200, f"Ожидался статус 200, но получен {response.status}"
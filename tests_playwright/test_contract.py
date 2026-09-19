# tests_playwright/test_contract.py
import allure
import pytest
from data.cities_contract import UI_CITIES, SWAGGER_CITIES

@allure.epic("Contract Testing")
@allure.feature("API & UI Consistency")
@allure.story("Check cities synchronization between Frontend DOM and Swagger API")
@allure.severity(allure.severity_level.NORMAL)
def test_cities_contract_mismatches():
    # Нормализуем для анализа (приводим к нижнему регистру и сглаживаем разницу Qiryat/Kiryat)
    def normalize(name):
        return name.lower().replace("qiryat", "kiryat").replace("raanana", "ra'anana").replace("beer sheva", "beersheba").replace("modiin", "modi'in-maccabim-re'ut")

    ui_normalized = {normalize(c): c for c in UI_CITIES}
    swagger_normalized = {normalize(c): c for c in SWAGGER_CITIES}

    only_in_ui = [UI_CITIES[i] for key, i in [(normalize(c), idx) for idx, c in enumerate(UI_CITIES)] if key not in swagger_normalized]
    only_in_swagger = [SWAGGER_CITIES[i] for key, i in [(normalize(c), idx) for idx, c in enumerate(SWAGGER_CITIES)] if key not in ui_normalized]

    # Фиксируем баг рассинхрона, если он есть
    failure_messages = []
    if only_in_ui:
        failure_messages.append(f"[BUG] Эти города есть в UI, но отсутствуют в Swagger: {only_in_ui}")
    if only_in_swagger:
        failure_messages.append(f"[BUG] Эти города есть в Swagger, но отсутствуют в UI: {only_in_swagger}")

    if failure_messages:
        pytest.fail("\n".join(failure_messages))
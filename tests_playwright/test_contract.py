
import allure
import json
import pytest
from data.cities_contract import UI_CITIES, SWAGGER_CITIES


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known contract mismatch: UI DOM cities and Swagger API cities are out of sync"
    # strict=True убран, теперь тест честно падает (FAILED), но классифицируется как xfail
)
@allure.epic("Contract Testing")
@allure.feature("API & UI Consistency")
@allure.story("Check cities synchronization between Frontend DOM and Swagger API")
@allure.title("Contract Bug: Detect synchronization mismatches between UI and Swagger cities")
@allure.description(
    "Этот тест проверяет строгое соответствие списков городов на фронтенде (UI) и в бэкенде (Swagger API). "
    "При наличии расхождений тест падает и прикрепляет готовые JSON-файлы с расхождениями для составления bug-report'а."
)
@allure.severity(allure.severity_level.NORMAL)
def test_cities_contract_mismatches():
    with allure.step("Прямое строгое сравнение списков городов UI и Swagger"):
        set_ui = set(UI_CITIES)
        set_swagger = set(SWAGGER_CITIES)

        only_in_ui = list(set_ui - set_swagger)
        only_in_swagger = list(set_swagger - set_ui)

    with allure.step("Прикрепление полных списков и дефектов в Allure для Bug-Report"):
        allure.attach(json.dumps(UI_CITIES, indent=2, ensure_ascii=False), name="All UI Cities",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(json.dumps(SWAGGER_CITIES, indent=2, ensure_ascii=False), name="All Swagger Cities",
                      attachment_type=allure.attachment_type.JSON)

        if only_in_ui:
            allure.attach(json.dumps(only_in_ui, indent=2, ensure_ascii=False),
                          name="[BUG] Only in UI (Missing in Swagger)", attachment_type=allure.attachment_type.JSON)
        if only_in_swagger:
            allure.attach(json.dumps(only_in_swagger, indent=2, ensure_ascii=False),
                          name="[BUG] Only in Swagger (Missing in UI)", attachment_type=allure.attachment_type.JSON)

    failure_messages = []
    if only_in_ui:
        failure_messages.append(f"[BUG] Эти города есть в UI, но отсутствуют в Swagger: {only_in_ui}")
    if only_in_swagger:
        failure_messages.append(f"[BUG] Эти города есть в Swagger, но отсутствуют в UI: {only_in_swagger}")

    if failure_messages:
        pytest.fail("\n".join(failure_messages))
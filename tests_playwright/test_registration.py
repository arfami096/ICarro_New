import re
import allure
import pytest
from playwright.sync_api import Page, expect
from data.data_generator import UserGenerator, fake
from pages_playwright.registration_playwright_page import RegistrationPlaywrightPage


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Navigation")
@allure.title("Navigatsiya so stranicy na formu registracii")
@allure.severity(allure.severity_level.NORMAL)
def test_navigation_to_registration(reg_playwright_page, page: Page):
    with allure.step("Otkryt' glavnuyu stranicu prilozheniya"):
        reg_playwright_page.open_main_page()

    with allure.step("Kliknut' na knopku registracii v navigacionnom menyu"):
        reg_playwright_page.click_registration_button_in_menu()

    with allure.step("Proverit', chto tekushchiy URL soderzhit /register"):
        expect(page).to_have_url(re.compile(r".*/register"))


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Positive Registration")
@allure.title("Uspeshnaya registratsiya novogo polzovatelya (End-to-End)")
@allure.severity(allure.severity_level.BLOCKER)
def test_registration_success(reg_playwright_page):
    user = UserGenerator.get_random_user()

    with allure.step("Otkryt' formu registracii"):
        reg_playwright_page.open_registration_form()

    with allure.step(f"Zapolnit' formu validnymi dannymi: {user.email}"):
        reg_playwright_page.fill_registration_form(user)
        reg_playwright_page.set_policy_checkbox(True)

    with allure.step("Otpravit' formu registracii"):
        reg_playwright_page.submit_registration()

    with allure.step("Proverit' uspeshnyy tost/soobshchenie i zakrytie modalki/okna"):
        reg_playwright_page.assert_confirmation_text("Registered")
        reg_playwright_page.assert_confirmation_text_1("You are logged in success")
        reg_playwright_page.close_window()


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Negative Registration - Fields Validation")
@allure.title("Validatsiya obyazatelnyh poley i nekorrektnyh formatov")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "field_name, invalid_value, expected_error",
    [
        ("name", "", "Name is required"),
        pytest.param(
            "name", "A", "Name must be at least 2 characters",
            marks=pytest.mark.xfail(reason="BUG: UI ne trebuet minimum 2 simvola dlya imeni")
        ),
        ("last_name", "", "Last name is required"),
        ("email", "tonygmail.com", "Wrong email format"),
        ("email", "", "Email is required"),
        ("password", "P123$", "Password must contain minimum 6 symbols"),
        ("password", "", "Password is required"),
    ]
)
def test_registration_negative_fields(reg_playwright_page, field_name, invalid_value, expected_error):
    kwargs = {field_name: invalid_value}
    user = UserGenerator.get_random_user(**kwargs)

    with allure.step("Otkryt' formu registracii"):
        reg_playwright_page.open_registration_form()

    with allure.step(f"Zapolnit' formu nevalidnym znacheniem dlya '{field_name}': '{invalid_value}'"):
        reg_playwright_page.fill_registration_form(user)
        reg_playwright_page.set_policy_checkbox(True)
        reg_playwright_page.remove_focus()

    with allure.step(f"Proverit' tekst oshibki '{expected_error}'"):
        reg_playwright_page.assert_error_message(expected_error)

    with allure.step("Strogaya proverka: knopka Submit zablokirovana pri nalichii oshibok validatsii"):
        reg_playwright_page.assert_submit_button_disabled(disabled=True)


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Negative Registration - Checkbox")
@allure.title("Proverka obyazatelnosti chekboksa polzovatelskogo soglasheniya")
@allure.severity(allure.severity_level.NORMAL)
def test_registration_without_check_box(reg_playwright_page):
    user = UserGenerator.get_random_user()

    with allure.step("Otkryt' formu i zapolnit' validnye dannye"):
        reg_playwright_page.open_registration_form()
        reg_playwright_page.fill_registration_form(user)
        reg_playwright_page.set_policy_checkbox(True)

    with allure.step("Snyat' chekboks polzovatelskogo soglasheniya"):
        reg_playwright_page.set_policy_checkbox(False)
        reg_playwright_page.remove_focus()

    with allure.step("Proverit' oshibku i blokirovku otpravki"):
        reg_playwright_page.assert_error_message("You must accept the terms")
        reg_playwright_page.assert_submit_button_disabled(disabled=True)


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Edge Cases & Sanitization")
@allure.title("Proverka obrabotki probelov (whitespace) i UX-sanitizacii poley")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "name, last_name, email, password, expected",
    [
        pytest.param(
            "   ", "Smith", "valid@test.com", "Password123!", "Name is required",
            marks=pytest.mark.xfail(reason="BUG: UI ne pokazyvaet oshibku pri vvode odnih probelov v imya")
        ),
        pytest.param(
            "John", "   ", "valid@test.com", "Password123!", "Last name is required",
            marks=pytest.mark.xfail(reason="BUG: UI ne pokazyvaet oshibku pri vvode odnih probelov v familiyu")
        ),
        ("John", "Smith", "   ", "Password123!", "Email is required"),
        ("John", "Smith", "valid@test.com", "   ", "Password must contain minimum 6 symbols")
    ],
    ids=[
        "spaces_in_name",
        "spaces_in_lastname",
        "spaces_in_email",
        "spaces_in_password"
    ]
)
def test_registration_whitespace_handling(
        reg_playwright_page: RegistrationPlaywrightPage,
        name: str,
        last_name: str,
        email: str,
        password: str,
        expected: str
):
    with allure.step("Otkryt' formu registracii"):
        reg_playwright_page.open_registration_form()

    with allure.step("Vvesti dannye s uchetom probelnyh scenariev"):
        reg_playwright_page.fill_name(name)
        reg_playwright_page.fill_last_name(last_name)
        reg_playwright_page.fill_email(email)
        reg_playwright_page.fill_password(password)
        reg_playwright_page.set_policy_checkbox(True)
        reg_playwright_page.remove_focus()

    with allure.step(f"Ozhidaem oshibku validacii: '{expected}'"):
        reg_playwright_page.assert_error_message(expected)
        reg_playwright_page.assert_submit_button_disabled(disabled=True)


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Edge Cases & Sanitization")
@allure.title("Proverka otpravki probelov i perehvat Network Payload")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(
    reason="BUG [Data Sanitization]: Polya firstName i lastName ne obrezayut probely po krayam (otstutstvuet trim()), i uletayut na server v iskajennom vide."
)
def test_registration_whitespace_payload_interception(reg_playwright_page: RegistrationPlaywrightPage):
    with allure.step("Otkryt' formu registracii"):
        reg_playwright_page.open_registration_form()

    with allure.step("Vvesti imya i familiyu s probelami po krayam"):
        unique_email = fake.unique.email()

        reg_playwright_page.fill_name(" as ")
        reg_playwright_page.fill_last_name(" sdggs ")
        reg_playwright_page.fill_email(unique_email)
        reg_playwright_page.fill_password("Password123!")
        reg_playwright_page.set_policy_checkbox(True)
        reg_playwright_page.remove_focus()

    with allure.step("Otpravit' formu i perehvatit' Network Payload"):
        with reg_playwright_page.page.expect_request("**/v1/user/registration/usernamepassword") as request_info:
            reg_playwright_page.submit_registration()

        request = request_info.value
        payload = request.post_data_json

        assert payload.get("firstName") == " as ", f"Ozhidalos' ' as ', no uletelo: {payload.get('firstName')}"
        assert payload.get("lastName") == " sdggs ", f"Ozhidalos' ' sdggs ', no uletelo: {payload.get('lastName')}"

        allure.attach(str(payload), name="Intercepted Network Payload", attachment_type=allure.attachment_type.JSON)

    with allure.step("Proverka uspeshnogo otveta i poyavleniya okna Registered"):
        reg_playwright_page.assert_confirmation_text("Registered")


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Edge Cases & Sanitization")
@allure.title("Проверка отправки пробелов в Name/LastName и перехват ошибки 400 Bad Request от бэкенда")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(
    reason="BUG [UI/UX Validation]: Поля firstName и lastName при вводе одних пробелов не показывают подсказок на UI, а при сабмите фронтенд отображает нечитаемый тост '[object Object]' вместо нормальной ошибки."
)
def test_registration_whitespace_empty_fields_backend_validation(reg_playwright_page: RegistrationPlaywrightPage):
    with allure.step("Открыть форму регистрации"):
        reg_playwright_page.open_registration_form()

    with allure.step("Ввести пробелы в обязательные текстовые поля"):
        reg_playwright_page.fill_name("   ")
        reg_playwright_page.fill_last_name("   ")
        reg_playwright_page.fill_email("valid@test.com")
        reg_playwright_page.fill_password("Password123!")
        reg_playwright_page.set_policy_checkbox(True)
        reg_playwright_page.remove_focus()

    with allure.step("Отправить форму и перехватить ответ сервера (400 Bad Request)"):
        with reg_playwright_page.page.expect_response("**/v1/user/registration/usernamepassword") as response_info:
            reg_playwright_page.submit_registration()

        response = response_info.value
        assert response.status == 400, f"Ожидался статус 400, но пришел: {response.status}"

        response_json = response.json()
        assert "must not be blank" in str(
            response_json), f"Ожидалась ошибка бэкенда о пустоте полей, но пришло: {response_json}"

        allure.attach(str(response_json), name="Backend Error Response (400)",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить текущее бажное поведение UI (появление модалки с ошибкой)"):
        reg_playwright_page.assert_confirmation_text("Registration failed")


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Edge Cases & Sanitization")
@allure.title("Proverka avtomaticheskogo trim-a probelov dlya email")
@allure.severity(allure.severity_level.NORMAL)
def test_email_whitespace_trimming(reg_playwright_page: RegistrationPlaywrightPage):
    with allure.step("Otkryt' formu registracii"):
        reg_playwright_page.open_registration_file() if hasattr(reg_playwright_page, 'open_registration_file') else reg_playwright_page.open_registration_form()

    with allure.step("Vvesti email s probelami po krayam i ostalnye validnye dannye"):
        unique_prefix = fake.user_name()
        dirty_email = f"   {unique_prefix}@gmail.com   "
        expected_clean_email = f"{unique_prefix}@gmail.com"

        reg_playwright_page.fill_name("John")
        reg_playwright_page.fill_last_name("Smith")
        reg_playwright_page.fill_email(dirty_email)
        reg_playwright_page.fill_password("Password123!")
        reg_playwright_page.set_policy_checkbox(True)
        reg_playwright_page.remove_focus()

    with allure.step("Otpravit' formu i perehvatit' Network Payload dlya proverki ochistki email"):
        with reg_playwright_page.page.expect_request("**/v1/user/registration/usernamepassword") as request_info:
            reg_playwright_page.submit_registration()

        request = request_info.value
        payload = request.post_data_json

        assert payload.get("username") == expected_clean_email, (
            f"Ozhidalos', chto email otchistitsya do '{expected_clean_email}', "
            f"no uletel 'gрязный' variant: {payload.get('username')}"
        )

        allure.attach(str(payload), name="Cleaned Email Payload", attachment_type=allure.attachment_type.JSON)

    with allure.step("Proverka uspeshnogo otveta i poyavleniya okna Registered"):
        reg_playwright_page.assert_confirmation_text("Registered")


@pytest.mark.ui
@pytest.mark.regression
@allure.epic("UI Testing (Playwright)")
@allure.feature("Registration Page")
@allure.story("Edge Cases & Sanitization")
@allure.title("Proverka trim-a probelov dlya firstName i lastName (Ozhidaem ochistku)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail(
    reason="BUG [Data Sanitization]: Polya firstName i lastName ne obrezayut probely po krayam (otstutstvuet trim), poetomu test pahaet do ispravleniya na storone frontenda."
)
def test_registration_whitespace_should_be_trimmed(reg_playwright_page: RegistrationPlaywrightPage):
    with allure.step("Otkryt' formu registracii"):
        reg_playwright_page.open_registration_form()

    with allure.step("Vvesti imya i familiyu s probelami po krayam"):
        unique_email = fake.unique.email()

        dirty_name = " as "
        dirty_last_name = " sdggs "

        reg_playwright_page.fill_name(dirty_name)
        reg_playwright_page.fill_last_name(dirty_last_name)
        reg_playwright_page.fill_email(unique_email)
        reg_playwright_page.fill_password("Password123!")
        reg_playwright_page.set_policy_checkbox(True)
        reg_playwright_page.remove_focus()

    with allure.step("Otpravit' formu i perehvatit' Network Payload"):
        with reg_playwright_page.page.expect_request("**/v1/user/registration/usernamepassword") as request_info:
            reg_playwright_page.submit_registration()

        request = request_info.value
        payload = request.post_data_json

        sent_name = payload.get("firstName")
        sent_last_name = payload.get("lastName")

        allure.attach(str(payload), name="Intercepted Payload", attachment_type=allure.attachment_type.JSON)

        # Требуем чистое значение (без пробелов). Пока баг есть — тест упадет здесь и получит статус XFAIL.
        assert sent_name == dirty_name.strip(), (
            f"Ozhidalos' ochishennoe znachenie '{dirty_name.strip()}', no uletelo '{sent_name}'"
        )
        assert sent_last_name == dirty_last_name.strip(), (
            f"Ozhidalos' ochishennoe znachenie '{dirty_last_name.strip()}', no uletelo '{sent_last_name}'"
        )

    with allure.step("Proverka uspeshnogo otveta"):
        reg_playwright_page.assert_confirmation_text("Registered")
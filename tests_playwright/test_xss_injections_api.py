import allure
import pytest

from data.data_generator import UserGenerator

API_URL = "https://ilcarro-backend.herokuapp.com/v1/user/registration/usernamepassword"


@allure.epic("iCarro Platform")
@allure.feature("User Registration API")
@allure.story("Security & Sanitization")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "firstName, lastName, password, description, expected_status",
    [
        ("<script>alert(1)</script>", "Smith", "Password123!", "XSS in firstName", 400),
        ("John'--", "O'Connor", "Password123!", "SQLi/Apostrophe in names", [200, 201, 400]),
        # зависит от бизнес-логики
        ("John", "Smith", "   ", "Whitespace only password", 400),
        ("John", "Smith", "12345", "Too short password (5 chars)", 400),
    ],
    ids=["xss_firstname", "apostrophe_names", "whitespace_password", "short_password"]
)
def test_api_registration_security_and_edge_cases(page, firstName, lastName, password, description, expected_status):
    user = UserGenerator.get_random_user()
    payload = {
        "username": f"sec_{hash(description)}@test.com",
        "password": password,
        "firstName": firstName,
        "lastName": lastName,
    }

    with allure.step(f"Testcase: {description}"):
        response = page.request.post(API_URL, data=payload)

        # Если expected_status передан списком допустимых кодов
        if isinstance(expected_status, list):
            assert response.status in expected_status, f"Получен неожиданный статус {response.status}"
        else:
            assert response.status == expected_status, f"Ожидался {expected_status}, но пришел {response.status}"
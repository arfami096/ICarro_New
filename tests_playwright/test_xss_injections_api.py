import allure
import pytest

from data.data_generator import UserGenerator

API_URL = "https://ilcarro-backend.herokuapp.com/v1/user/registration/usernamepassword"


@pytest.mark.api
@pytest.mark.regression
@allure.epic("iCarro Platform")
@allure.feature("User Registration API")
@allure.story("Security & Sanitization")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "firstName, lastName, password, description, expected_status",
    [
        pytest.param(
            "<script>alert(1)</script>",
            "Smith",
            "Password123!",
            "XSS in firstName",
            400,
            marks=pytest.mark.xfail(
                reason="Known Security Bug: Backend accepts unescaped HTML/JS script in firstName instead of sanitizing or returning 400 Bad Request.",
                strict=False
            )
        ),
        ("John'--", "O'Connor", "Password123!", "SQLi/Apostrophe in names", [200, 201, 400]),
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

        if isinstance(expected_status, list):
            assert response.status in expected_status, f"Poluchen neozhidanniy status {response.status}"
        else:
            assert response.status == expected_status, f"Ozhidalsya {expected_status}, no prishel {response.status}"

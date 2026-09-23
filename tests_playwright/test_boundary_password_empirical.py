import pytest
import allure

API_URL = "https://ilcarro-backend.herokuapp.com/v1/user/registration/usernamepassword"


def generate_password_with_length(length: int) -> str:
    base = "Aa1!_val"
    if length < len(base):
        return "Aa1!123"[:length]
    return base + ("a" * (length - len(base)))


@pytest.mark.api
@pytest.mark.regression
@allure.epic("API Testing")
@allure.feature("Registration")
@pytest.mark.parametrize(
    "password_length, expected_status",
    [
        (5, 400),
        # Вот здесь точечно вешаем xfail на конкретные кейсы с багами:
        pytest.param(
            6, 200,
            marks=pytest.mark.xfail(reason="BUG-UI-01: UI says min 6, backend requires 8")
        ),
        pytest.param(
            7, 200,
            marks=pytest.mark.xfail(reason="BUG-UI-01: UI says min 6, backend requires 8")
        ),
        (8, [200, 201, 409]),
        (100, [200, 201, 409]),
        (256, [200, 201, 409]),
        pytest.param(
            500, 400,
            marks=pytest.mark.xfail(reason="BUG-SEC-02: Missing max length validation")
        ),
    ]
)
def test_password_boundary(page, password_length, expected_status):
    test_password = generate_password_with_length(password_length)
    payload = {
        "username": f"test_bound_{password_length}_{hash(test_password)}@test.com",
        "password": test_password,
        "firstName": "John",
        "lastName": "Smith"
    }

    response = page.request.post(API_URL, data=payload)
    response_json = response.json() if response.status != 500 else response.text

    if isinstance(expected_status, list):
        assert response.status in expected_status
    else:
        assert response.status == expected_status
import pytest
from playwright.sync_api import Page
from pages_playwright.registration_playwright_page import RegistrationPlaywrightPage
from pages_playwright.search_playwright_page import SearchPlaywrightPage
from pages_playwright.login_playwright_page  import LoginPlaywrightPage
from pages_playwright.add_car_playwright_page import AddCarPlaywrightPage

@pytest.fixture(autouse=True)
def setup_viewport(page: Page):
    # Установим большой размер окна, чтобы верстка не сжималась
    page.set_viewport_size({"width": 1440, "height": 900})

@pytest.fixture
def reg_playwright_page(page: Page) -> RegistrationPlaywrightPage:
    return RegistrationPlaywrightPage(page)


@pytest.fixture
def search_playwright_page(page: Page) -> SearchPlaywrightPage:
    return SearchPlaywrightPage(page)


@pytest.fixture
def login_playwright_page(page: Page) -> LoginPlaywrightPage:
    return LoginPlaywrightPage(page)


@pytest.fixture
def add_car_playwright_page(page: Page) -> AddCarPlaywrightPage:
    return AddCarPlaywrightPage(page)


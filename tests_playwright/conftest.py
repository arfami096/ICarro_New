import pytest
from playwright.sync_api import Page
from pages_playwright.registration_playwright_page import RegistrationPlaywrightPage
from pages_playwright.search_playwright_page import SearchPlaywrightPage
from pages_playwright.login_playwright_page  import LoginPlaywrightPage
from pages_playwright.add_car_playwright_page import AddCarPlaywrightPage



@pytest.fixture
def reg_page(page: Page) -> RegistrationPlaywrightPage:
    return RegistrationPlaywrightPage(page)


@pytest.fixture
def search_page(page: Page) -> SearchPlaywrightPage:
    return SearchPlaywrightPage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPlaywrightPage:
    return LoginPlaywrightPage(page)


@pytest.fixture
def add_car_page(page: Page) -> AddCarPlaywrightPage:
    return AddCarPlaywrightPage(page)


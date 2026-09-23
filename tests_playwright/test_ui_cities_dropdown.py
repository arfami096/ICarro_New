import pytest
from playwright.sync_api import Page

from tests_playwright.test_api_and_frontend_city_lists import matching_cities


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("city", matching_cities)
def test_dropdown_with_matching_cities(page: Page, city: str):
    """Тестируем выбор каждого совпадающего города в выпадающем списке"""
    page.goto("https://icarro-v1.netlify.app/search?page=0&size=10")

    input_selector = '#city'
    dropdown_selector = '[data-testid="city-dropdown"]'

    page.fill(input_selector, '')
    page.fill(input_selector, city)
    page.wait_for_selector(dropdown_selector)

    dropdown_content = page.locator(dropdown_selector).inner_text()

    assert city in dropdown_content, f"Город '{city}' не найден в выпадающем списке!"
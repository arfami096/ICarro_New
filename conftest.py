import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from dotenv import load_dotenv
from api.car_api import IlCarroAPI

# Загружаем переменные из .env
load_dotenv()


@pytest.fixture
def driver():
    is_headless = os.getenv('HEADLESS_MODE', 'false').lower() == 'true'
    is_ci = os.environ.get('CI') == 'true'
    driver_instance = None

    if is_ci:
        # CI-окружение (GitHub Actions) — строго Chrome Headless
        options = ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        driver_instance = webdriver.Chrome(options=options)
    else:
        # Локальная разработка: Каскадный запуск (Chrome -> Edge -> Safari)

        # 1. Сначала пробуем Chrome
        try:
            options = ChromeOptions()
            if is_headless:
                options.add_argument('--headless')
                options.add_argument('--window-size=1920,1080')
            driver_instance = webdriver.Chrome(options=options)
            print("\n[INFO] Браузер успешно запущен: Chrome")
        except Exception as e_chrome:
            print(f"\n[WARNING] Chrome не найден или не запущен: {e_chrome}. Пробуем Edge...")

            # 2. Если Chrome недоступен, пробуем Edge
            try:
                options = EdgeOptions()
                if is_headless:
                    options.add_argument('--headless')
                driver_instance = webdriver.Edge(options=options)
                print("\n[INFO] Браузер успешно запущен: Edge")
            except Exception as e_edge:
                print(f"\n[WARNING] Edge не найден или не запущен: {e_edge}. Пробуем Safari...")

                # 3. Если нет и Edge, запускаем Safari (родной для macOS)
                try:
                    driver_instance = webdriver.Safari()
                    print("\n[INFO] Браузер успешно запущен: Safari")
                except Exception as e_safari:
                    raise RuntimeError(
                        f"Не удалось запустить ни один доступный браузер!\n"
                        f"Chrome error: {e_chrome}\n"
                        f"Edge error: {e_edge}\n"
                        f"Safari error: {e_safari}"
                    )

        # Максимизируем окно (для Safari это работает иначе, поэтому обходим стороной)
        if not is_headless and driver_instance and type(driver_instance).__name__ != 'Safari':
            try:
                driver_instance.maximize_window()
            except Exception:
                pass

    driver_instance.implicitly_wait(5)
    yield driver_instance
    driver_instance.quit()


# --- АВТОМАТИЧЕСКИЕ СКРИНШОТЫ ПРИ ПАДЕНИИ ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            test_name = item.name.replace("/", "_").replace("::", "_")
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Скриншот ошибки: {test_name}",
                attachment_type=allure.attachment_type.PNG
            )


from api.car_api import IlCarroAPI


@pytest.fixture
def auth_api():
    """Фикстура, которая автоматически создает API-клиента и логинится"""
    api = IlCarroAPI()
    email = os.getenv("USER_EMAIL")
    password = os.getenv("USER_PASSWORD")

    with allure.step("Setup Fixture: Автоматическая API-авторизация"):
        api.login(email, password)

    return api
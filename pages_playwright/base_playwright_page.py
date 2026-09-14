from playwright.sync_api import Page


class BasePlaywrightPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://icarro-v1.netlify.app"

    def open_url(self, path: str = ""):
        """Открытие страницы относительно базового URL"""
        full_url = f"{self.base_url}{path}" if path.startswith("/") else f"{self.base_url}/{path}"
        self.page.goto(full_url, wait_until="domcontentloaded")
        return self

    def get_current_url(self) -> str:
        """Получение текущего URL"""
        return self.page.url

    def get_title(self) -> str:
        """Получение заголовка страницы (title)"""
        return self.page.title()

    def wait_for_dom(self):
        """Ожидание готовности DOM"""
        self.page.wait_for_load_state("domcontentloaded")
        return self
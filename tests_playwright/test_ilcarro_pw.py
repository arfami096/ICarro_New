from playwright.sync_api import Page, expect

def test_ilcarro_login_button(page: Page):
    page.goto("https://icarro-v1.netlify.app/")
    page.get_by_role("link", name="Log in").first.click()
    yalla_btn = page.locator("button[type='submit']")
    expect(yalla_btn).to_be_visible()

def test_ilcarro_login(page: Page):
    page.goto("https://icarro-v1.netlify.app/")
    page.get_by_role("link", name="Log in").first.click()

    # 1. Вводим твои РЕАЛЬНЫЕ данные для входа
    page.locator("input[type='email']").press_sequentially("arfami096@gmail.com", delay=100)
    page.locator("input[type='password']").press_sequentially("Jamalungma08!", delay=100)

    # 2. Ждем и кликаем Yalla!
    yalla_btn = page.locator("button[type='submit']")
    yalla_btn.wait_for(state="visible")
    yalla_btn.click()

    # 3. Кликаем OK в модалке подтверждения
    ok_btn = page.get_by_text("OK").first
    ok_btn.wait_for(state="visible", timeout=5000)
    ok_btn.click()

    # 4. Честная проверка: в шапке обязательно должен появиться элемент "Logout"
    logout_link = page.get_by_text("Log out").first
    expect(logout_link).to_be_visible()
import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://icarro-v1.netlify.app")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://ilcarro-backend.herokuapp.com/v1")
    API_REG_URL = f"{API_BASE_URL}/user/registration/usernamepassword"
    API_LOGIN_URL = f"{API_BASE_URL}/user/login/usernamepassword"

    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_PASSWORD = os.getenv("USER_PASSWORD")

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_TO = os.getenv("TELEGRAM_TO")


# Создаем экземпляр нашего класса конфигурации
config = Config()


def send_telegram_message(message: str):
    if not config.TELEGRAM_TOKEN or not config.TELEGRAM_TO:
        print("Telegram токен или чат ID не настроены в .env")
        return

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_TO,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Уведомление в Telegram успешно отправлено!")
    else:
        print(f"Ошибка отправки в Telegram: {response.text}")
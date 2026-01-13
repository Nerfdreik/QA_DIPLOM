import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Класс настроек приложения"""

    BASE_URL = "https://www.labirint.ru"
    API_BASE_URL = "https://www.labirint.ru"  

    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    API_RETRY_COUNT = int(os.getenv("API_RETRY_COUNT", "3"))

    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))

    DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
    SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
    LOGS_DIR = os.path.join(os.getcwd(), "logs")

    TEST_EMAIL = os.getenv("TEST_EMAIL", "")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")
    TEST_TOKEN = os.getenv("TEST_TOKEN", "")

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


settings = Settings()

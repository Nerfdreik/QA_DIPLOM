import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Конфигурационные настройки проекта."""

    BASE_URL: str = os.getenv("BASE_URL", "https://www.labirint.ru")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://www.labirint.ru/ajax")

    BROWSER: str = os.getenv("BROWSER", "chrome").lower()
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    WINDOW_WIDTH: int = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT: int = int(os.getenv("WINDOW_HEIGHT", "1080"))

    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    API_MAX_RETRIES: int = int(os.getenv("API_MAX_RETRIES", "3"))

    SCREENSHOTS_DIR: str = os.getenv("SCREENSHOTS_DIR", "screenshots")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "logs")

    SEARCH_QUERY_RUSSIAN: str = os.getenv("SEARCH_QUERY_RUSSIAN", "Властелин колец")
    SEARCH_QUERY_ENGLISH: str = os.getenv("SEARCH_QUERY_ENGLISH", "Harry Potter")
    SEARCH_QUERY_WITH_NUMBERS: str = os.getenv("SEARCH_QUERY_WITH_NUMBERS", "1984")

    VALID_EMAIL: Optional[str] = os.getenv("VALID_EMAIL")
    VALID_PASSWORD: Optional[str] = os.getenv("VALID_PASSWORD")
    API_KEY: Optional[str] = os.getenv("API_KEY")

    @classmethod
    def validate(cls) -> None:
        """Валидация настроек."""
        required_vars = ["BASE_URL"]
        missing = [var for var in required_vars if not getattr(cls, var)]

        if missing:
            raise ValueError(f"Отсутствуют обязательные настройки: {', '.join(missing)}")


settings = Settings()
settings.validate()

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Конфигурационные настройки проекта."""

    BASE_URL: str = os.getenv("BASE_URL", "https://demoqa.com/books")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://demoqa.com/BookStore/v1")

    TEST_USERNAME: str = os.getenv("TEST_USERNAME", "test_user")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "Test@123")
    TEST_API_KEY: Optional[str] = os.getenv("TEST_API_KEY")

    BROWSER: str = os.getenv("BROWSER", "chrome").lower()
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    API_MAX_RETRIES: int = int(os.getenv("API_MAX_RETRIES", "3"))

    SCREENSHOTS_DIR: str = "screenshots"
    LOGS_DIR: str = "logs"

    @classmethod
    def validate(cls) -> None:
        """Валидация настроек."""
        required_vars = ["BASE_URL", "TEST_USERNAME", "TEST_PASSWORD"]
        missing = [var for var in required_vars if not getattr(cls, var)]

        if missing:
            raise ValueError(f"Отсутствуют обязательные настройки: {', '.join(missing)}")


settings = Settings()

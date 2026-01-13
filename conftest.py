import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import settings


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для создания WebDriver.
    """
    options = Options()

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)

    yield driver

    driver.quit()



@pytest.fixture(scope="function")
def api_client():
    from api.api_client import APIClient
    return APIClient()

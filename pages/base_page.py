from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Tuple, List
from selenium.webdriver.remote.webelement import WebElement
import allure


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть URL: {url}")
    def open(self, url: str) -> None:
        self.driver.get(url)

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Найти элементы: {locator}")
    def find_elements(self, locator: Tuple[str, str], timeout: int = 10) -> List[WebElement]:
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator: Tuple[str, str]) -> None:
        element = self.find_element(locator)
        element.click()

    @allure.step("Ввести текст '{text}' в элемент: {locator}")
    def type_text(self, locator: Tuple[str, str], text: str) -> None:
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента: {locator}")
    def get_element_text(self, locator: Tuple[str, str]) -> str:
        return self.find_element(locator).text

    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Дождаться кликабельности элемента: {locator}")
    def wait_for_clickable(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Получить заголовок страницы")
    def get_page_title(self) -> str:
        return self.driver.title

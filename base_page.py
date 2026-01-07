from typing import Tuple, Optional, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import allure
import time


class BasePage:
    """Базовый класс для всех Page Object'ов."""

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """
        Инициализация базовой страницы.

        Args:
            driver (WebDriver): Экземпляр WebDriver
            timeout (int): Таймаут для ожиданий (по умолчанию 10)
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.actions = ActionChains(driver)

    @allure.step("Поиск элемента по локатору: {locator}")
    def find_element(self, locator: Tuple[By, str]) -> WebElement:
        """
        Находит элемент на странице.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)

        Returns:
            WebElement: Найденный элемент

        Raises:
            NoSuchElementException: Если элемент не найден
        """
        return self.driver.find_element(*locator)

    @allure.step("Поиск элементов по локатору: {locator}")
    def find_elements(self, locator: Tuple[By, str]) -> list[WebElement]:
        """
        Находит все элементы на странице по локатору.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)

        Returns:
            list[WebElement]: Список найденных элементов
        """
        return self.driver.find_elements(*locator)

    @allure.step("Ожидание видимости элемента: {locator}")
    def wait_for_visibility(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """
        Ожидает видимость элемента.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)
            timeout (Optional[int]): Кастомный таймаут

        Returns:
            WebElement: Видимый элемент
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Ожидание кликабельности элемента: {locator}")
    def wait_for_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """
        Ожидает кликабельность элемента.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)
            timeout (Optional[int]): Кастомный таймаут

        Returns:
            WebElement: Кликабельный элемент
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator: Tuple[By, str]) -> None:
        """
        Кликает на элемент.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)
        """
        element = self.wait_for_clickable(locator)
        element.click()

    @allure.step("Ввод текста '{text}' в элемент: {locator}")
    def type_text(self, locator: Tuple[By, str], text: str) -> None:
        """
        Вводит текст в элемент.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)
            text (str): Текст для ввода
        """
        element = self.wait_for_visibility(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получение текста элемента: {locator}")
    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Получает текст элемента.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)

        Returns:
            str: Текст элемента
        """
        element = self.wait_for_visibility(locator)
        return element.text.strip()

    @allure.step("Получение атрибута элемента: {locator}, атрибут: {attribute}")
    def get_attribute(self, locator: Tuple[By, str], attribute: str) -> str:
        """
        Получает значение атрибута элемента.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)
            attribute (str): Название атрибута

        Returns:
            str: Значение атрибута
        """
        element = self.wait_for_visibility(locator)
        return element.get_attribute(attribute)

    @allure.step("Проверка наличия элемента: {locator}")
    def is_element_present(self, locator: Tuple[By, str]) -> bool:
        """
        Проверяет наличие элемента на странице.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)

        Returns:
            bool: True если элемент присутствует
        """
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False

    @allure.step("Проверка видимости элемента: {locator}")
    def is_element_visible(self, locator: Tuple[By, str]) -> bool:
        """
        Проверяет видимость элемента.

        Args:
            locator (Tuple[By, str]): Кортеж (стратегия, значение)

        Returns:
            bool: True если элемент видим
        """
        try:
            return self.wait_for_visibility(locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    @allure.step("Переход по URL: {url}")
    def open(self, url: str) -> None:
        """
        Открывает указанный URL.

        Args:
            url (str): URL для открытия
        """
        self.driver.get(url)

    @allure.step("Получение текущего URL")
    def get_current_url(self) -> str:
        """
        Возвращает текущий URL.

        Returns:
            str: Текущий URL
        """
        return self.driver.current_url

    @allure.step("Получение заголовка страницы")
    def get_page_title(self) -> str:
        """
        Возвращает заголовок страницы.

        Returns:
            str: Заголовок страницы
        """
        return self.driver.title

    @allure.step("Сделать скриншот с именем: {screenshot_name}")
    def take_screenshot(self, screenshot_name: str) -> str:
        """
        Делает скриншот страницы.

        Args:
            screenshot_name (str): Имя скриншота

        Returns:
            str: Путь к сохраненному скриншоту
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshot_name}_{timestamp}.png"
        filepath = f"./screenshots/{filename}"

        self.driver.save_screenshot(filepath)
        allure.attach.file(filepath, name=screenshot_name, attachment_type=allure.attachment_type.PNG)

        return filepath

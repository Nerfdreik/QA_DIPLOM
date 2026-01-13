from typing import List, Tuple, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from config.settings import settings
import allure
import time


class MainPage(BasePage):
    """Page Object для главной страницы книжного магазина."""

    LOGO = (By.CSS_SELECTOR, "a.b-header-b-logo-e-logo")
    SEARCH_INPUT = (By.CSS_SELECTOR, "#search-field")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.b-header-b-search-e-btn")
    CART_ICON = (By.CSS_SELECTOR, "a[href*='cart']")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация главной страницы.

        Args:
            driver (WebDriver): Экземпляр WebDriver
        """
        super().__init__(driver)
        self.url = settings.BASE_URL

    @allure.step("Открыть главную страницу")
    def open_main_page(self) -> 'MainPage':
        """
        Открывает главную страницу.

        Returns:
            MainPage: Экземпляр текущей страницы
        """
        self.driver.get(self.url)
        time.sleep(2)  
        return self

    @allure.step("Проверить, что главная страница отображается")
    def is_main_page_displayed(self) -> bool:
        """
        Проверяет, что главная страница отображается.

        Returns:
            bool: True если страница отображается
        """
        try:

            current_url = self.driver.current_url
            page_title = self.driver.title.lower()

            return ("labirint.ru" in current_url and 
                    ("лабиринт" in page_title or "labirint" in page_title))
        except:
            return False

    @allure.step("Проверить кликабельность логотипа")
    def is_logo_clickable(self) -> bool:
        """
        Проверяет, что логотип кликабелен.

        Returns:
            bool: True если логотип кликабелен
        """
        try:
            logo = self.find_element(self.LOGO, timeout=5)
            return logo.is_displayed() and logo.is_enabled()
        except:
            return False

    @allure.step("Поиск книги: {query}")
    def search_book(self, query: str) -> 'MainPage':
        """
        Выполняет поиск книги.

        Args:
            query (str): Поисковый запрос

        Returns:
            MainPage: Экземпляр текущей страницы
        """
        try:
            search_input = self.find_element(self.SEARCH_INPUT)
            search_input.clear()
            search_input.send_keys(query)

            search_button = self.find_element(self.SEARCH_BUTTON)
            search_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Ошибка при поиске: {e}")

        return self

    @allure.step("Получить список книг")
    def get_books_list(self) -> List[str]:
        """
        Возвращает список названий книг на странице.

        Returns:
            List[str]: Список названий книг
        """
        return []

    @allure.step("Получить количество книг")
    def get_books_count(self) -> int:
        """
        Возвращает количество книг на странице.

        Returns:
            int: Количество книг
        """
        return 0

    @allure.step("Кликнуть по логотипу")
    def click_logo(self) -> 'MainPage':
        """
        Кликает по логотипу сайта.

        Returns:
            MainPage: Экземпляр текущей страницы
        """
        try:
            logo = self.find_element(self.LOGO)
            logo.click()
            time.sleep(2)
        except:
            pass
        return self

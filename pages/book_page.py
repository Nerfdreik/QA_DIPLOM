from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from base_page import BasePage
import allure
from config import test_data


class BookPage(BasePage):
    """Page Object для страницы книги."""

    BOOK_TITLE: Tuple[By, str] = (By.CSS_SELECTOR, "#title-wrapper .mr-2")
    BOOK_AUTHOR: Tuple[By, str] = (By.CSS_SELECTOR, "#author-wrapper .mr-2")
    BOOK_PUBLISHER: Tuple[By, str] = (By.CSS_SELECTOR, "#publisher-wrapper .mr-2")
    BOOK_ISBN: Tuple[By, str] = (By.CSS_SELECTOR, "#isbn-wrapper .mr-2")
    BOOK_PAGES: Tuple[By, str] = (By.CSS_SELECTOR, "#pages-wrapper .mr-2")
    BOOK_DESCRIPTION: Tuple[By, str] = (By.CSS_SELECTOR, "#description-wrapper .mr-2")
    BOOK_WEBSITE: Tuple[By, str] = (By.CSS_SELECTOR, "#website-wrapper .mr-2")
    ADD_TO_CART_BUTTON: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["add_to_cart_button"])
    BACK_TO_BOOKSTORE_BUTTON: Tuple[By, str] = (By.CSS_SELECTOR, "button:text('Back To Book Store')")

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы книги.

        Args:
            driver (WebDriver): Экземпляр WebDriver
        """
        super().__init__(driver)

    @allure.step("Получить информацию о книге")
    def get_book_info(self) -> dict:
        """
        Получает полную информацию о книге.

        Returns:
            dict: Словарь с информацией о книге
        """
        return {
            "title": self.get_text(self.BOOK_TITLE),
            "author": self.get_text(self.BOOK_AUTHOR),
            "publisher": self.get_text(self.BOOK_PUBLISHER),
            "isbn": self.get_text(self.BOOK_ISBN),
            "pages": self.get_text(self.BOOK_PAGES),
            "description": self.get_text(self.BOOK_DESCRIPTION),
            "website": self.get_text(self.BOOK_WEBSITE),
        }

    @allure.step("Получить название книги")
    def get_book_title(self) -> str:
        """
        Получает название книги.

        Returns:
            str: Название книги
        """
        return self.get_text(self.BOOK_TITLE)

    @allure.step("Получить автора книги")
    def get_book_author(self) -> str:
        """
        Получает автора книги.

        Returns:
            str: Автор книги
        """
        return self.get_text(self.BOOK_AUTHOR)

    @allure.step("Получить ISBN книги")
    def get_book_isbn(self) -> str:
        """
        Получает ISBN книги.

        Returns:
            str: ISBN книги
        """
        return self.get_text(self.BOOK_ISBN)

    @allure.step("Добавить книгу в корзину")
    def add_to_cart(self) -> None:
        """
        Добавляет книгу в корзину.
        """
        self.click(self.ADD_TO_CART_BUTTON)

    @allure.step("Проверить, что кнопка 'Добавить в корзину' активна")
    def is_add_to_cart_button_enabled(self) -> bool:
        """
        Проверяет, что кнопка добавления в корзину активна.

        Returns:
            bool: True если кнопка активна
        """
        return self.wait_for_clickable(self.ADD_TO_CART_BUTTON).is_enabled()

    @allure.step("Вернуться в книжный магазин")
    def back_to_bookstore(self) -> None:
        """
        Возвращается в книжный магазин.
        """
        self.click(self.BACK_TO_BOOKSTORE_BUTTON)

    @allure.step("Проверить полную информацию о книге")
    def verify_book_information_complete(self) -> bool:
        """
        Проверяет, что вся информация о книге присутствует.

        Returns:
            bool: True если вся информация присутствует
        """
        info = self.get_book_info()
        required_fields = ["title", "author", "isbn", "description"]

        for field in required_fields:
            if not info.get(field):
                return False

        return True

from typing import Dict, Any, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from config.test_data import test_data
import allure


class BookPage(BasePage):
    """Page Object для страницы книги."""

    BOOK_TITLE: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_title"])
    BOOK_AUTHOR: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_author"])
    BOOK_PRICE: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_price"])
    BOOK_OLD_PRICE: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_old_price"])
    BOOK_DESCRIPTION: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_description"])
    BOOK_COVER: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_cover"])

    ADD_TO_CART_BUTTON: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["add_to_cart_button"])
    ADD_TO_WISHLIST_BUTTON: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["add_to_wishlist_button"])
    READ_FRAGMENT_BUTTON: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["read_fragment_button"])

    BOOK_RATING: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_rating"])
    BOOK_REVIEWS: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_reviews"])
    BOOK_SERIES: Tuple[By, str] = (By.XPATH, test_data.LOCATORS["book_series"])

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы книги.

        Args:
            driver (WebDriver): Экземпляр WebDriver
        """
        super().__init__(driver)

    @allure.step("Получить информацию о книге")
    def get_book_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию о книге.

        Returns:
            Dict[str, Any]: Словарь с информацией о книге
        """
        info = {}

        try:
            info["title"] = self.get_element_text(self.BOOK_TITLE)
        except:
            info["title"] = "Не найдено"

        try:
            info["author"] = self.get_element_text(self.BOOK_AUTHOR)
        except:
            info["author"] = "Не найдено"

        try:
            info["price"] = self.get_element_text(self.BOOK_PRICE)
        except:
            info["price"] = "Не найдено"

        try:
            info["old_price"] = self.get_element_text(self.BOOK_OLD_PRICE)
        except:
            info["old_price"] = "Не найдено"

        try:
            info["description"] = self.get_element_text(self.BOOK_DESCRIPTION)
        except:
            info["description"] = "Не найдено"

        return info

    @allure.step("Проверить наличие кнопки 'Добавить в корзину'")
    def is_add_to_cart_button_present(self) -> bool:
        """
        Проверяет наличие кнопки добавления в корзину.

        Returns:
            bool: True если кнопка присутствует
        """
        return self.is_element_visible(self.ADD_TO_CART_BUTTON, timeout=3)

    @allure.step("Нажать кнопку 'Добавить в корзину'")
    def click_add_to_cart(self) -> None:
        """
        Нажимает кнопку добавления в корзину.
        """
        self.click(self.ADD_TO_CART_BUTTON)

    @allure.step("Добавить книгу в корзину")
    def add_book_to_cart(self) -> bool:
        """
        Добавляет книгу в корзину.

        Returns:
            bool: True если книга успешно добавлена
        """
        if self.is_add_to_cart_button_present():
            self.click_add_to_cart()
            return True
        return False

    @allure.step("Проверить отображение цены")
    def is_price_displayed(self) -> bool:
        """
        Проверяет отображение цены книги.

        Returns:
            bool: True если цена отображается
        """
        return self.is_element_visible(self.BOOK_PRICE)

    @allure.step("Получить цену книги")
    def get_book_price(self) -> str:
        """
        Возвращает цену книги.

        Returns:
            str: Цена книги
        """
        try:
            return self.get_element_text(self.BOOK_PRICE)
        except:
            return "Не найдено"

    @allure.step("Проверить, что вся информация о книге отображается")
    def verify_book_information_complete(self) -> bool:
        """
        Проверяет, что вся основная информация о книге отображается.

        Returns:
            bool: True если вся информация отображается
        """
        info = self.get_book_info()

        return all([
            info["title"] != "Не найдено",
            info["author"] != "Не найдено",
            info["price"] != "Не найдено"
        ])

    @allure.step("Проверить наличие обложки книги")
    def is_book_cover_displayed(self) -> bool:
        """
        Проверяет наличие обложки книги.

        Returns:
            bool: True если обложка отображается
        """
        return self.is_element_visible(self.BOOK_COVER)

    @allure.step("Проверить наличие описания книги")
    def is_description_displayed(self) -> bool:
        """
        Проверяет наличие описания книги.

        Returns:
            bool: True если описание отображается
        """
        return self.is_element_visible(self.BOOK_DESCRIPTION)

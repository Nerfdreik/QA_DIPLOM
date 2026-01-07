from typing import List, Tuple, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from base_page import BasePage
import allure


class MainPage(BasePage):
    """Page Object для главной страницы книжного магазина."""

    LOGO: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["logo"])
    SEARCH_INPUT: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["search_input"])
    SEARCH_BUTTON: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["search_button"])
    BOOK_LIST: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["book_list"])
    BOOK_ITEMS: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["book_item"])
    BOOK_TITLES: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["book_title_in_list"])
    LOGIN_BUTTON: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["login_button"])
    CART_ICON: Tuple[By, str] = (By.CSS_SELECTOR, test_data.LOCATORS["cart_icon"])

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
        self.open(self.url)
        return self

    @allure.step("Кликнуть по логотипу")
    def click_logo(self) -> 'MainPage':
        """
        Кликает по логотипу сайта.

        Returns:
            MainPage: Экземпляр текущей страницы
        """
        self.click(self.LOGO)
        return self

    @allure.step("Проверить кликабельность логотипа")
    def is_logo_clickable(self) -> bool:
        """
        Проверяет, что логотип кликабелен.

        Returns:
            bool: True если логотип кликабелен
        """
        try:
            return self.wait_for_clickable(self.LOGO).is_enabled()
        except Exception:
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
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        return self

    @allure.step("Получить список книг")
    def get_books_list(self) -> List[str]:
        """
        Возвращает список названий книг на странице.

        Returns:
            List[str]: Список названий книг
        """
        books = self.find_elements(self.BOOK_TITLES)
        return [book.text for book in books]

    @allure.step("Получить количество книг")
    def get_books_count(self) -> int:
        """
        Возвращает количество книг на странице.

        Returns:
            int: Количество книг
        """
        books = self.find_elements(self.BOOK_ITEMS)
        return len(books)

    @allure.step("Кликнуть по книге с названием: {book_title}")
    def click_book_by_title(self, book_title: str) -> None:
        """
        Кликает по книге с указанным названием.

        Args:
            book_title (str): Название книги
        """
        book_locator = (By.XPATH, f"//a[text()='{book_title}']")
        self.click(book_locator)

    @allure.step("Перейти на страницу логина")
    def go_to_login_page(self) -> None:
        """
        Переходит на страницу логина.
        """
        self.click(self.LOGIN_BUTTON)

    @allure.step("Проверить отображение главной страницы")
    def is_main_page_displayed(self) -> bool:
        """
        Проверяет, что главная страница отображается.

        Returns:
            bool: True если страница отображается
        """
        return (
            self.is_element_visible(self.LOGO) and
            self.is_element_visible(self.BOOK_LIST) and
            test_data.UI_TEST_DATA["expected_page_title"] in self.get_page_title()
        )

    @allure.step("Проверить реакцию кнопок")
    def check_buttons_responsiveness(self) -> bool:
        """
        Проверяет реакцию кнопок на странице.

        Returns:
            bool: True если все кнопки реагируют
        """
        buttons_to_check = [
            self.LOGIN_BUTTON,
            self.SEARCH_BUTTON,
        ]

        for button in buttons_to_check:
            if not self.is_element_visible(button):
                return False
            if not self.wait_for_clickable(button).is_enabled():
                return False

        return True

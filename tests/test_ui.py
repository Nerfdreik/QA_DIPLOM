import pytest
import allure
from typing import Dict, Any
from selenium.webdriver.remote.webdriver import WebDriver
from main_page import MainPage
from book_page import BookPage
import time


@pytest.mark.ui
@allure.feature("UI Тесты")
@allure.story("Главная страница")
class TestMainPage:
    """Тесты главной страницы книжного магазина."""

    @allure.title("Тест 1: Открытие главной страницы")
    @allure.description("Тест проверяет успешное открытие главной страницы книжного магазина")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_open_main_page(self, driver: WebDriver) -> None:
        """
        Тест открытия главной страницы.

        Args:
            driver (WebDriver): Фикстура WebDriver
        """
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open_main_page()

            current_url = main_page.get_current_url()
            page_title = main_page.get_page_title()

            allure.attach(
                f"URL: {current_url}\nTitle: {page_title}",
                name="Page Info",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверить, что страница открылась"):
            assert main_page.is_main_page_displayed(), "Главная страница не отображается"
            assert test_data.UI_TEST_DATA["expected_page_title"] in page_title, \
                f"Заголовок страницы не соответствует ожидаемому"

    @allure.title("Тест 2: Реакция кнопок на главной странице")
    @allure.description("Тест проверяет, что все кнопки на главной странице кликабельны и реагируют на действия")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_buttons_responsiveness(self, driver: WebDriver) -> None:
        """
        Тест реакции кнопок на главной странице.

        Args:
            driver (WebDriver): Фикстура WebDriver
        """
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open_main_page()

        with allure.step("Проверить реакцию кнопок"):
            buttons_are_responsive = main_page.check_buttons_responsiveness()
            assert buttons_are_responsive, "Не все кнопки реагируют на действия"

    @allure.title("Тест 3: Кликабельность логотипа сайта")
    @allure.description("Тест проверяет, что логотип сайта кликабелен и ведет на главную страницу")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logo_clickable(self, driver: WebDriver) -> None:
        """
        Тест кликабельности логотипа.

        Args:
            driver (WebDriver): Фикстура WebDriver
        """
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open_main_page()
            initial_url = main_page.get_current_url()

        with allure.step("Кликнуть по логотипу"):
            assert main_page.is_logo_clickable(), "Логотип не кликабелен"
            main_page.click_logo()
            time.sleep(1)  # Дать время для перехода

            new_url = main_page.get_current_url()

            allure.attach(
                f"Initial URL: {initial_url}\nNew URL: {new_url}",
                name="URL Before and After Click",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверить, что остались на главной странице"):
            assert main_page.is_main_page_displayed(), "После клика по логотипу не остались на главной странице"

    @allure.title("Тест 4: Поиск и отображение информации о книге")
    @allure.description("Тест проверяет поиск книги и отображение полной информации о ней")
    @allure.severity(allure.severity_level.NORMAL)
    def test_book_information_display(self, driver: WebDriver) -> None:
        """
        Тест отображения информации о книге.

        Args:
            driver (WebDriver): Фикстура WebDriver
        """
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open_main_page()

        with allure.step("Найти книгу по названию"):
            book_title = test_data.UI_TEST_DATA["book_title"]
            main_page.search_book(book_title)
            time.sleep(2)

            books_list = main_page.get_books_list()
            assert len(books_list) > 0, "Книги не найдены"
            assert book_title in books_list, f"Книга '{book_title}' не найдена в результатах поиска"

        with allure.step("Открыть страницу книги"):
            main_page.click_book_by_title(book_title)
            book_page = BookPage(driver)
            time.sleep(2)

        with allure.step("Проверить информацию о книге"):
            book_info = book_page.get_book_info()

            allure.attach(
                str(book_info),
                name="Book Information",
                attachment_type=allure.attachment_type.JSON,
            )

            assert book_info["title"] == book_title, "Название книги не совпадает"
            assert book_info["author"] == test_data.UI_TEST_DATA["book_author"], "Автор книги не совпадает"
            assert book_info["isbn"] == test_data.UI_TEST_DATA["book_isbn"], "ISBN книги не совпадает"
            assert book_page.verify_book_information_complete(), "Не вся информация о книге отображается"

    @allure.title("Тест 5: Отображение цены книги")
    @allure.description("Тест проверяет корректное отображение цены книги на странице")
    @allure.severity(allure.severity_level.NORMAL)
    def test_book_price_display(self, driver: WebDriver) -> None:
        """
        Тест отображения цены книги.

        Args:
            driver (WebDriver): Фикстура WebDriver
        """
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open_main_page()

        with allure.step("Найти книгу по названию"):
            book_title = test_data.UI_TEST_DATA["book_title"]
            main_page.search_book(book_title)
            time.sleep(2)

            books_count = main_page.get_books_count()
            assert books_count > 0, "Книги не найдены"

        with allure.step("Открыть страницу книги"):
            main_page.click_book_by_title(book_title)
            book_page = BookPage(driver)
            time.sleep(2)

        with allure.step("Проверить информацию о книге"):
            book_info = book_page.get_book_info()

            assert book_info.get("description"), "Отсутствует описание книги"

            allure.attach(
                f"Book Info: {book_info}",
                name="Book Details",
                attachment_type=allure.attachment_type.TEXT,
            )

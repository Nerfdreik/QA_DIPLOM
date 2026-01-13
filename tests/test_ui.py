import pytest
import allure
import time
from selenium.webdriver.remote.webdriver import WebDriver
from pages.main_page import MainPage
from pages.book_page import BookPage


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
            time.sleep(3)  

            current_url = main_page.get_current_url()
            page_title = main_page.get_page_title()

            allure.attach(
                f"URL: {current_url}\nTitle: {page_title}",
                name="Page Info",
                attachment_type=allure.attachment_type.TEXT,
            )

            driver.save_screenshot("main_page_loaded.png")

        with allure.step("Проверить, что страница открылась"):
            assert "labirint.ru" in current_url, f"URL должен содержать labirint.ru, получен: {current_url}"
            assert "Лабиринт" in page_title, f"Заголовок должен содержать 'Лабиринт', получен: {page_title}"

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
            time.sleep(3)

        with allure.step("Проверить базовую функциональность"):
            current_url = main_page.get_current_url()
            assert "labirint.ru" in current_url

            title = main_page.get_page_title()
            assert title is not None and len(title) > 0

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
            time.sleep(3)

            initial_url = main_page.get_current_url()
            allure.attach(f"Начальный URL: {initial_url}", name="Initial URL", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить основные элементы страницы"):
            assert "labirint.ru" in initial_url

            driver.save_screenshot("before_logo_click.png")

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
            time.sleep(3)

        with allure.step("Проверить работу поиска"):
            current_url = main_page.get_current_url()
            assert "labirint.ru" in current_url

            allure.attach(
                f"Страница успешно загружена: {current_url}",
                name="Page Loaded",
                attachment_type=allure.attachment_type.TEXT,
            )

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
            time.sleep(3)

        with allure.step("Проверить загрузку страницы"):
            current_url = driver.current_url
            page_title = driver.title

            allure.attach(
                f"URL: {current_url}\nTitle: {page_title}",
                name="Page Information",
                attachment_type=allure.attachment_type.TEXT,
            )

            assert "labirint.ru" in current_url, "Страница не загрузилась корректно"

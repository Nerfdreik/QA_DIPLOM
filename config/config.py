from typing import Dict, Any


class TestData:
    """Тестовые данные для проекта."""

    UI_TEST_DATA: Dict[str, Any] = {
        "search_queries": {
            "russian": "Властелин колец",
            "english": "Harry Potter",
            "with_numbers": "1984",
            "empty": "",
            "special_chars": "Test@Book#123"
        },
        "expected_titles": {
            "main_page": "Лабиринт – книжный магазин: купить книги, учебники, подарки",
            "search_results": "Поиск"
        },
        "book_info_selectors": {
            "title": "//h1[@itemprop='name']",
            "author": "//div[@class='authors']//a",
            "price": "//div[@class='buying-price']//span[@class='buying-price-val-number']",
            "isbn": "//div[contains(text(), 'ISBN')]/following-sibling::div",
            "publisher": "//div[contains(text(), 'Издательство')]/following-sibling::div//a"
        }
    }

    API_TEST_DATA: Dict[str, Any] = {
        "search_endpoints": {
            "autocomplete": "/search/autocomplete-jquery.php",
            "search": "/search/",
            "quick_search": "/search/quicksearch/"
        },
        "search_test_cases": [
            {"query": "война и мир", "description": "Кириллица, классика"},
            {"query": "harry potter", "description": "Латиница, современная литература"},
            {"query": "451 градус по фаренгейту", "description": "Цифры в названии"},
            {"query": "", "description": "Пустой запрос"},
            {"query": "   ", "description": "Пробелы"}
        ],
        "api_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Requested-With": "XMLHttpRequest"
        }
    }

    LOCATORS: Dict[str, str] = {
        "logo": "//a[@class='b-header-b-logo-e-logo']",
        "search_input": "//input[@id='search-field']",
        "search_button": "//button[@type='submit' and @class='b-header-b-search-e-btn']",
        "cart_icon": "//a[@class='b-header-b-personal-e-link top-link-cart']",

        "book_title": "//h1[@itemprop='name']",
        "book_author": "//div[@class='authors']//a",
        "book_price": "//div[@class='buying-price']//span[@class='buying-price-val-number']",
        "book_old_price": "//span[@class='buying-priceold-val-number']",
        "book_description": "//div[@id='product-about']//p",
        "book_cover": "//img[@id='product-image']",

        "search_results": "//div[@class='product need-watch watched']",
        "search_result_title": ".//a[@class='product-title-link']",
        "search_result_author": ".//div[@class='product-author']//a",
        "search_result_price": ".//span[@class='price-val']//span",

        "main_menu": "//div[@class='b-header-b-menu-e-list']",
        "user_menu": "//div[@class='b-header-b-personal-e-list']"
    }


test_data = TestData()

from typing import Dict, Any, List


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
        "expected_page_title": "Лабиринт – книжный магазин: купить книги, учебники, подарки",
        "book_title": "Мастер и Маргарита",
        "book_author": "Михаил Булгаков",
        "book_isbn": "978-5-17-080115-2",
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
        "login_button": "//a[contains(@class, 'js-b-autofade-wrap')]",
        "main_menu": "//div[@class='b-header-b-menu-e-list']",
        "user_menu": "//div[@class='b-header-b-personal-e-list']",

        "book_list": "//div[contains(@class, 'product') and contains(@class, 'need-watch')]",
        "book_item": ".//div[contains(@class, 'product')]",
        "book_title_in_list": ".//a[contains(@class, 'product-title-link')]",

        "book_title": "//h1[@itemprop='name']",
        "book_author": "//div[@class='authors']//a",
        "book_price": "//div[@class='buying-price']//span[@class='buying-price-val-number']",
        "book_old_price": "//span[@class='buying-priceold-val-number']",
        "book_description": "//div[@id='product-about']//p",
        "book_cover": "//img[@id='product-image']",

        "add_to_cart_button": "//a[contains(@class, 'btn-buy')]",
        "add_to_wishlist_button": "//a[contains(@class, 'favorite')]",
        "read_fragment_button": "//a[contains(@class, 'btn-read')]",
        "book_rating": "//div[@class='rating']",
        "book_reviews": "//div[@class='reviews']",
        "book_series": "//div[contains(text(), 'Серия:')]/following-sibling::a",

        "search_results": "//div[@class='product need-watch watched']",
        "search_result_title": ".//a[@class='product-title-link']",
        "search_result_author": ".//div[@class='product-author']//a",
        "search_result_price": ".//span[@class='price-val']//span",

        "cart_items": "//div[@class='basket-list-items']",
        "cart_item_title": ".//a[@class='basket-list-item-link']",
        "cart_item_price": ".//span[@class='basket-list-item-price']",
        "cart_total": "//div[@class='basket-order-total']",

        "modal_window": "//div[contains(@class, 'modal-container')]",
        "close_modal_button": "//button[contains(@class, 'js-close-modal')]",

        "pagination": "//div[@class='pagination-number']",
        "next_page": "//a[contains(@class, 'pagination-next')]",
        "prev_page": "//a[contains(@class, 'pagination-prev')]"
    }


test_data = TestData()

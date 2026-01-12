from typing import Dict, Any, List


class TestData:
    """Тестовые данные для проекта."""

    UI_TEST_DATA: Dict[str, Any] = {
        "book_title": "Designing Evolvable Web APIs with ASP.NET",
        "book_author": "Glenn Block et al.",
        "book_isbn": "9781449337711",
        "book_price": "$20.00",
        "expected_page_title": "Book Store",
    }

    API_TEST_DATA: Dict[str, Any] = {
        "valid_book_isbn": "9781449337711",
        "invalid_book_isbn": "0000000000000",
        "new_user": {
            "userName": "test_user_001",
            "password": "Test@123456"
        },
        "book_to_add": {
            "userId": "test-user-id",
            "collectionOfIsbns": [
                {"isbn": "9781449337711"}
            ]
        }
    }

    NEGATIVE_TEST_DATA: Dict[str, Any] = {
        "invalid_credentials": [
            {"username": "invalid_user", "password": "wrong_pass"},
            {"username": "", "password": "Test@123"},
            {"username": "test_user", "password": ""},
        ],
        "invalid_search_queries": [
            "",
            "   ",
            "non_existent_book_12345",
        ]
    }

    LOCATORS: Dict[str, str] = {
        "logo": ".logo",
        "search_input": "#searchBox",
        "search_button": "button[type='submit']",
        "book_list": ".rt-tbody",
        "book_item": ".rt-tr-group",
        "book_title_in_list": ".action-buttons a",
        "book_author": ".rt-td:nth-child(3)",
        "book_price": ".rt-td:nth-child(5)",
        "add_to_cart_button": "text=Add To Your Collection",
        "cart_icon": ".fa-shopping-cart",
        "login_button": "#login",
        "username_input": "#userName",
        "password_input": "#password",
    }


test_data = TestData()

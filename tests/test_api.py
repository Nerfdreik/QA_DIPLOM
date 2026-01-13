import pytest
import allure
import json
from api.api_client import APIClient


@pytest.mark.api
@allure.feature("API Тесты")
@allure.story("Поиск книг")
class TestLabirintAPI:
    """API тесты для сайта Лабиринт."""

    @allure.title("API Тест 1: Поиск книг на кириллице")
    @allure.description("Тест проверяет поиск книг с использованием кириллицы в запросе")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_cyrillic(self, api_client: APIClient) -> None:
        """
        Тест поиска книг на кириллице.

        Args:
            api_client (APIClient): Фикстура API клиента
        """
        test_queries = [
            "война и мир",
            "преступление и наказание",
            "мастер и маргарита",
            "евгений онегин",
            "анна каренина"
        ]

        results = []

        for query in test_queries:
            with allure.step(f"Поиск книги: '{query}'"):
                response = api_client.search_books(query)

                result_info = {
                    "query": query,
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "content_type": response.headers.get("Content-Type", ""),
                    "content_length": len(response.content) if response.content else 0
                }

                if result_info["success"]:
                    content = response.text
                    result_info["has_html_structure"] = "<!DOCTYPE html>" in content or "<html" in content
                    result_info["contains_search_results"] = "search-result" in content or "product " in content

                    result_info["contains_query"] = query.lower() in content.lower()

                results.append(result_info)

        with allure.step("Анализ результатов поиска на кириллице"):
            allure.attach(
                json.dumps(results, indent=2, ensure_ascii=False),
                name="Результаты поиска на кириллице",
                attachment_type=allure.attachment_type.JSON,
            )

            successful_searches = [r for r in results if r["success"]]
            successful_count = len(successful_searches)

            assert successful_count > 0, "Ни один запрос на кириллице не вернул успешный ответ"

            for result in successful_searches:
                assert result.get("has_html_structure", False), \
                    f"Успешный ответ для '{result['query']}' не содержит HTML структуру"

                assert result.get("contains_search_results", False) or \
                       "ничего не найдено" in response.text.lower(), \
                    f"Ответ для '{result['query']}' не содержит результатов поиска"

    @allure.title("API Тест 2: Поиск книг на латинице")
    @allure.description("Тест проверяет поиск книг с использованием латиницы в запросе")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_latin(self, api_client: APIClient) -> None:
        """
        Тест поиска книг на латинице.

        Args:
            api_client (APIClient): Фикстура API клиента
        """
        test_queries = [
            "harry potter",
            "the lord of the rings",
            "game of thrones",
            "to kill a mockingbird",
            "1984"
        ]

        search_results = []

        for query in test_queries:
            with allure.step(f"Поиск книги: '{query}'"):
                response = api_client.search_books(query)

                result = {
                    "query": query,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }

                if response.status_code == 200:
                    content = response.text
                    result["content_length"] = len(content)

                    result["is_html"] = "<!DOCTYPE html>" in content or "<html" in content
                    result["has_results"] = any(
                        marker in content.lower()
                        for marker in ["search-result", "product ", "товар", "книг"]
                    )

                    result["mentions_query"] = query.lower() in content.lower()

                search_results.append(result)

                if response.status_code == 200:
                    preview = content[:1000] + "..." if len(content) > 1000 else content
                    allure.attach(
                        preview,
                        name=f"Response_preview_{query}",
                        attachment_type=allure.attachment_type.HTML if result.get("is_html") else allure.attachment_type.TEXT,
                    )

        with allure.step("Анализ результатов поиска на латинице"):
            allure.attach(
                json.dumps(search_results, indent=2),
                name="Latin Search Analysis",
                attachment_type=allure.attachment_type.JSON,
            )

            successful_responses = [r for r in search_results if r["status_code"] == 200]
            assert len(successful_responses) > 0, "API не вернул ни одного успешного ответа для латинских запросов"

            for result in successful_responses:
                assert result["response_time"] < 30, \
                    f"Время ответа для '{result['query']}' слишком большое: {result['response_time']}сек"

                if result.get("is_html"):
                    assert result.get("has_results", False), \
                        f"HTML ответ для '{result['query']}' не содержит результатов"

    @allure.title("API Тест 3: Поиск книг с цифрами в названии")
    @allure.description("Тест проверяет поиск книг, содержащих цифры в названии")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_numbers(self, api_client: APIClient) -> None:
        """
        Тест поиска книг с цифрами в названии.

        Args:
            api_client (APIClient): Фикстура API клиента
        """
        test_queries = [
            "1984",
            "451 градус по фаренгейту",
            "20000 лье под водой",
            "книга 1",
            "12 стульев"
        ]

        results = []

        for query in test_queries:
            with allure.step(f"Поиск: '{query}'"):
                response = api_client.search_books(query)

                result_info = {
                    "query": query,
                    "status_code": response.status_code,
                    "has_numbers": any(char.isdigit() for char in query)
                }

                if response.status_code == 200:
                    content = response.text
                    result_info["response_size"] = len(content)

                    result_info["contains_numbers"] = any(char.isdigit() for char in content[:5000])

                    result_info["has_book_results"] = any(
                        marker in content.lower()
                        for marker in ["product-", "book-", "товар", "книг"]
                    )

                results.append(result_info)

        with allure.step("Анализ поиска с цифрами"):
            allure.attach(
                json.dumps(results, indent=2, ensure_ascii=False),
                name="Поиск с цифрами - результаты",
                attachment_type=allure.attachment_type.JSON,
            )

            successful_requests = [r for r in results if r["status_code"] == 200]
            assert len(successful_requests) > 0, "API не вернул успешных ответов для запросов с цифрами"

            for result in successful_requests:
                if result["has_numbers"] and result.get("contains_numbers") is not None:
                    assert result["contains_numbers"], \
                        f"Ответ для запроса с цифрами '{result['query']}' не содержит цифр"

    @allure.title("API Тест 4: Поиск с пустым полем запроса")
    @allure.description("Тест проверяет поведение API при отправке поискового запроса с пустым полем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_empty_query(self, api_client: APIClient) -> None:
        """
        Тест поиска с пустым запросом.

        Args:
            api_client (APIClient): Фикстура API клиента
        """
        test_cases = [
            {"query": "", "description": "Пустая строка"},
            {"query": "   ", "description": "Пробелы"},
            {"query": None, "description": "None (должен обрабатываться как пустой)"}
        ]

        results = []

        for test_case in test_cases:
            with allure.step(f"Тест: {test_case['description']}"):
                query = test_case["query"]

                if query is None:
                    response = api_client.get("/search/")
                else:
                    response = api_client.search_books(query)

                result = {
                    "test_case": test_case["description"],
                    "query": query,
                    "status_code": response.status_code,
                    "response_size": len(response.content) if response.content else 0
                }

                if response.status_code == 200:
                    content = response.text
                    result["is_redirect"] = "location" in response.headers or "redirect" in content.lower()
                    result["is_main_page"] = "лабиринт" in content.lower() and "книжный" in content.lower()
                    result["has_content"] = len(content.strip()) > 0

                results.append(result)

        with allure.step("Анализ поведения при пустых запросах"):
            allure.attach(
                json.dumps(results, indent=2, ensure_ascii=False),
                name="Пустые запросы - результаты",
                attachment_type=allure.attachment_type.JSON,
            )

            for result in results:
                assert result["status_code"] != 500, \
                    f"Серверная ошибка 500 при пустом запросе: {result['test_case']}"

            status_codes = [r["status_code"] for r in results]
            unique_statuses = set(status_codes)

            assert len(unique_statuses) <= 2, \
                f"API ведет себя непоследовательно для пустых запросов: {unique_statuses}"

    @allure.title("API Тест 5: Поиск книг без токена авторизации")
    @allure.description("Тест проверяет доступность поиска книг без токена авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_without_token(self, api_client: APIClient) -> None:
        """
        Тест поиска без токена авторизации.

        Args:
            api_client (APIClient): Фикстура API клиента
        """
        test_queries = ["книга", "book", "роман"]

        results_with_auth = []
        results_without_auth = []

        for query in test_queries:
            with allure.step(f"Поиск с авторизацией: '{query}'"):
                response = api_client.search_books(query, include_auth=True)

                results_with_auth.append({
                    "query": query,
                    "status_code": response.status_code,
                    "headers_count": len(response.headers)
                })

        for query in test_queries:
            with allure.step(f"Поиск без авторизации: '{query}'"):
                response = api_client.search_books(query, include_auth=False)

                result = {
                    "query": query,
                    "status_code": response.status_code,
                    "headers_count": len(response.headers),
                    "is_unauthorized": response.status_code in [401, 403]
                }

                results_without_auth.append(result)

                allure.attach(
                    json.dumps(dict(response.headers), indent=2),
                    name=f"Headers_Without_Auth_{query}",
                    attachment_type=allure.attachment_type.JSON,
                )

        with allure.step("Сравнение результатов с авторизацией и без"):
            comparison = []

            for i, (with_auth, without_auth) in enumerate(zip(results_with_auth, results_without_auth)):
                comparison.append({
                    "query": with_auth["query"],
                    "with_auth_status": with_auth["status_code"],
                    "without_auth_status": without_auth["status_code"],
                    "status_match": with_auth["status_code"] == without_auth["status_code"],
                    "requires_auth": without_auth["is_unauthorized"]
                })

            allure.attach(
                json.dumps(comparison, indent=2, ensure_ascii=False),
                name="Сравнение авторизации",
                attachment_type=allure.attachment_type.JSON,
            )

            all_require_auth = all(r["requires_auth"] for r in results_without_auth)
            none_require_auth = all(not r["requires_auth"] for r in results_without_auth)

            if all_require_auth:
                allure.dynamic.title("API Тест 5: Поиск требует авторизацию")
                allure.attach(
                    "API требует авторизацию для всех поисковых запросов",
                    name="Политика доступа",
                    attachment_type=allure.attachment_type.TEXT,
                )
                for result in results_without_auth:
                    assert result["status_code"] in [401, 403], \
                        f"Без авторизации ожидалась ошибка 401/403, но получен {result['status_code']}"

            elif none_require_auth:
                allure.dynamic.title("API Тест 5: Поиск доступен без авторизации")
                allure.attach(
                    "API предоставляет публичный доступ к поиску",
                    name="Политика доступа",
                    attachment_type=allure.attachment_type.TEXT,
                )
                for result in results_without_auth:
                    assert result["status_code"] == 200, \
                        f"Без авторизации ожидался статус 200, но получен {result['status_code']}"

            else:
                allure.dynamic.title("API Тест 5: Смешанная политика доступа")
                allure.attach(
                    "API имеет смешанную политику доступа для разных запросов",
                    name="Политика доступа",
                    attachment_type=allure.attachment_type.TEXT,
                )
                status_codes = [r["status_code"] for r in results_without_auth]
                assert len(set(status_codes)) <= 2, \
                    f"API ведет себя непоследовательно без авторизации: {set(status_codes)}"

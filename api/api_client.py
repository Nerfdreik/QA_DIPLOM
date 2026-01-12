import requests
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.config import settings
import allure
import json
import logging


class APIClient:
    """Клиент для работы с API Лабиринта."""

    def __init__(self) -> None:
        """
        Инициализация API клиента.
        """
        self.base_url = settings.BASE_URL
        self.api_base_url = settings.API_BASE_URL
        self.session = requests.Session()

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest"
        }

        retry_strategy = Retry(
            total=settings.API_MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.logger = logging.getLogger(__name__)

    @allure.step("Отправить {method} запрос на {url}")
    def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        include_auth: bool = True
    ) -> requests.Response:
        """
        Базовый метод для отправки HTTP запросов.

        Args:
            method (str): HTTP метод
            url (str): URL для запроса
            params (Optional[Dict[str, Any]]): Параметры запроса
            data (Optional[Dict[str, Any]]): Тело запроса
            headers (Optional[Dict[str, str]]): Дополнительные заголовки
            include_auth (bool): Включать ли авторизацию

        Returns:
            requests.Response: Ответ сервера
        """
        request_headers = {**self.headers, **(headers or {})}

        if not include_auth:
            if "Authorization" in request_headers:
                del request_headers["Authorization"]
            if "Cookie" in request_headers:
                del request_headers["Cookie"]

        self.logger.info(f"Sending {method} request to {url}")

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=data,
                headers=request_headers,
                timeout=settings.API_TIMEOUT
            )

            request_info = {
                "method": method,
                "url": url,
                "params": params,
                "headers": dict(response.request.headers),
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }

            try:
                request_info["response"] = response.json()
            except:
                request_info["response"] = response.text[:500] + "..." if len(response.text) > 500 else response.text

            allure.attach(
                json.dumps(request_info, indent=2, ensure_ascii=False),
                name=f"{method} {url}",
                attachment_type=allure.attachment_type.JSON,
            )

            return response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            allure.attach(
                str(e),
                name=f"Request Error: {method} {url}",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise

    @allure.step("GET запрос: {endpoint}")
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        include_auth: bool = True
    ) -> requests.Response:
        """
        Отправляет GET запрос.

        Args:
            endpoint (str): Конечная точка
            params (Optional[Dict[str, Any]]): Параметры запроса
            headers (Optional[Dict[str, str]]): Заголовки запроса
            include_auth (bool): Включать ли авторизацию

        Returns:
            requests.Response: Ответ сервера
        """
        url = f"{self.base_url}{endpoint}" if endpoint.startswith("/") else endpoint
        return self._request("GET", url, params=params, headers=headers, include_auth=include_auth)

    @allure.step("POST запрос: {endpoint}")
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        include_auth: bool = True
    ) -> requests.Response:
        """
        Отправляет POST запрос.

        Args:
            endpoint (str): Конечная точка
            data (Optional[Dict[str, Any]]): Тело запроса
            headers (Optional[Dict[str, str]]): Заголовки запроса
            include_auth (bool): Включать ли авторизацию

        Returns:
            requests.Response: Ответ сервера
        """
        url = f"{self.base_url}{endpoint}" if endpoint.startswith("/") else endpoint
        return self._request("POST", url, data=data, headers=headers, include_auth=include_auth)

    @allure.step("Поиск книг: {query}")
    def search_books(
        self,
        query: str,
        include_auth: bool = True
    ) -> requests.Response:
        """
        Выполняет поиск книг.

        Args:
            query (str): Поисковый запрос
            include_auth (bool): Включать ли авторизацию

        Returns:
            requests.Response: Ответ сервера
        """
        params = {"q": query} if query else {}
        return self.get("/search/", params=params, include_auth=include_auth)

    @allure.step("Автодополнение поиска: {query}")
    def autocomplete_search(
        self,
        query: str,
        include_auth: bool = True
    ) -> requests.Response:
        """
        Получает предложения для автодополнения поиска.

        Args:
            query (str): Поисковый запрос
            include_auth (bool): Включать ли авторизацию

        Returns:
            requests.Response: Ответ сервера
        """
        params = {"q": query}
        return self.get("/search/autocomplete-jquery.php", params=params, include_auth=include_auth)

    @allure.step("Быстрый поиск: {query}")
    def quick_search(
        self,
        query: str,
        include_auth: bool = True
    ) -> requests.Response:
        """
        Выполняет быстрый поиск.

        Args:
            query (str): Поисковый запрос
            include_auth (bool): Включать ли авторизацию

        Returns:
            requests.Response: Ответ сервера
        """
        params = {"q": query}
        return self.get("/search/quicksearch/", params=params, include_auth=include_auth)

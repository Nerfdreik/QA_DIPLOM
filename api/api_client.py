import requests
import logging
from typing import Optional, Dict, Any
from urllib.parse import urljoin
from config.settings import settings

logger = logging.getLogger(__name__)


class APIClient:
    """API клиент для сайта Лабиринт."""
    
    def __init__(self) -> None:
        """
        Инициализация API клиента.
        """
        self.base_url = settings.BASE_URL  
        self.session = requests.Session()
        self.session.headers.update(settings.DEFAULT_HEADERS)
        self.timeout = settings.API_TIMEOUT
 
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        include_auth: bool = True
    ) -> requests.Response:
        """
        Выполнение HTTP запроса.
        """
        url = urljoin(self.base_url, endpoint)

        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        if include_auth and settings.TEST_TOKEN:
            request_headers["Authorization"] = f"Bearer {settings.TEST_TOKEN}"

        logger.info(f"Sending {method} request to {url}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=request_headers,
                timeout=self.timeout
            )
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def search_books(
        self,
        query: str,
        include_auth: bool = True
    ) -> requests.Response:
        """
        Поиск книг.

        Args:
            query: Поисковый запрос
            include_auth: Включить авторизацию

        Returns:
            Response: Ответ с результатами поиска
        """
        params = {"q": query}
        return self._make_request(
            method="GET",
            endpoint="/search/",
            params=params,
            include_auth=include_auth
        )

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """
        GET запрос.
        """
        return self._make_request("GET", endpoint, **kwargs)

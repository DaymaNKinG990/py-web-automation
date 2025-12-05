"""
Data models for web automation testing framework.
"""

# Python imports
from http import HTTPStatus
from json import loads
from json.decoder import JSONDecodeError
from typing import Any

from msgspec import Struct, field


class HttpResult(Struct, frozen=True):
    """
    HTTP request result.

    Contains complete information about an HTTP request and response,
    including status, headers, body, and timing information.
    """

    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    redirect: bool
    client_error: bool
    server_error: bool
    informational: bool
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    content_type: str | None = None
    reason: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def json(self) -> dict[str, Any]:
        """
        Parse JSON from response body.

        Returns:
            Parsed JSON data as dictionary

        Raises:
            ValueError: If body is not valid JSON
        """
        try:
            return loads(self.body.decode("utf-8"))
        except (JSONDecodeError, ValueError, UnicodeDecodeError) as e:
            raise ValueError(f"Failed to parse JSON: {e}") from e

    @property
    def text(self) -> str:
        """
        Get response body as text.

        Returns:
            Response body decoded as UTF-8 string
        """
        return self.body.decode("utf-8", errors="replace")

    def raise_for_status(self) -> None:
        """
        Raise exception if status code indicates error.

        Raises:
            Exception: If status code is 4xx or 5xx (client or server error)
        """
        if not self._is_error_status():
            return

        error_msg = self.error_message or self.text
        raise Exception(f"HTTP {self.status_code}: {error_msg}")

    def _is_error_status(self) -> bool:
        """
        Check if status code indicates error.

        Returns:
            True if status code is 4xx or 5xx
        """
        try:
            status = HTTPStatus(self.status_code)
            return status.is_client_error or status.is_server_error
        except ValueError:
            # Invalid status code - treat as error if >= 400
            return self.status_code >= 400

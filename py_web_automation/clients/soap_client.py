"""
SOAP API client for web automation testing.

This module provides SoapClient for testing SOAP API endpoints,
including WSDL parsing, operation invocation, and response handling.
"""

from typing import Any
from xml.etree import ElementTree as ET

from httpx import AsyncClient, Limits

from ..config import Config
from .base_client import BaseClient
from .models import ApiResult


class SoapClient(BaseClient):
    """
    SOAP API client for web automation testing.

    Implements SOAP 1.1 and 1.2 protocol support for testing SOAP web services.
    Follows the Single Responsibility Principle by focusing solely on SOAP API testing.

    Provides methods for testing SOAP API endpoints:
    - WSDL parsing and service discovery
    - SOAP operation invocation
    - SOAP envelope construction
    - Response parsing and validation
    - SOAP fault handling

    Attributes:
        client: HTTP client instance for making requests
        _auth_token: Current authentication token (private)
        _auth_token_type: Type of authentication token (default: "Bearer")
        wsdl_url: WSDL document URL (optional)
        soap_version: SOAP version ("1.1" or "1.2", default: "1.1")

    Example:
        >>> from py_web_automation import Config, SoapClient
        >>> config = Config(timeout=30)
        >>> async with SoapClient("https://api.example.com/soap", config) as soap:
        ...     result = await soap.call(
        ...         operation="GetUser",
        ...         body={"userId": "123"}
        ...     )
        ...     assert result.success
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        wsdl_url: str | None = None,
        soap_version: str = "1.1",
    ) -> None:
        """
        Initialize SOAP client.

        Args:
            url: SOAP service endpoint URL
            config: Configuration object with timeout and retry settings
            wsdl_url: WSDL document URL (optional, for service discovery)
            soap_version: SOAP version ("1.1" or "1.2", default: "1.1")

        Raises:
            ValueError: If config is None or soap_version is invalid

        Example:
            >>> config = Config(timeout=30)
            >>> soap = SoapClient(
            ...     "https://api.example.com/soap",
            ...     config,
            ...     wsdl_url="https://api.example.com/wsdl"
            ... )
        """
        super().__init__(url, config)
        if soap_version not in ("1.1", "1.2"):
            raise ValueError(f"Invalid SOAP version: {soap_version}. Must be '1.1' or '1.2'")

        self.client: AsyncClient = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )
        self.wsdl_url: str | None = wsdl_url
        self.soap_version: str = soap_version
        self._auth_token: str | None = None
        self._auth_token_type: str = "Bearer"

    async def close(self) -> None:
        """
        Close HTTP client and cleanup resources.

        Closes the underlying HTTP client connection pool and clears
        authentication tokens. This method is automatically called
        when exiting an async context manager.
        """
        await self.client.aclose()
        self._auth_token = None
        self._auth_token_type = "Bearer"

    def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
        """
        Set authentication token for all subsequent requests.

        Args:
            token: Authentication token
            token_type: Token type (default: "Bearer")
        """
        self._auth_token = token
        self._auth_token_type = token_type
        self.logger.debug(f"Authentication token set (type: {token_type})")

    def clear_auth_token(self) -> None:
        """Clear authentication token."""
        self._auth_token = None
        self._auth_token_type = "Bearer"
        self.logger.debug("Authentication token cleared")

    def _build_soap_envelope(self, operation: str, body: dict[str, Any], namespace: str | None = None) -> str:
        """
        Build SOAP envelope XML.

        Args:
            operation: SOAP operation name
            body: Operation body data
            namespace: SOAP namespace (optional)

        Returns:
            SOAP envelope as XML string
        """
        if self.soap_version == "1.1":
            soap_ns = "http://schemas.xmlsoap.org/soap/envelope/"
        else:  # SOAP 1.2
            soap_ns = "http://www.w3.org/2003/05/soap-envelope"

        # Create SOAP envelope
        envelope = ET.Element(f"{{{soap_ns}}}Envelope")
        envelope.set("xmlns:soap", soap_ns)
        if namespace:
            envelope.set("xmlns", namespace)

        # Create header (empty for now, can be extended)
        ET.SubElement(envelope, f"{{{soap_ns}}}Header")

        # Create body
        soap_body = ET.SubElement(envelope, f"{{{soap_ns}}}Body")
        operation_elem = ET.SubElement(soap_body, operation)

        # Add body data
        self._dict_to_xml(operation_elem, body)

        return ET.tostring(envelope, encoding="unicode", xml_declaration=True)

    def _dict_to_xml(self, parent: ET.Element, data: dict[str, Any]) -> None:
        """
        Convert dictionary to XML elements recursively.

        Args:
            parent: Parent XML element
            data: Dictionary data to convert
        """
        for key, value in data.items():
            if isinstance(value, dict):
                elem = ET.SubElement(parent, key)
                self._dict_to_xml(elem, value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        elem = ET.SubElement(parent, key)
                        self._dict_to_xml(elem, item)
                    else:
                        elem = ET.SubElement(parent, key)
                        elem.text = str(item)
            else:
                elem = ET.SubElement(parent, key)
                elem.text = str(value)

    async def call(
        self,
        operation: str,
        body: dict[str, Any],
        namespace: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> ApiResult:
        """
        Execute SOAP operation call.

        Args:
            operation: SOAP operation name
            body: Operation body data as dictionary
            namespace: SOAP namespace (optional)
            headers: Custom request headers (optional)

        Returns:
            ApiResult with SOAP response

        Example:
            >>> result = await soap.call(
            ...     operation="GetUser",
            ...     body={"userId": "123"},
            ...     namespace="http://example.com/service"
            ... )
            >>> if result.success:
            ...     # Parse SOAP response
            ...     xml_response = result.text()
        """
        # Build SOAP envelope
        soap_envelope = self._build_soap_envelope(operation, body, namespace)

        # Prepare headers
        request_headers: dict[str, str] = {
            "Content-Type": 'text/xml; charset="utf-8"',
            "SOAPAction": f'"{operation}"' if self.soap_version == "1.1" else "",
        }
        if headers:
            request_headers.update(headers)

        # Add authentication token if set
        if self._auth_token and "Authorization" not in request_headers:
            auth_header = f"{self._auth_token_type} {self._auth_token}"
            request_headers["Authorization"] = auth_header

        self.logger.info(f"Executing SOAP operation: {operation}")

        try:
            response = await self.client.post(
                url=self.url,
                content=soap_envelope.encode("utf-8"),
                headers=request_headers,
            )

            response_body = response.content
            response_headers = dict(response.headers)

            # Redact sensitive headers
            sensitive_headers = {
                "authorization",
                "cookie",
                "set-cookie",
                "x-api-key",
                "x-auth-token",
            }
            redacted_headers = {
                k.lower(): ("[REDACTED]" if k.lower() in sensitive_headers else v) for k, v in response_headers.items()
            }

            content_type = response_headers.get("Content-Type") or response_headers.get("content-type")

            try:
                response_time = response.elapsed.total_seconds()
            except (AttributeError, RuntimeError):
                response_time = 0.0

            self.logger.info(f"SOAP response: status_code={response.status_code}, elapsed={response_time:.3f}s")

            return ApiResult(
                endpoint=self.url,
                method="POST",
                informational=response.is_informational,
                success=response.is_success,
                redirect=response.is_redirect,
                client_error=response.is_client_error,
                server_error=response.is_server_error,
                status_code=response.status_code,
                response_time=response_time,
                headers=redacted_headers,
                body=response_body,
                content_type=content_type,
                reason=getattr(response, "reason_phrase", None),
                error_message=None,
            )
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"SOAP request failed: {error_msg}")
            return ApiResult(
                endpoint=self.url,
                method="POST",
                status_code=0,
                response_time=0,
                success=False,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                headers={},
                body=b"",
                content_type=None,
                reason=None,
                error_message=error_msg,
            )

    def parse_soap_fault(self, result: ApiResult) -> dict[str, Any] | None:
        """
        Parse SOAP fault from response.

        Args:
            result: ApiResult from SOAP call

        Returns:
            Dictionary with fault information or None if no fault

        Example:
            >>> result = await soap.call("InvalidOperation", {})
            >>> fault = soap.parse_soap_fault(result)
            >>> if fault:
            ...     print(f"SOAP Fault: {fault['faultstring']}")
        """
        try:
            root = ET.fromstring(result.body)
            # Find fault element (namespace-aware)
            namespaces = {
                "soap": "http://schemas.xmlsoap.org/soap/envelope/",
                "soap12": "http://www.w3.org/2003/05/soap-envelope",
            }

            fault = root.find(".//soap:Fault", namespaces)
            if fault is None:
                fault = root.find(".//soap12:Fault", namespaces)
            if fault is not None:
                fault_info: dict[str, Any] = {}
                for child in fault:
                    fault_info[child.tag.split("}")[-1]] = child.text
                return fault_info
        except (ET.ParseError, ValueError, AttributeError):
            pass

        return None

"""
SOAP API client for web automation testing.

This module provides SoapClient for testing SOAP API endpoints,
including WSDL parsing, operation invocation, and response handling.
"""

# Python imports
from __future__ import annotations

from asyncio import sleep
from time import time
from types import TracebackType
from typing import TYPE_CHECKING, Any

from httpx import AsyncClient, Limits
from zeep import AsyncClient as ZeepAsyncClient
from zeep.exceptions import Fault
from zeep.transports import AsyncTransport

# Local imports
from ....config import Config
from ....exceptions import OperationError
from .middleware.context import _SoapRequestContext, _SoapResponseContext
from .soap_result import SoapResult

if TYPE_CHECKING:
    from .middleware.context import _SoapRequestContext, _SoapResponseContext
    from .middleware.middleware import MiddlewareChain


class SoapClient:
    """
    SOAP API client for web automation testing.

    Implements SOAP 1.1 and 1.2 protocol support for testing SOAP web services.
    Follows the Single Responsibility Principle by focusing solely on SOAP API testing.

    Provides methods for testing SOAP API endpoints:
    - WSDL parsing and service discovery
    - SOAP operation invocation with middleware support
    - SOAP envelope construction
    - Response parsing and validation
    - SOAP fault handling

    Attributes:
        url: SOAP service endpoint URL
        config: Configuration object
        client: Zeep async client instance
        wsdl_url: WSDL document URL (optional)
        soap_version: SOAP version ("1.1" or "1.2", default: "1.1")
        _httpx_client: HTTP client for transport (private)
        _middleware: Middleware chain for operation processing (private)

    Example:
        >>> from py_web_automation.clients.soap_client import SoapClient, MiddlewareChain
        >>> from py_web_automation.clients.soap_client.middleware import LoggingMiddleware
        >>> config = Config(timeout=30)
        >>> middleware = MiddlewareChain().add(LoggingMiddleware())
        >>> async with SoapClient(
        ...     "https://api.example.com/soap", config, middleware=middleware
        ... ) as soap:
        ...     result = await soap.call("GetUser", {"userId": "123"})
        ...     if result.success:
        ...         print(result.response)
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        wsdl_url: str | None = None,
        soap_version: str = "1.1",
        middleware: MiddlewareChain | None = None,
    ) -> None:
        """
        Initialize SOAP client.

        Args:
            url: SOAP service endpoint URL
            config: Configuration object with timeout and retry settings
            wsdl_url: WSDL document URL (optional, for service discovery)
            soap_version: SOAP version ("1.1" or "1.2", default: "1.1")
            middleware: Optional middleware chain for operation processing

        Raises:
            ImportError: If zeep is not installed
            ValueError: If soap_version is invalid
            TypeError: If config is not a Config object when provided

        Example:
            >>> config = Config(timeout=30)
            >>> middleware = MiddlewareChain().add(LoggingMiddleware())
            >>> soap = SoapClient(
            ...     "https://api.example.com/soap",
            ...     config,
            ...     wsdl_url="https://api.example.com/wsdl",
            ...     middleware=middleware
            ... )
        """
        if config is None:
            config = Config()
        elif not isinstance(config, Config):
            raise TypeError("config must be a Config object")
        if soap_version not in ("1.1", "1.2"):
            raise ValueError(f"Invalid SOAP version: {soap_version}. Must be '1.1' or '1.2'")
        self.url: str = url
        self.config: Config = config
        # Create httpx client for transport
        httpx_client = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )
        # Create zeep async transport
        transport = AsyncTransport(client=httpx_client)
        # Use wsdl_url if provided, otherwise use url
        wsdl = wsdl_url or url
        # Create zeep async client
        self.client: ZeepAsyncClient = ZeepAsyncClient(wsdl=wsdl, transport=transport)
        self.wsdl_url: str | None = wsdl_url
        self.soap_version: str = soap_version
        self._httpx_client: AsyncClient = httpx_client
        self._middleware = middleware

    async def __aenter__(self) -> SoapClient:
        """
        Async context manager entry.

        Returns:
            Self for use in async with statement
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Async context manager exit.

        Ensures proper cleanup by calling close() method.
        """
        await self.close()

    async def close(self) -> None:
        """
        Close HTTP client and cleanup resources.

        Closes the underlying HTTP client connection pool.
        This method is automatically called when exiting an async context manager.
        """
        await self._httpx_client.aclose()

    async def _prepare_request_context(
        self,
        operation: str,
        body: dict[str, Any] | None,
        headers: dict[str, str] | None,
        namespace: str | None,
    ) -> _SoapRequestContext:
        """
        Prepare request context with middleware.

        Args:
            operation: SOAP operation name
            body: Operation body data
            headers: Custom request headers
            namespace: SOAP namespace

        Returns:
            _SoapRequestContext with middleware applied
        """
        request_context = _SoapRequestContext(
            operation=operation,
            body=body or {},
            headers=headers.copy() if headers else {},
            namespace=namespace,
        )
        # Process through middleware
        if self._middleware:
            await self._middleware.process_request(request_context)
        return request_context

    async def _process_response(
        self, result: SoapResult, request_context: _SoapRequestContext
    ) -> SoapResult:
        """
        Process response through middleware.

        Args:
            result: SoapResult from operation
            request_context: Original request context

        Returns:
            Processed SoapResult (may be modified by middleware)
        """
        if self._middleware:
            response_context = _SoapResponseContext(result)
            # Copy metadata_context from request to result
            response_context.metadata_context = request_context.metadata_context.copy()
            result = result.__class__(
                operation=result.operation,
                response_time=result.response_time,
                success=result.success,
                response=result.response,
                soap_fault=result.soap_fault,
                headers=result.headers,
                metadata=response_context.metadata_context,
            )
            await self._middleware.process_response(response_context)
            # Create new result from potentially modified context
            result = response_context.result
        return result

    def _extract_soap_fault(self, error: Exception) -> dict[str, Any] | None:
        """Extract SOAP fault information from exception."""
        if not isinstance(error, Fault):
            return None
        return {
            "faultcode": str(error.code) if hasattr(error, "code") else "Unknown",
            "faultstring": str(error.message) if hasattr(error, "message") else str(error),
            "detail": str(error.detail) if hasattr(error, "detail") else None,
        }

    async def _handle_operation_error(
        self,
        error: Exception,
        operation: str,
        request_context: _SoapRequestContext,
        start_time: float,
    ) -> SoapResult:
        """
        Handle error during SOAP operation execution.

        Args:
            error: Exception that occurred
            operation: Operation name
            request_context: Request context
            start_time: Operation start time

        Returns:
            SoapResult representing the error
        """
        response_time = time() - start_time
        soap_fault = self._extract_soap_fault(error)

        # Process error through middleware
        if self._middleware:
            error_result = await self._middleware.process_error(request_context, error)
            if error_result is not None:
                return error_result

        # Create error result
        return SoapResult(
            operation=operation,
            response_time=response_time,
            success=False,
            response=None,
            soap_fault=soap_fault,
            headers={},
            metadata=request_context.metadata_context.copy(),
        )

    def _get_operation_proxy(self, operation: str) -> Any:
        """Get SOAP operation proxy by name."""
        service = self.client.service
        operation_proxy = getattr(service, operation, None)
        if operation_proxy is not None:
            return operation_proxy
        # Try using item access for operations with invalid Python names
        try:
            return service[operation]
        except (KeyError, AttributeError):
            raise OperationError(f"Operation '{operation}' not found in WSDL") from None

    def _extract_response_headers(self) -> dict[str, str]:
        """Extract response headers from httpx client if available."""
        if hasattr(self._httpx_client, "headers"):
            return dict(self._httpx_client.headers)
        return {}

    def _create_success_result(
        self,
        operation: str,
        response: Any,
        request_context: _SoapRequestContext,
        response_time: float,
        response_headers: dict[str, str],
    ) -> SoapResult:
        """Create successful SoapResult."""
        return SoapResult(
            operation=operation,
            response_time=response_time,
            success=True,
            response=response,
            soap_fault=None,
            headers=response_headers,
            metadata=request_context.metadata_context.copy(),
        )

    async def _handle_retry(self, request_context: _SoapRequestContext) -> bool:
        """Check if retry is needed and wait if necessary."""
        if not request_context.metadata_context.get("should_retry"):
            return False
        delay = request_context.metadata_context.get("retry_delay", 0)
        if delay > 0:
            await sleep(delay)
        return True

    async def call(
        self,
        operation: str,
        body: dict[str, Any] | None = None,
        namespace: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> SoapResult:
        """
        Execute SOAP operation call using zeep with middleware support.

        Args:
            operation: SOAP operation name
            body: Operation body data as dictionary (optional)
            namespace: SOAP namespace (optional, ignored when using WSDL)
            headers: Custom request headers (optional)

        Returns:
            SoapResult with response, SOAP fault, and metadata

        Raises:
            OperationError: If operation not found or call fails after retries

        Example:
            >>> result = await soap.call("GetUser", {"userId": "123"})
            >>> if result.success:
            ...     print(result.response)
            >>> else:
            ...     result.raise_for_fault()
        """
        # Retry loop for operations
        while True:
            start_time = time()
            request_context = await self._prepare_request_context(
                operation=operation,
                body=body,
                headers=headers,
                namespace=namespace,
            )
            request_context.metadata_context["start_time"] = start_time
            try:
                # Update transport headers from context (middleware may have modified them)
                if request_context.headers:
                    self._httpx_client.headers.update(request_context.headers)

                operation_proxy = self._get_operation_proxy(operation)
                response = await operation_proxy(**request_context.body)
                response_time = time() - start_time
                response_headers = self._extract_response_headers()
                result = self._create_success_result(
                    operation, response, request_context, response_time, response_headers
                )
                result = await self._process_response(result, request_context)
                return result
            except Exception as e:
                error_result = await self._handle_operation_error(
                    e, operation, request_context, start_time
                )
                # Check if retry is needed (set by RetryMiddleware)
                if await self._handle_retry(request_context):
                    continue  # Retry the operation
                return error_result

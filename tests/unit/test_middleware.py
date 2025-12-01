"""
Unit tests for middleware module.
"""

from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

from py_web_automation.clients.models import ApiResult
from py_web_automation.metrics import Metrics
from py_web_automation.middleware import (
    AuthMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
    Middleware,
    MiddlewareChain,
    RequestContext,
    ResponseContext,
    ValidationMiddleware,
)

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestMiddlewareChain:
    """Test MiddlewareChain class."""

    @pytest.mark.asyncio
    @allure.title("TC-MW-001: MiddlewareChain - add middleware")
    async def test_middleware_chain_add(self):
        """Test adding middleware to chain."""
        with allure.step("Create MiddlewareChain and middleware"):
            chain = MiddlewareChain()
            middleware = MagicMock(spec=Middleware)
            middleware.process_request = AsyncMock()
            middleware.process_response = AsyncMock()
            middleware.process_error = AsyncMock(return_value=None)

        with allure.step("Add middleware to chain"):
            result = chain.add(middleware)

        with allure.step("Verify middleware added and method chaining"):
            assert middleware in chain._middleware
            assert result is chain  # Method chaining

    @pytest.mark.asyncio
    @allure.title("TC-MW-002: MiddlewareChain - remove middleware")
    async def test_middleware_chain_remove(self):
        """Test removing middleware from chain."""
        with allure.step("Create MiddlewareChain with middleware"):
            chain = MiddlewareChain()
            middleware = MagicMock(spec=Middleware)
            middleware.process_request = AsyncMock()
            middleware.process_response = AsyncMock()
            middleware.process_error = AsyncMock(return_value=None)
            chain.add(middleware)

        with allure.step("Remove middleware"):
            result = chain.remove(middleware)

        with allure.step("Verify middleware removed"):
            assert middleware not in chain._middleware
            assert result is chain  # Method chaining

    @pytest.mark.asyncio
    @allure.title("TC-MW-003: MiddlewareChain - process_request")
    async def test_middleware_chain_process_request(self):
        """Test processing request through all middleware."""
        with allure.step("Create MiddlewareChain with multiple middleware"):
            chain = MiddlewareChain()
            middleware1 = MagicMock(spec=Middleware)
            middleware1.process_request = AsyncMock()
            middleware2 = MagicMock(spec=Middleware)
            middleware2.process_request = AsyncMock()
            chain.add(middleware1).add(middleware2)

            context = RequestContext(method="GET", url="/test")

        with allure.step("Process request"):
            await chain.process_request(context)

        with allure.step("Verify all middleware called in order"):
            middleware1.process_request.assert_called_once_with(context)
            middleware2.process_request.assert_called_once_with(context)
            assert middleware1.process_request.call_count == 1
            assert middleware2.process_request.call_count == 1

    @pytest.mark.asyncio
    @allure.title("TC-MW-004: MiddlewareChain - process_response (обратный порядок)")
    async def test_middleware_chain_process_response_reverse_order(self):
        """Test response processed in reverse order."""
        with allure.step("Create MiddlewareChain with multiple middleware"):
            chain = MiddlewareChain()
            call_order = []

            class TrackingMiddleware(Middleware):
                def __init__(self, name):
                    self.name = name

                async def process_request(self, context):
                    pass

                async def process_response(self, context):
                    call_order.append(self.name)

                async def process_error(self, context, error):
                    return None

            m1 = TrackingMiddleware("m1")
            m2 = TrackingMiddleware("m2")
            chain.add(m1).add(m2)

            result = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=200,
                response_time=0.5,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
            context = ResponseContext(result)

        with allure.step("Process response"):
            await chain.process_response(context)

        with allure.step("Verify middleware called in reverse order"):
            assert call_order == ["m2", "m1"]  # Last added, first called

    @pytest.mark.asyncio
    @allure.title("TC-MW-005: MiddlewareChain - process_error")
    async def test_middleware_chain_process_error(self):
        """Test error processing through chain."""
        with allure.step("Create MiddlewareChain with middleware that returns ApiResult"):
            chain = MiddlewareChain()

            class ErrorHandlingMiddleware(Middleware):
                async def process_request(self, context):
                    pass

                async def process_response(self, context):
                    pass

                async def process_error(self, context, error):
                    return ApiResult(
                        endpoint="/test",
                        method="GET",
                        status_code=500,
                        response_time=0.0,
                        success=False,
                        redirect=False,
                        client_error=False,
                        server_error=True,
                        informational=False,
                        error_message=str(error),
                    )

            middleware = ErrorHandlingMiddleware()
            chain.add(middleware)

            context = RequestContext(method="GET", url="/test")
            error = ValueError("test error")

        with allure.step("Process error"):
            result = await chain.process_error(context, error)

        with allure.step("Verify ApiResult returned"):
            assert result is not None
            assert result.status_code == 500
            assert result.error_message == "test error"

    @pytest.mark.asyncio
    @allure.title("TC-MW-006: MiddlewareChain - process_error возвращает None")
    async def test_middleware_chain_process_error_returns_none(self):
        """Test error propagates when middleware returns None."""
        with allure.step("Create MiddlewareChain with middleware that returns None"):
            chain = MiddlewareChain()

            class PassThroughMiddleware(Middleware):
                async def process_request(self, context):
                    pass

                async def process_response(self, context):
                    pass

                async def process_error(self, context, error):
                    return None

            middleware = PassThroughMiddleware()
            chain.add(middleware)

            context = RequestContext(method="GET", url="/test")
            error = ValueError("test error")

        with allure.step("Process error"):
            result = await chain.process_error(context, error)

        with allure.step("Verify None returned"):
            assert result is None


@pytest.mark.unit
class TestLoggingMiddleware:
    """Test LoggingMiddleware class."""

    @pytest.mark.asyncio
    @allure.title("TC-MW-007: LoggingMiddleware - process_request")
    async def test_logging_middleware_process_request(self, caplog):
        """Test request logging."""
        with allure.step("Create LoggingMiddleware"):
            middleware = LoggingMiddleware()

        with allure.step("Create RequestContext"):
            context = RequestContext(
                method="GET",
                url="/test",
                headers={"X-Custom": "value"},
                params={"page": 1},
            )

        with allure.step("Process request"):
            await middleware.process_request(context)

        with allure.step("Verify request logged"):
            assert "Request: GET /test" in caplog.text
            assert "headers=1" in caplog.text or "params=1" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-MW-008: LoggingMiddleware - process_response")
    async def test_logging_middleware_process_response(self, caplog):
        """Test response logging."""
        with allure.step("Create LoggingMiddleware"):
            middleware = LoggingMiddleware()

        with allure.step("Create ResponseContext"):
            result = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=200,
                response_time=0.5,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
            context = ResponseContext(result)

        with allure.step("Process response"):
            await middleware.process_response(context)

        with allure.step("Verify response logged"):
            assert "Response: 200" in caplog.text
            assert "time=0.5" in caplog.text
            assert "success=True" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-MW-009: LoggingMiddleware - process_error")
    async def test_logging_middleware_process_error(self, caplog):
        """Test error logging."""
        with allure.step("Create LoggingMiddleware"):
            middleware = LoggingMiddleware()

        with allure.step("Create RequestContext and error"):
            context = RequestContext(method="GET", url="/test")
            error = ValueError("test error")

        with allure.step("Process error"):
            result = await middleware.process_error(context, error)

        with allure.step("Verify error logged"):
            assert "Request error: GET /test" in caplog.text
            assert "test error" in caplog.text
            assert result is None


@pytest.mark.unit
class TestMetricsMiddleware:
    """Test MetricsMiddleware class."""

    @pytest.mark.asyncio
    @allure.title("TC-MW-010: MetricsMiddleware - process_request")
    async def test_metrics_middleware_process_request(self):
        """Test start_time recorded in metadata."""
        with allure.step("Create MetricsMiddleware with Metrics"):
            metrics = Metrics()
            middleware = MetricsMiddleware(metrics)

        with allure.step("Create RequestContext"):
            context = RequestContext(method="GET", url="/test")

        with allure.step("Process request"):
            await middleware.process_request(context)

        with allure.step("Verify start_time in metadata"):
            assert "start_time" in context.metadata
            assert isinstance(context.metadata["start_time"], float)

    @pytest.mark.asyncio
    @allure.title("TC-MW-011: MetricsMiddleware - process_response успех")
    async def test_metrics_middleware_process_response_success(self):
        """Test metrics recorded for successful response."""
        with allure.step("Create MetricsMiddleware with Metrics"):
            metrics = Metrics()
            middleware = MetricsMiddleware(metrics)

        with allure.step("Create ResponseContext with success"):
            result = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=200,
                response_time=0.5,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                metadata={"start_time": 1.0},  # Must be truthy (not 0.0)
            )
            context = ResponseContext(result)

        with allure.step("Process response"):
            await middleware.process_response(context)

        with allure.step("Verify metrics recorded"):
            assert metrics.request_count == 1
            assert metrics.success_count == 1
            assert metrics.error_count == 0
            assert metrics.avg_latency == pytest.approx(0.5, rel=0.1)

    @pytest.mark.asyncio
    @allure.title("TC-MW-012: MetricsMiddleware - process_response ошибка")
    async def test_metrics_middleware_process_response_error(self):
        """Test metrics recorded for error response."""
        with allure.step("Create MetricsMiddleware with Metrics"):
            metrics = Metrics()
            middleware = MetricsMiddleware(metrics)

        with allure.step("Create ResponseContext with error"):
            result = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=404,
                response_time=0.1,
                success=False,
                redirect=False,
                client_error=True,
                server_error=False,
                informational=False,
                metadata={"start_time": 1.0},  # Must be truthy (not 0.0)
            )
            context = ResponseContext(result)

        with allure.step("Process response"):
            await middleware.process_response(context)

        with allure.step("Verify error metrics recorded"):
            assert metrics.request_count == 1
            assert metrics.success_count == 0
            assert metrics.error_count == 1
            assert "client_error" in metrics.errors_by_type

    @pytest.mark.asyncio
    @allure.title("TC-MW-013: MetricsMiddleware - process_error")
    async def test_metrics_middleware_process_error(self):
        """Test error metrics recorded."""
        with allure.step("Create MetricsMiddleware with Metrics"):
            metrics = Metrics()
            middleware = MetricsMiddleware(metrics)

        with allure.step("Create RequestContext and error"):
            context = RequestContext(method="GET", url="/test")
            error = ConnectionError("connection failed")

        with allure.step("Process error"):
            await middleware.process_error(context, error)

        with allure.step("Verify error metrics recorded"):
            assert metrics.request_count == 1
            assert metrics.success_count == 0
            assert metrics.error_count == 1
            assert "ConnectionError" in metrics.errors_by_type


@pytest.mark.unit
class TestAuthMiddleware:
    """Test AuthMiddleware class."""

    @pytest.mark.asyncio
    @allure.title("TC-MW-014: AuthMiddleware - process_request добавляет Authorization header")
    async def test_auth_middleware_adds_header(self):
        """Test Authorization header added to request."""
        with allure.step("Create AuthMiddleware"):
            middleware = AuthMiddleware(token="abc123", token_type="Bearer")

        with allure.step("Create RequestContext without Authorization"):
            context = RequestContext(method="GET", url="/test")

        with allure.step("Process request"):
            await middleware.process_request(context)

        with allure.step("Verify Authorization header added"):
            assert context.headers["Authorization"] == "Bearer abc123"

    @pytest.mark.asyncio
    @allure.title("TC-MW-015: AuthMiddleware - не перезаписывает существующий header")
    async def test_auth_middleware_preserves_existing_header(self):
        """Test existing Authorization header not overwritten."""
        with allure.step("Create AuthMiddleware"):
            middleware = AuthMiddleware(token="abc123")

        with allure.step("Create RequestContext with existing Authorization"):
            context = RequestContext(method="GET", url="/test", headers={"Authorization": "Bearer existing"})

        with allure.step("Process request"):
            await middleware.process_request(context)

        with allure.step("Verify existing header preserved"):
            assert context.headers["Authorization"] == "Bearer existing"

    @pytest.mark.asyncio
    @allure.title("TC-MW-016: AuthMiddleware - custom token_type")
    async def test_auth_middleware_custom_token_type(self):
        """Test custom token type used."""
        with allure.step("Create AuthMiddleware with custom token_type"):
            middleware = AuthMiddleware(token="abc123", token_type="ApiKey")

        with allure.step("Create RequestContext"):
            context = RequestContext(method="GET", url="/test")

        with allure.step("Process request"):
            await middleware.process_request(context)

        with allure.step("Verify custom token type used"):
            assert context.headers["Authorization"] == "ApiKey abc123"


@pytest.mark.unit
class TestValidationMiddleware:
    """Test ValidationMiddleware class."""

    @pytest.mark.asyncio
    @allure.title("TC-MW-017: ValidationMiddleware - process_response валидный ответ")
    async def test_validation_middleware_valid_response(self):
        """Test validation of valid response."""
        with allure.step("Create ValidationMiddleware with schema"):
            from msgspec import Struct

            class User(Struct):
                id: int
                name: str

            middleware = ValidationMiddleware(User)

        with allure.step("Create ResponseContext with valid ApiResult"):
            result = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=200,
                response_time=0.5,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                body=b'{"id": 1, "name": "John"}',
            )
            context = ResponseContext(result)

        with allure.step("Process response"):
            await middleware.process_response(context)

        with allure.step("Verify no validation error"):
            assert "validation_error" not in context.metadata

    @pytest.mark.asyncio
    @allure.title("TC-MW-018: ValidationMiddleware - process_response невалидный ответ")
    async def test_validation_middleware_invalid_response(self):
        """Test validation error recorded."""
        with allure.step("Create ValidationMiddleware with schema"):
            from msgspec import Struct

            class User(Struct):
                id: int
                name: str

            middleware = ValidationMiddleware(User)

        with allure.step("Create ResponseContext with invalid ApiResult"):
            result = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=200,
                response_time=0.5,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                body=b'{"id": "invalid", "name": "John"}',  # id should be int
            )
            context = ResponseContext(result)

        with allure.step("Process response"):
            await middleware.process_response(context)

        with allure.step("Verify validation error in metadata"):
            assert "validation_error" in context.metadata

    @pytest.mark.asyncio
    @allure.title("TC-MW-019: ValidationMiddleware - только для успешных ответов")
    async def test_validation_middleware_only_success(self):
        """Test validation only for successful responses."""
        with allure.step("Create ValidationMiddleware"):
            from msgspec import Struct

            class User(Struct):
                id: int
                name: str

            middleware = ValidationMiddleware(User)

        with allure.step("Create ResponseContext with success=False"):
            result = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=404,
                response_time=0.5,
                success=False,
                redirect=False,
                client_error=True,
                server_error=False,
                informational=False,
            )
            context = ResponseContext(result)

        with allure.step("Process response"):
            await middleware.process_response(context)

        with allure.step("Verify validation not performed"):
            assert "validation_error" not in context.metadata


@pytest.mark.unit
class TestRequestContext:
    """Test RequestContext class."""

    @allure.title("TC-MW-020: RequestContext - инициализация")
    def test_request_context_init(self):
        """Test RequestContext initialization."""
        with allure.step("Create RequestContext"):
            context = RequestContext(
                method="GET",
                url="/test",
                headers={"X-Custom": "value"},
                params={"page": 1},
            )

        with allure.step("Verify all fields initialized"):
            assert context.method == "GET"
            assert context.url == "/test"
            assert context.headers == {"X-Custom": "value"}
            assert context.params == {"page": 1}
            assert context.metadata == {}

    @allure.title("TC-MW-021: RequestContext - модификация headers")
    def test_request_context_modify_headers(self):
        """Test headers can be modified."""
        with allure.step("Create RequestContext"):
            context = RequestContext(method="GET", url="/test")

        with allure.step("Modify headers"):
            context.headers["X-Custom"] = "value"

        with allure.step("Verify header modified"):
            assert context.headers["X-Custom"] == "value"


@pytest.mark.unit
class TestResponseContext:
    """Test ResponseContext class."""

    @allure.title("TC-MW-022: ResponseContext - инициализация")
    def test_response_context_init(self):
        """Test ResponseContext initialization."""
        with allure.step("Create ApiResult"):
            result = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=200,
                response_time=0.5,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )

        with allure.step("Create ResponseContext"):
            context = ResponseContext(result)

        with allure.step("Verify fields initialized"):
            assert context.result == result
            assert context.metadata == {}

    @allure.title("TC-MW-023: ResponseContext - модификация result")
    def test_response_context_modify_result(self):
        """Test result can be modified."""
        with allure.step("Create ResponseContext"):
            result1 = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=200,
                response_time=0.5,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
            context = ResponseContext(result1)

        with allure.step("Modify result"):
            result2 = ApiResult(
                endpoint="/test",
                method="GET",
                status_code=201,
                response_time=0.5,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
            context.result = result2

        with allure.step("Verify result modified"):
            assert context.result.status_code == 201

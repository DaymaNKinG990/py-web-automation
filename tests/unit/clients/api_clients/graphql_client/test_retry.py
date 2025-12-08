"""
Unit tests for RetryHandler and RetryConfig.
"""

# Python imports
from allure import title, description, step
from pytest import mark

# Local imports
from py_web_automation.clients.api_clients.graphql_client.retry import (
    RetryHandler,
    RetryConfig,
)
from py_web_automation.exceptions import ConnectionError, TimeoutError

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestRetryConfig:
    """Test RetryConfig class."""

    @mark.asyncio
    @title("RetryConfig initialization")
    @description("Test RetryConfig initializes with default values.")
    async def test_retry_config_init(self) -> None:
        """Test RetryConfig initializes with default values."""
        with step("Create RetryConfig"):
            config = RetryConfig()
        with step("Verify default values"):
            assert config.max_attempts == 3
            assert config.delay == 1.0
            assert config.backoff == 2.0
            assert config.max_delay is None
            assert config.jitter is False

    @mark.asyncio
    @title("RetryConfig calculate delay")
    @description("Test RetryConfig.calculate_delay() calculates delay correctly.")
    async def test_retry_config_calculate_delay(self) -> None:
        """Test RetryConfig.calculate_delay() calculates delay correctly."""
        with step("Create RetryConfig"):
            config = RetryConfig(delay=1.0, backoff=2.0)
        with step("Calculate delays for attempts (0-indexed)"):
            delay0 = config.calculate_delay(0)  # First retry attempt
            delay1 = config.calculate_delay(1)  # Second retry attempt
            delay2 = config.calculate_delay(2)  # Third retry attempt
        with step("Verify exponential backoff"):
            assert delay0 == 1.0  # 1.0 * 2^0
            assert delay1 == 2.0  # 1.0 * 2^1
            assert delay2 == 4.0  # 1.0 * 2^2

    @mark.asyncio
    @title("RetryConfig max delay caps delay")
    @description("Test RetryConfig.max_delay caps calculated delay.")
    async def test_retry_config_max_delay(self) -> None:
        """Test RetryConfig.max_delay caps calculated delay."""
        with step("Create RetryConfig with max_delay"):
            config = RetryConfig(delay=1.0, backoff=2.0, max_delay=3.0)
        with step("Calculate delay that exceeds max"):
            delay = config.calculate_delay(5)  # Would be 16.0 without max
        with step("Verify delay is capped"):
            assert delay == 3.0

    @mark.asyncio
    @title("RetryConfig calculate delay with jitter")
    @description("Test RetryConfig.calculate_delay() adds jitter when enabled.")
    async def test_retry_config_calculate_delay_with_jitter(self) -> None:
        """Test RetryConfig.calculate_delay() adds jitter when enabled."""
        with step("Create RetryConfig with jitter"):
            config = RetryConfig(delay=1.0, backoff=2.0, jitter=True)
        with step("Calculate delay multiple times"):
            delays = [config.calculate_delay(1) for _ in range(10)]
        with step("Verify jitter adds variation"):
            # Base delay for attempt 1 is 2.0, jitter adds ±10% (0.2)
            # So delays should be in range [1.8, 2.2]
            base_delay = 2.0
            jitter_range = base_delay * 0.1
            for delay in delays:
                assert 1.8 <= delay <= 2.2
            # Verify not all delays are the same (jitter adds randomness)
            assert len(set(delays)) > 1

    @mark.asyncio
    @title("RetryConfig calculate delay with jitter ensures non-negative")
    @description("Test RetryConfig.calculate_delay() with jitter ensures non-negative delay.")
    async def test_retry_config_calculate_delay_jitter_non_negative(self) -> None:
        """Test RetryConfig.calculate_delay() with jitter ensures non-negative delay."""
        with step("Create RetryConfig with jitter"):
            config = RetryConfig(delay=0.1, backoff=1.0, jitter=True)
        with step("Calculate delay multiple times"):
            delays = [config.calculate_delay(0) for _ in range(10)]
        with step("Verify all delays are non-negative"):
            for delay in delays:
                assert delay >= 0.0


class TestRetryHandler:
    """Test RetryHandler class."""

    @mark.asyncio
    @title("RetryHandler handle_error sets should_retry for retryable exception")
    @description("Test RetryHandler.handle_error() sets should_retry for retryable exception.")
    async def test_retry_handler_handles_retryable_error(self) -> None:
        """Test RetryHandler.handle_error() sets should_retry for retryable exception."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )

        with step("Create RetryHandler"):
            config = RetryConfig(max_attempts=3, delay=0.01)
            handler = RetryHandler(config)
        with step("Create request context"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
        with step("Handle retryable error"):
            error = ConnectionError("Temporary error")
            result = await handler.handle_error(context, error)
        with step("Verify should_retry is set and None returned"):
            assert result is None
            assert context.metadata.get("should_retry") is True
            assert context.metadata.get("retry_attempt") == 1

    @mark.asyncio
    @title("RetryHandler handle_error gives up after max attempts")
    @description("Test RetryHandler.handle_error() gives up after max_attempts.")
    async def test_retry_handler_gives_up_after_max_attempts(self) -> None:
        """Test RetryHandler.handle_error() gives up after max_attempts."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )

        with step("Create RetryHandler"):
            config = RetryConfig(max_attempts=2, delay=0.01)
            handler = RetryHandler(config)
        with step("Create request context"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
        with step("Handle error multiple times up to max_attempts"):
            error = ConnectionError("Persistent error")
            # First attempt (attempt 1)
            result1 = await handler.handle_error(context, error)
            assert result1 is None
            assert context.metadata.get("should_retry") is True
            assert context.metadata.get("retry_attempt") == 1
            # Clear should_retry for next attempt
            context.metadata.pop("should_retry", None)
            # Second attempt (attempt 2, should exceed max_attempts=2)
            result2 = await handler.handle_error(context, error)
        with step("Verify retry limit exceeded"):
            assert result2 is None  # Returns None
            # After max_attempts, should_retry should not be set (limit exceeded)
            assert context.metadata.get("should_retry") is None

    @mark.asyncio
    @title("RetryHandler handle_error does not retry non-retryable exception")
    @description("Test RetryHandler.handle_error() does not retry on non-retryable exception.")
    async def test_retry_handler_no_retry_non_retryable(self) -> None:
        """Test RetryHandler.handle_error() does not retry on non-retryable exception."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )

        with step("Create RetryHandler with specific exceptions"):
            config = RetryConfig(
                max_attempts=3, delay=0.01, exceptions=(ConnectionError, TimeoutError)
            )
            handler = RetryHandler(config)
        with step("Create request context"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
        with step("Handle non-retryable error"):
            error = ValueError("Non-retryable error")
            result = await handler.handle_error(context, error)
        with step("Verify no retry is set"):
            assert result is None
            assert context.metadata.get("should_retry") is None

    @mark.asyncio
    @title("RetryHandler initialization with default config")
    @description("Test RetryHandler.__init__() creates default config when None provided.")
    async def test_retry_handler_init_default_config(self) -> None:
        """Test RetryHandler.__init__() creates default config when None provided."""
        with step("Create RetryHandler without config"):
            handler = RetryHandler()
        with step("Verify default config is created"):
            assert handler.config is not None
            assert handler.config.max_attempts == 3
            assert handler.config.delay == 1.0
            assert handler.config.backoff == 2.0
            assert ConnectionError in handler.config.exceptions
            assert TimeoutError in handler.config.exceptions

    @mark.asyncio
    @title("RetryHandler _get_request_key with request_id")
    @description("Test RetryHandler._get_request_key() includes request_id when present.")
    async def test_retry_handler_get_request_key_with_request_id(self) -> None:
        """Test RetryHandler._get_request_key() includes request_id when present."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )

        with step("Create RetryHandler"):
            handler = RetryHandler()
        with step("Create request context with request_id"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query", operation_name="GetUsers"
            )
            context.metadata["request_id"] = "req-123"
        with step("Get request key"):
            key = handler._get_request_key(context)
        with step("Verify key includes request_id"):
            assert "req-123" in key
            assert "query" in key
            assert "GetUsers" in key

"""
Unit tests for retry module.
"""

from unittest.mock import AsyncMock, patch

import allure
import pytest

from py_web_automation.exceptions import ConnectionError, TimeoutError
from py_web_automation.retry import (
    RetryConfig,
    retry_on_connection_error,
    retry_on_failure,
)

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestRetryOnFailure:
    """Test retry_on_failure decorator."""

    @pytest.mark.asyncio
    @allure.title("TC-RETRY-001: retry_on_failure - успешный вызов")
    async def test_retry_on_failure_success(self):
        """Test retry_on_failure doesn't affect successful calls."""
        with allure.step("Create function with retry decorator"):
            call_count = 0

            @retry_on_failure(max_attempts=3, delay=0.1, backoff=2.0)
            async def successful_function():
                nonlocal call_count
                call_count += 1
                return "success"

        with allure.step("Call function successfully"):
            result = await successful_function()

        with allure.step("Verify function called once"):
            assert call_count == 1
            assert result == "success"

    @pytest.mark.asyncio
    @allure.title("TC-RETRY-002: retry_on_failure - повтор при ошибке")
    async def test_retry_on_failure_retries_on_error(self):
        """Test retry_on_failure retries on failure."""
        with allure.step("Create function that fails then succeeds"):
            call_count = 0

            @retry_on_failure(max_attempts=3, delay=0.1, backoff=2.0)
            async def failing_then_success():
                nonlocal call_count
                call_count += 1
                if call_count < 3:
                    raise ValueError("test error")
                return "success"

        with allure.step("Call function"):
            result = await failing_then_success()

        with allure.step("Verify function called 3 times"):
            assert call_count == 3
            assert result == "success"

    @pytest.mark.asyncio
    @allure.title("TC-RETRY-003: retry_on_failure - exponential backoff")
    async def test_retry_on_failure_exponential_backoff(self):
        """Test retry_on_failure uses exponential backoff."""
        with allure.step("Create function with retry and mock sleep"):
            call_count = 0

            @retry_on_failure(max_attempts=3, delay=0.1, backoff=2.0)
            async def failing_function():
                nonlocal call_count
                call_count += 1
                if call_count < 3:
                    raise ValueError("test error")
                return "success"

            with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
                with allure.step("Call function"):
                    await failing_function()

                with allure.step("Verify sleep called with exponential delays"):
                    assert mock_sleep.call_count == 2
                    # First delay: 0.1, second delay: 0.2
                    assert mock_sleep.call_args_list[0][0][0] == pytest.approx(0.1, rel=0.1)
                    assert mock_sleep.call_args_list[1][0][0] == pytest.approx(0.2, rel=0.1)

    @pytest.mark.asyncio
    @allure.title("TC-RETRY-004: retry_on_failure - on_retry callback")
    async def test_retry_on_failure_on_retry_callback(self):
        """Test retry_on_failure calls on_retry callback."""
        with allure.step("Create callback and function"):
            callback_calls = []

            def on_retry(attempt, exception):
                callback_calls.append((attempt, str(exception)))

            call_count = 0

            @retry_on_failure(max_attempts=3, delay=0.1, backoff=2.0, on_retry=on_retry)
            async def failing_function():
                nonlocal call_count
                call_count += 1
                if call_count < 3:
                    raise ValueError("test error")
                return "success"

        with allure.step("Call function"):
            await failing_function()

        with allure.step("Verify callback called for each retry"):
            assert len(callback_calls) == 2
            assert callback_calls[0][0] == 1
            assert callback_calls[1][0] == 2
            assert "test error" in callback_calls[0][1]

    @pytest.mark.asyncio
    @allure.title("TC-RETRY-005: retry_on_failure - исключение после всех попыток")
    async def test_retry_on_failure_raises_after_all_attempts(self):
        """Test retry_on_failure raises exception after all attempts."""
        with allure.step("Create function that always fails"):
            call_count = 0

            @retry_on_failure(max_attempts=3, delay=0.1, backoff=2.0)
            async def always_failing():
                nonlocal call_count
                call_count += 1
                raise ValueError("always fails")

        with allure.step("Call function and expect exception"):
            with pytest.raises(ValueError, match="always fails"):
                await always_failing()

        with allure.step("Verify function called 3 times"):
            assert call_count == 3

    @pytest.mark.asyncio
    @allure.title("TC-RETRY-006: retry_on_failure - специфичные исключения")
    async def test_retry_on_failure_specific_exceptions(self):
        """Test retry_on_failure only retries on specified exceptions."""
        with allure.step("Create function that raises different exception"):
            call_count = 0

            @retry_on_failure(max_attempts=3, delay=0.1, exceptions=(ConnectionError,))
            async def raises_value_error():
                nonlocal call_count
                call_count += 1
                raise ValueError("not retried")

        with allure.step("Call function and expect immediate exception"):
            with pytest.raises(ValueError, match="not retried"):
                await raises_value_error()

        with allure.step("Verify function called only once"):
            assert call_count == 1


@pytest.mark.unit
class TestRetryOnConnectionError:
    """Test retry_on_connection_error decorator."""

    @pytest.mark.asyncio
    @allure.title("TC-RETRY-007: retry_on_connection_error - ConnectionError")
    async def test_retry_on_connection_error_retries(self):
        """Test retry_on_connection_error retries on ConnectionError."""
        with allure.step("Create function that raises ConnectionError"):
            call_count = 0

            @retry_on_connection_error(max_attempts=3, delay=0.1)
            async def connection_error_then_success():
                nonlocal call_count
                call_count += 1
                if call_count < 2:
                    raise ConnectionError("connection failed")
                return "success"

        with allure.step("Call function"):
            result = await connection_error_then_success()

        with allure.step("Verify function retried"):
            assert call_count == 2
            assert result == "success"

    @pytest.mark.asyncio
    @allure.title("TC-RETRY-008: retry_on_connection_error - TimeoutError")
    async def test_retry_on_connection_error_timeout(self):
        """Test retry_on_connection_error retries on TimeoutError."""
        with allure.step("Create function that raises TimeoutError"):
            call_count = 0

            @retry_on_connection_error(max_attempts=3, delay=0.1)
            async def timeout_error_then_success():
                nonlocal call_count
                call_count += 1
                if call_count < 2:
                    raise TimeoutError("timeout")
                return "success"

        with allure.step("Call function"):
            result = await timeout_error_then_success()

        with allure.step("Verify function retried"):
            assert call_count == 2
            assert result == "success"


@pytest.mark.unit
class TestRetryConfig:
    """Test RetryConfig class."""

    @allure.title("TC-RETRY-009: RetryConfig - calculate_delay")
    def test_retry_config_calculate_delay(self):
        """Test RetryConfig delay calculation."""
        with allure.step("Create RetryConfig"):
            config = RetryConfig(delay=1.0, backoff=2.0)

        with allure.step("Calculate delays for different attempts"):
            delay_0 = config.calculate_delay(0)
            delay_1 = config.calculate_delay(1)
            delay_2 = config.calculate_delay(2)

        with allure.step("Verify exponential backoff"):
            assert delay_0 == pytest.approx(1.0, rel=0.1)
            assert delay_1 == pytest.approx(2.0, rel=0.1)
            assert delay_2 == pytest.approx(4.0, rel=0.1)

    @allure.title("TC-RETRY-010: RetryConfig - max_delay ограничение")
    def test_retry_config_max_delay(self):
        """Test RetryConfig max_delay limits delay."""
        with allure.step("Create RetryConfig with max_delay"):
            config = RetryConfig(delay=1.0, backoff=2.0, max_delay=5.0)

        with allure.step("Calculate delay for high attempt"):
            delay_0 = config.calculate_delay(0)  # 1.0
            delay_2 = config.calculate_delay(2)  # 4.0
            delay_10 = config.calculate_delay(10)  # Should be capped at 5.0

        with allure.step("Verify delay capped at max_delay"):
            assert delay_0 == pytest.approx(1.0, rel=0.1)
            assert delay_2 == pytest.approx(4.0, rel=0.1)
            assert delay_10 == pytest.approx(5.0, rel=0.1)

    @allure.title("TC-RETRY-011: RetryConfig - jitter")
    def test_retry_config_jitter(self):
        """Test RetryConfig jitter adds randomness."""
        with allure.step("Create RetryConfig with jitter"):
            config = RetryConfig(delay=1.0, backoff=2.0, jitter=True)

        with allure.step("Calculate delay multiple times"):
            delays = [config.calculate_delay(1) for _ in range(10)]

        with allure.step("Verify delays vary (within ±10% range)"):
            # Delays should vary but be within 2.0 ± 0.2
            assert all(1.8 <= d <= 2.2 for d in delays)
            # At least some variation
            assert len(set(delays)) > 1

    @allure.title("TC-RETRY-012: RetryConfig - to_dict")
    def test_retry_config_to_dict(self):
        """Test RetryConfig conversion to dictionary."""
        with allure.step("Create RetryConfig"):
            config = RetryConfig(max_attempts=5, delay=1.0, backoff=2.0, exceptions=(ValueError,))

        with allure.step("Convert to dictionary"):
            config_dict = config.to_dict()

        with allure.step("Verify dictionary contains config values"):
            assert config_dict["max_attempts"] == 5
            assert config_dict["delay"] == 1.0
            assert config_dict["backoff"] == 2.0
            assert config_dict["exceptions"] == (ValueError,)

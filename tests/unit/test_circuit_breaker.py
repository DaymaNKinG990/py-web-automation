"""
Unit tests for circuit_breaker module.
"""

from datetime import datetime, timedelta

import allure
import pytest

from py_web_automation.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerStats,
    CircuitState,
)
from py_web_automation.exceptions import ConnectionError

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestCircuitBreaker:
    """Test CircuitBreaker class."""

    @allure.title("TC-CB-001: CircuitBreaker - инициализация")
    def test_circuit_breaker_init(self):
        """Test CircuitBreaker initialization."""
        with allure.step("Create CircuitBreaker with default config"):
            breaker = CircuitBreaker()

        with allure.step("Verify config and stats initialized"):
            assert breaker.config.failure_threshold == 5
            assert breaker.config.timeout == 60.0
            assert breaker.stats.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    @allure.title("TC-CB-002: CircuitBreaker - call успешный")
    async def test_circuit_breaker_call_success(self):
        """Test successful call through circuit breaker."""
        with allure.step("Create CircuitBreaker in CLOSED state"):
            breaker = CircuitBreaker()

        with allure.step("Call call() with successful function"):

            async def success_func():
                return "success"

            result = await breaker.call(success_func)

        with allure.step("Verify function result returned"):
            assert result == "success"
            assert breaker.stats.successes == 1
            assert breaker.stats.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    @allure.title("TC-CB-003: CircuitBreaker - call открывает circuit при ошибках")
    async def test_circuit_breaker_call_opens_circuit(self):
        """Test circuit opens after failure threshold."""
        with allure.step("Create CircuitBreaker with low failure_threshold"):
            breaker = CircuitBreaker(failure_threshold=2)

        with allure.step("Call call() with failing function 2 times"):

            async def failing_func():
                raise ValueError("test error")

            for _ in range(2):
                try:
                    await breaker.call(failing_func)
                except ValueError:
                    pass

        with allure.step("Verify circuit state = OPEN"):
            assert breaker.stats.state == CircuitState.OPEN
            assert breaker.stats.failures == 2

    @pytest.mark.asyncio
    @allure.title("TC-CB-004: CircuitBreaker - call блокирует при OPEN")
    async def test_circuit_breaker_call_blocks_when_open(self):
        """Test call blocked when circuit is OPEN."""
        with allure.step("Create CircuitBreaker in OPEN state"):
            breaker = CircuitBreaker(failure_threshold=1, timeout=60.0)
            breaker.stats.state = CircuitState.OPEN
            breaker.stats.opened_at = datetime.now()

        with allure.step("Call call() with function"):

            async def func():
                return "result"

            with allure.step("Verify ConnectionError raised"):
                with pytest.raises(ConnectionError, match="Circuit breaker is OPEN"):
                    await breaker.call(func)

    @pytest.mark.asyncio
    @allure.title("TC-CB-005: CircuitBreaker - переход в HALF_OPEN")
    async def test_circuit_breaker_transition_to_half_open(self):
        """Test transition to HALF_OPEN after timeout."""
        with allure.step("Create CircuitBreaker in OPEN state"):
            breaker = CircuitBreaker(failure_threshold=1, timeout=0.1)  # Short timeout
            breaker.stats.state = CircuitState.OPEN
            breaker.stats.opened_at = datetime.now() - timedelta(seconds=0.2)

        with allure.step("Wait for timeout and call call()"):

            async def func():
                return "result"

            result = await breaker.call(func)

        with allure.step("Verify state = HALF_OPEN"):
            assert breaker.stats.state == CircuitState.HALF_OPEN
            assert result == "result"

    @pytest.mark.asyncio
    @allure.title("TC-CB-006: CircuitBreaker - закрытие из HALF_OPEN")
    async def test_circuit_breaker_closes_from_half_open(self):
        """Test circuit closes from HALF_OPEN after successes."""
        with allure.step("Create CircuitBreaker in HALF_OPEN state"):
            breaker = CircuitBreaker(success_threshold=2)
            breaker.stats.state = CircuitState.HALF_OPEN
            breaker.stats.successes = 0

        with allure.step("Call call() with successful function success_threshold times"):

            async def success_func():
                return "success"

            for _ in range(2):
                await breaker.call(success_func)

        with allure.step("Verify state = CLOSED"):
            assert breaker.stats.state == CircuitState.CLOSED
            assert breaker.stats.failures == 0

    @pytest.mark.asyncio
    @allure.title("TC-CB-007: CircuitBreaker - возврат в OPEN из HALF_OPEN")
    async def test_circuit_breaker_reopens_from_half_open(self):
        """Test circuit reopens on failure in HALF_OPEN."""
        with allure.step("Create CircuitBreaker in HALF_OPEN state"):
            breaker = CircuitBreaker()
            breaker.stats.state = CircuitState.HALF_OPEN

        with allure.step("Call call() with failing function"):

            async def failing_func():
                raise ValueError("test error")

            with pytest.raises(ValueError):
                await breaker.call(failing_func)

        with allure.step("Verify state = OPEN"):
            assert breaker.stats.state == CircuitState.OPEN

    @allure.title("TC-CB-008: CircuitBreaker - reset")
    def test_circuit_breaker_reset(self):
        """Test manual reset."""
        with allure.step("Create CircuitBreaker in OPEN state"):
            breaker = CircuitBreaker()
            breaker.stats.state = CircuitState.OPEN
            breaker.stats.failures = 5

        with allure.step("Call reset"):
            breaker.reset()

        with allure.step("Verify state = CLOSED, stats reset"):
            assert breaker.stats.state == CircuitState.CLOSED
            assert breaker.stats.failures == 0
            assert breaker.stats.successes == 0

    @allure.title("TC-CB-009: CircuitBreaker - get_state и get_stats")
    def test_circuit_breaker_get_state_and_stats(self):
        """Test state and stats retrieval."""
        with allure.step("Create CircuitBreaker"):
            breaker = CircuitBreaker()

        with allure.step("Record some successes/failures"):
            breaker.stats.successes = 3
            breaker.stats.failures = 1

        with allure.step("Call get_state() and get_stats()"):
            state = breaker.get_state()
            stats = breaker.get_stats()

        with allure.step("Verify correct values returned"):
            assert state == CircuitState.CLOSED
            assert stats.successes == 3
            assert stats.failures == 1


@pytest.mark.unit
class TestCircuitBreakerConfig:
    """Test CircuitBreakerConfig class."""

    @allure.title("TC-CB-010: CircuitBreakerConfig - инициализация")
    def test_circuit_breaker_config_init(self):
        """Test CircuitBreakerConfig initialization."""
        with allure.step("Create CircuitBreakerConfig"):
            config = CircuitBreakerConfig(
                failure_threshold=10,
                timeout=120.0,
                success_threshold=3,
                expected_exception=ValueError,
            )

        with allure.step("Verify all fields set correctly"):
            assert config.failure_threshold == 10
            assert config.timeout == 120.0
            assert config.success_threshold == 3
            assert config.expected_exception is ValueError


@pytest.mark.unit
class TestCircuitBreakerStats:
    """Test CircuitBreakerStats class."""

    @allure.title("TC-CB-011: CircuitBreakerStats - инициализация")
    def test_circuit_breaker_stats_init(self):
        """Test CircuitBreakerStats initialization."""
        with allure.step("Create CircuitBreakerStats"):
            stats = CircuitBreakerStats()

        with allure.step("Verify default values"):
            assert stats.failures == 0
            assert stats.successes == 0
            assert stats.state == CircuitState.CLOSED
            assert stats.last_failure_time is None
            assert stats.last_success_time is None

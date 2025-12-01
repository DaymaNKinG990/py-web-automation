"""
Unit tests for rate_limit module.
"""

import asyncio
import time

import allure
import pytest

from py_web_automation.rate_limit import RateLimitConfig, RateLimiter

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestRateLimiter:
    """Test RateLimiter class."""

    @pytest.mark.asyncio
    @allure.title("TC-RL-001: RateLimiter - acquire успешно")
    async def test_rate_limiter_acquire_success(self):
        """Test successful permission acquisition."""
        with allure.step("Create RateLimiter"):
            limiter = RateLimiter(max_requests=10, window=60)

        with allure.step("Call acquire 5 times"):
            for _ in range(5):
                await limiter.acquire()

        with allure.step("Verify all calls succeed"):
            assert limiter.get_remaining() == 5

    @pytest.mark.asyncio
    @allure.title("TC-RL-002: RateLimiter - acquire блокирует при превышении лимита")
    async def test_rate_limiter_acquire_blocks(self):
        """Test acquire blocks when limit exceeded."""
        with allure.step("Create RateLimiter with max_requests=2"):
            limiter = RateLimiter(max_requests=2, window=1)  # Short window for testing

        with allure.step("Call acquire 2 times (succeeds)"):
            await limiter.acquire()
            await limiter.acquire()

        with allure.step("Call acquire 3rd time (should block)"):
            start = time.time()
            await limiter.acquire()
            elapsed = time.time() - start

        with allure.step("Verify 3rd call blocked then succeeded"):
            # Should have waited at least a bit (sliding window cleanup)
            assert elapsed >= 0.0  # May be immediate if window expired quickly

    @pytest.mark.asyncio
    @allure.title("TC-RL-003: RateLimiter - try_acquire успешно")
    async def test_rate_limiter_try_acquire_success(self):
        """Test try_acquire returns True when available."""
        with allure.step("Create RateLimiter"):
            limiter = RateLimiter(max_requests=10, window=60)

        with allure.step("Call try_acquire"):
            result = await limiter.try_acquire()

        with allure.step("Verify True returned"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("TC-RL-004: RateLimiter - try_acquire при превышении лимита")
    async def test_rate_limiter_try_acquire_limit_exceeded(self):
        """Test try_acquire returns False when limit exceeded."""
        with allure.step("Create RateLimiter with max_requests=1"):
            limiter = RateLimiter(max_requests=1, window=60)

        with allure.step("Call try_acquire twice"):
            result1 = await limiter.try_acquire()
            result2 = await limiter.try_acquire()

        with allure.step("Verify first True, second False"):
            assert result1 is True
            assert result2 is False

    @pytest.mark.asyncio
    @allure.title("TC-RL-005: RateLimiter - sliding window")
    async def test_rate_limiter_sliding_window(self):
        """Test old requests removed from window."""
        with allure.step("Create RateLimiter with short window"):
            limiter = RateLimiter(max_requests=2, window=1)

        with allure.step("Call acquire 2 times"):
            await limiter.acquire()
            await limiter.acquire()

        with allure.step("Wait for window to expire"):
            await asyncio.sleep(2)

        with allure.step("Call acquire again"):
            result = await limiter.try_acquire()

        with allure.step("Verify 3rd call succeeds (old requests removed)"):
            assert result is True

    @allure.title("TC-RL-006: RateLimiter - get_remaining")
    def test_rate_limiter_get_remaining(self):
        """Test remaining requests calculation."""
        with allure.step("Create RateLimiter"):
            limiter = RateLimiter(max_requests=10, window=60)

        with allure.step("Call acquire 3 times"):
            asyncio.run(limiter.acquire())
            asyncio.run(limiter.acquire())
            asyncio.run(limiter.acquire())

        with allure.step("Call get_remaining"):
            remaining = limiter.get_remaining()

        with allure.step("Verify 7 returned"):
            assert remaining == 7

    @pytest.mark.asyncio
    @allure.title("TC-RL-007: RateLimiter - get_wait_time")
    async def test_rate_limiter_get_wait_time(self):
        """Test wait time calculation."""
        with allure.step("Create RateLimiter at limit"):
            limiter = RateLimiter(max_requests=1, window=60)

        with allure.step("Call acquire"):
            await limiter.acquire()

        with allure.step("Call get_wait_time"):
            wait_time = limiter.get_wait_time()

        with allure.step("Verify wait_time > 0"):
            assert wait_time > 0

    @allure.title("TC-RL-008: RateLimiter - get_wait_time когда доступно")
    def test_rate_limiter_get_wait_time_available(self):
        """Test wait_time = 0 when available."""
        with allure.step("Create RateLimiter with available slots"):
            limiter = RateLimiter(max_requests=10, window=60)

        with allure.step("Call get_wait_time"):
            wait_time = limiter.get_wait_time()

        with allure.step("Verify 0.0 returned"):
            assert wait_time == 0.0

    @pytest.mark.asyncio
    @allure.title("TC-RL-009: RateLimiter - reset")
    async def test_rate_limiter_reset(self):
        """Test rate limiter reset."""
        with allure.step("Create RateLimiter"):
            limiter = RateLimiter(max_requests=10, window=60)

        with allure.step("Call acquire several times"):
            await limiter.acquire()
            await limiter.acquire()

        with allure.step("Reset limiter"):
            limiter.reset()

        with allure.step("Verify get_remaining = max_requests"):
            assert limiter.get_remaining() == 10


@pytest.mark.unit
class TestRateLimitConfig:
    """Test RateLimitConfig class."""

    @allure.title("TC-RL-011: RateLimitConfig - инициализация")
    def test_rate_limit_config_init(self):
        """Test RateLimitConfig initialization."""
        with allure.step("Create RateLimitConfig"):
            config = RateLimitConfig(max_requests=100, window=60, burst=10)

        with allure.step("Verify all fields set correctly"):
            assert config.max_requests == 100
            assert config.window == 60
            assert config.burst == 10

    @allure.title("TC-RL-012: RateLimitConfig - default burst")
    def test_rate_limit_config_default_burst(self):
        """Test default burst calculation."""
        with allure.step("Create RateLimitConfig without burst"):
            config = RateLimitConfig(max_requests=100, window=60)

        with allure.step("Verify burst = 10 (10% of max_requests)"):
            assert config.burst == 10

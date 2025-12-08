"""
Unit tests for RateLimiter and RateLimitConfig.
"""

# Python imports
import asyncio
from allure import title, description, step
from pytest import mark

# Local imports
from py_web_automation.clients.api_clients.graphql_client.rate_limit import (
    RateLimiter,
    RateLimitConfig,
)

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestRateLimitConfig:
    """Test RateLimitConfig class."""

    @mark.asyncio
    @title("RateLimitConfig initialization")
    @description("Test RateLimitConfig initializes with default values.")
    async def test_rate_limit_config_init(self) -> None:
        """Test RateLimitConfig initializes with default values."""
        with step("Create RateLimitConfig"):
            config = RateLimitConfig()
        with step("Verify default values"):
            assert config.max_requests == 100
            assert config.window == 60
            assert config.burst == 10

    @mark.asyncio
    @title("RateLimitConfig custom values")
    @description("Test RateLimitConfig initializes with custom values.")
    async def test_rate_limit_config_custom_values(self) -> None:
        """Test RateLimitConfig initializes with custom values."""
        with step("Create RateLimitConfig with custom values"):
            config = RateLimitConfig(max_requests=50, window=30, burst=5)
        with step("Verify custom values"):
            assert config.max_requests == 50
            assert config.window == 30
            assert config.burst == 5


class TestRateLimiter:
    """Test RateLimiter class."""

    @mark.asyncio
    @title("RateLimiter acquire allows request within limit")
    @description("Test RateLimiter.acquire() allows request within rate limit.")
    async def test_rate_limiter_acquire_within_limit(self) -> None:
        """Test RateLimiter.acquire() allows request within rate limit."""
        with step("Create RateLimiter"):
            limiter = RateLimiter(max_requests=10, window=60)
        with step("Acquire permission"):
            await limiter.acquire()
        with step("Verify request was allowed"):
            assert len(limiter.requests) == 1

    @mark.asyncio
    @title("RateLimiter blocks when limit exceeded")
    @description("Test RateLimiter.acquire() blocks when rate limit is exceeded.")
    async def test_rate_limiter_blocks_when_exceeded(self) -> None:
        """Test RateLimiter.acquire() blocks when rate limit is exceeded."""
        with step("Create RateLimiter with low limit"):
            limiter = RateLimiter(max_requests=2, window=1)
        with step("Acquire up to limit"):
            await limiter.acquire()
            await limiter.acquire()
        with step("Verify limit reached"):
            assert len(limiter.requests) == 2
        with step("Next acquire should block"):
            # This should block until window expires
            # In test, we'll just verify it doesn't raise immediately
            task = asyncio.create_task(limiter.acquire())
            await asyncio.sleep(0.1)
            # Task should still be pending (blocked)
            assert not task.done()
            task.cancel()

    @mark.asyncio
    @title("RateLimiter burst configuration")
    @description("Test RateLimiter stores burst configuration correctly.")
    async def test_rate_limiter_burst_config(self) -> None:
        """Test RateLimiter stores burst configuration correctly."""
        with step("Create RateLimiter with burst"):
            limiter = RateLimiter(max_requests=2, window=1, burst=2)
        with step("Verify burst is stored in config"):
            assert limiter.config.burst == 2
        with step("Note: burst logic is not implemented in _is_rate_limit_exceeded"):
            # Current implementation only checks max_requests, not max_requests + burst
            # This test verifies config is stored, actual burst behavior may need implementation
            assert limiter.config.max_requests == 2

    @mark.asyncio
    @title("RateLimiter resets after window")
    @description("Test RateLimiter resets requests after window expires.")
    async def test_rate_limiter_resets_after_window(self) -> None:
        """Test RateLimiter resets requests after window expires."""
        with step("Create RateLimiter with short window"):
            limiter = RateLimiter(max_requests=2, window=1)
        with step("Acquire up to limit"):
            await limiter.acquire()
            await limiter.acquire()
        with step("Wait for window to expire"):
            await asyncio.sleep(1.1)
        with step("Acquire should succeed after window"):
            await limiter.acquire()
            assert len(limiter.requests) == 1  # Old requests cleared

    @mark.asyncio
    @title("RateLimiter try_acquire succeeds when limit not exceeded")
    @description("Test RateLimiter.try_acquire() returns True when limit not exceeded.")
    async def test_rate_limiter_try_acquire_succeeds(self) -> None:
        """Test RateLimiter.try_acquire() returns True when limit not exceeded."""
        with step("Create RateLimiter"):
            limiter = RateLimiter(max_requests=5, window=60)
        with step("Try acquire permission"):
            result = await limiter.try_acquire()
        with step("Verify permission granted"):
            assert result is True
            assert len(limiter.requests) == 1

    @mark.asyncio
    @title("RateLimiter try_acquire fails when limit exceeded")
    @description("Test RateLimiter.try_acquire() returns False when limit exceeded.")
    async def test_rate_limiter_try_acquire_fails(self) -> None:
        """Test RateLimiter.try_acquire() returns False when limit exceeded."""
        with step("Create RateLimiter with low limit"):
            limiter = RateLimiter(max_requests=2, window=60)
        with step("Acquire up to limit"):
            await limiter.acquire()
            await limiter.acquire()
        with step("Try acquire should fail"):
            result = await limiter.try_acquire()
        with step("Verify permission denied"):
            assert result is False
            assert len(limiter.requests) == 2

    @mark.asyncio
    @title("RateLimiter reset clears all requests")
    @description("Test RateLimiter.reset() clears all request history.")
    async def test_rate_limiter_reset(self) -> None:
        """Test RateLimiter.reset() clears all request history."""
        with step("Create RateLimiter and acquire requests"):
            limiter = RateLimiter(max_requests=10, window=60)
            await limiter.acquire()
            await limiter.acquire()
            await limiter.acquire()
        with step("Verify requests recorded"):
            assert len(limiter.requests) == 3
        with step("Reset limiter"):
            limiter.reset()
        with step("Verify all requests cleared"):
            assert len(limiter.requests) == 0

    @mark.asyncio
    @title("RateLimiter get_remaining returns correct count")
    @description("Test RateLimiter.get_remaining() returns correct remaining requests.")
    async def test_rate_limiter_get_remaining(self) -> None:
        """Test RateLimiter.get_remaining() returns correct remaining requests."""
        with step("Create RateLimiter"):
            limiter = RateLimiter(max_requests=5, window=60)
        with step("Get remaining when empty"):
            remaining = limiter.get_remaining()
        with step("Verify full limit available"):
            assert remaining == 5
        with step("Acquire some requests"):
            await limiter.acquire()
            await limiter.acquire()
        with step("Get remaining after requests"):
            remaining = limiter.get_remaining()
        with step("Verify remaining count"):
            assert remaining == 3

    @mark.asyncio
    @title("RateLimiter get_remaining cleans old requests")
    @description("Test RateLimiter.get_remaining() cleans old requests outside window.")
    async def test_rate_limiter_get_remaining_cleans_old(self) -> None:
        """Test RateLimiter.get_remaining() cleans old requests outside window."""
        with step("Create RateLimiter with short window"):
            limiter = RateLimiter(max_requests=5, window=1)
        with step("Acquire requests"):
            await limiter.acquire()
            await limiter.acquire()
        with step("Wait for window to expire"):
            await asyncio.sleep(1.1)
        with step("Get remaining should clean old requests"):
            remaining = limiter.get_remaining()
        with step("Verify old requests cleaned"):
            assert remaining == 5
            assert len(limiter.requests) == 0

    @mark.asyncio
    @title("RateLimiter get_wait_time returns zero when limit not exceeded")
    @description("Test RateLimiter.get_wait_time() returns 0.0 when limit not exceeded.")
    async def test_rate_limiter_get_wait_time_zero(self) -> None:
        """Test RateLimiter.get_wait_time() returns 0.0 when limit not exceeded."""
        with step("Create RateLimiter"):
            limiter = RateLimiter(max_requests=5, window=60)
        with step("Acquire some requests"):
            await limiter.acquire()
            await limiter.acquire()
        with step("Get wait time"):
            wait_time = limiter.get_wait_time()
        with step("Verify no wait needed"):
            assert wait_time == 0.0

    @mark.asyncio
    @title("RateLimiter get_wait_time returns correct wait time when limit exceeded")
    @description("Test RateLimiter.get_wait_time() returns correct wait time when limit exceeded.")
    async def test_rate_limiter_get_wait_time_exceeded(self) -> None:
        """Test RateLimiter.get_wait_time() returns correct wait time when limit exceeded."""
        with step("Create RateLimiter with short window"):
            limiter = RateLimiter(max_requests=2, window=1)
        with step("Acquire up to limit"):
            await limiter.acquire()
            await limiter.acquire()
        with step("Get wait time"):
            wait_time = limiter.get_wait_time()
        with step("Verify wait time is positive"):
            assert wait_time > 0.0
            assert wait_time <= 1.0  # Should be within window

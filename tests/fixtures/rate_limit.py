"""
Fixtures for RateLimiter testing with automatic cleanup.
"""

# Python imports
from pytest import fixture

# Local imports
from py_web_automation.clients.api_clients.http_client.rate_limit import RateLimiter


@fixture
def rate_limiter() -> RateLimiter:
    """Create RateLimiter instance with automatic cleanup."""
    limiter = RateLimiter(max_requests=10, window=60)
    yield limiter
    limiter.reset()


@fixture
def rate_limiter_short_window() -> RateLimiter:
    """Create RateLimiter with short window for testing."""
    limiter = RateLimiter(max_requests=2, window=1)
    yield limiter
    limiter.reset()


@fixture
def rate_limiter_single() -> RateLimiter:
    """Create RateLimiter with max_requests=1 for testing."""
    limiter = RateLimiter(max_requests=1, window=60)
    yield limiter
    limiter.reset()

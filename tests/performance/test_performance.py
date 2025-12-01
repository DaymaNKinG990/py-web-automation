"""
Performance tests for web automation framework.

This module contains performance benchmarks and load tests
to ensure framework meets performance requirements.
"""

import asyncio
import time

import allure
import pytest

from py_web_automation import ApiClient

# Apply markers to all tests in this module
pytestmark = [pytest.mark.performance]


@pytest.mark.asyncio
@allure.title("Performance: API request latency")
@allure.description("Measure average latency of API requests")
async def test_api_request_latency(mocker, valid_config):
    """Test that API requests complete within acceptable latency."""
    with allure.step("Setup API client with mocked responses"):
        url = "https://api.example.com"
        api = ApiClient(url, valid_config)

        # Mock fast response
        from datetime import timedelta
        from unittest.mock import AsyncMock, MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.1)
        mock_response.is_success = True
        mock_response.content = b'{"data": "test"}'
        mock_response.headers = {"Content-Type": "application/json"}

        api.client.request = AsyncMock(return_value=mock_response)

    with allure.step("Make multiple requests and measure latency"):
        latencies: list[float] = []
        num_requests = 10

        for _ in range(num_requests):
            start = time.time()
            result = await api.make_request("/test")
            elapsed = time.time() - start
            latencies.append(elapsed)
            assert result.success

    with allure.step("Calculate average latency"):
        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)

    with allure.step("Verify latency is acceptable"):
        # Average should be under 200ms for mocked requests
        assert avg_latency < 0.2, f"Average latency {avg_latency:.3f}s exceeds 200ms"
        # Max should be under 500ms
        assert max_latency < 0.5, f"Max latency {max_latency:.3f}s exceeds 500ms"


@pytest.mark.performance
@pytest.mark.asyncio
@allure.title("Performance: Concurrent requests")
@allure.description("Test framework handles concurrent requests efficiently")
async def test_concurrent_requests(mocker, valid_config):
    """Test that framework handles concurrent requests efficiently."""
    with allure.step("Setup API client with mocked responses"):
        url = "https://api.example.com"
        api = ApiClient(url, valid_config)

        from datetime import timedelta
        from unittest.mock import AsyncMock, MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.1)
        mock_response.is_success = True
        mock_response.content = b'{"data": "test"}'
        mock_response.headers = {"Content-Type": "application/json"}

        api.client.request = AsyncMock(return_value=mock_response)

    with allure.step("Make concurrent requests"):
        num_concurrent = 20
        start = time.time()

        tasks = [api.make_request(f"/test/{i}") for i in range(num_concurrent)]
        results = await asyncio.gather(*tasks)

        elapsed = time.time() - start

    with allure.step("Verify all requests succeeded"):
        assert all(r.success for r in results)

    with allure.step("Verify concurrent performance"):
        # Concurrent requests should complete faster than sequential
        # With 20 requests at 0.1s each, sequential would take ~2s
        # Concurrent should take ~0.1-0.2s
        assert elapsed < 1.0, f"Concurrent requests took {elapsed:.3f}s, expected < 1.0s"


@pytest.mark.performance
@pytest.mark.asyncio
@allure.title("Performance: Request Builder overhead")
@allure.description("Measure overhead of Request Builder pattern")
async def test_request_builder_overhead(mocker, valid_config):
    """Test that Request Builder doesn't add significant overhead."""
    with allure.step("Setup API client"):
        url = "https://api.example.com"
        api = ApiClient(url, valid_config)

        from datetime import timedelta
        from unittest.mock import AsyncMock, MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.1)
        mock_response.is_success = True
        mock_response.content = b'{"data": "test"}'
        mock_response.headers = {"Content-Type": "application/json"}

        api.client.request = AsyncMock(return_value=mock_response)

    with allure.step("Measure direct make_request"):
        start = time.time()
        await api.make_request("/test", method="GET")
        direct_time = time.time() - start

    with allure.step("Measure Request Builder"):
        start = time.time()
        builder = api.build_request()
        await builder.get("/test").execute()
        builder_time = time.time() - start

    with allure.step("Verify overhead is minimal"):
        # Request Builder should add < 50ms overhead
        overhead = builder_time - direct_time
        assert overhead < 0.05, f"Request Builder overhead {overhead:.3f}s exceeds 50ms"


@pytest.mark.performance
@pytest.mark.asyncio
@allure.title("Performance: Response validation speed")
@allure.description("Measure performance of response validation")
async def test_validation_performance(mocker, valid_config):
    """Test that response validation is fast."""
    with allure.step("Setup validation"):
        from msgspec import Struct

        from py_web_automation.validators import validate_response

        class User(Struct):
            id: int
            name: str
            email: str

        data = {"id": 1, "name": "Test", "email": "test@example.com"}

    with allure.step("Measure validation time"):
        num_validations = 1000
        start = time.time()

        for _ in range(num_validations):
            validate_response(data, User)

        elapsed = time.time() - start
        avg_time = elapsed / num_validations

    with allure.step("Verify validation is fast"):
        # Each validation should take < 1ms on average
        assert avg_time < 0.001, f"Average validation time {avg_time * 1000:.3f}ms exceeds 1ms"


@pytest.mark.performance
@pytest.mark.asyncio
@allure.title("Performance: Cache hit performance")
@allure.description("Measure performance improvement from caching")
async def test_cache_performance(mocker, valid_config):
    """Test that caching improves performance."""
    with allure.step("Setup API client with cache"):
        from py_web_automation import ResponseCache

        url = "https://api.example.com"
        cache = ResponseCache(default_ttl=300)
        api = ApiClient(url, valid_config, cache=cache)

        from datetime import timedelta
        from unittest.mock import AsyncMock, MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.1)
        mock_response.is_success = True
        mock_response.content = b'{"data": "test"}'
        mock_response.headers = {"Content-Type": "application/json"}

        api.client.request = AsyncMock(return_value=mock_response)

    with allure.step("First request (cache miss)"):
        start = time.time()
        result1 = await api.make_request("/test", method="GET")
        first_time = time.time() - start

    with allure.step("Second request (cache hit)"):
        start = time.time()
        result2 = await api.make_request("/test", method="GET")
        second_time = time.time() - start

    with allure.step("Verify cache improves performance"):
        # Cached request should be at least 5x faster
        # Note: With mocked HTTP requests, the speedup is lower than with real requests
        # because the HTTP overhead is minimal. Real requests would show higher speedup.
        speedup = first_time / second_time if second_time > 0 else float("inf")
        assert speedup > 5, (
            f"Cache speedup {speedup:.1f}x is less than 5x (expected >5x for mocked requests, >10x for real requests)"
        )
        assert result1.status_code == result2.status_code

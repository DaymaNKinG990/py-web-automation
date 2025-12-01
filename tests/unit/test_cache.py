"""
Unit tests for cache module.
"""

import time
from datetime import datetime

import allure
import pytest

from py_web_automation.cache import CacheEntry, ResponseCache
from py_web_automation.clients.models import ApiResult

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestResponseCache:
    """Test ResponseCache class."""

    @allure.title("TC-CACHE-001: ResponseCache - get cache hit")
    @allure.description("Test getting cached value. TC-CACHE-001")
    def test_cache_get_hit(self):
        """Test getting cached value."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Save value through set"):
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
            cache.set("GET", "https://api.example.com/test", result)

        with allure.step("Get value through get"):
            cached_result = cache.get("GET", "https://api.example.com/test")

        with allure.step("Verify value matches"):
            assert cached_result is not None
            assert cached_result.status_code == 200
            assert cached_result.success is True

    @allure.title("TC-CACHE-002: ResponseCache - get cache miss")
    @allure.description("Test None returned when not in cache. TC-CACHE-002")
    def test_cache_get_miss(self):
        """Test None returned when not in cache."""
        with allure.step("Create empty ResponseCache"):
            cache = ResponseCache()

        with allure.step("Get value for non-existent key"):
            result = cache.get("GET", "https://api.example.com/nonexistent")

        with allure.step("Verify None returned"):
            assert result is None

    @allure.title("TC-CACHE-003: ResponseCache - expired entry")
    @allure.description("Test expired entries not returned. TC-CACHE-003")
    def test_cache_expired_entry(self):
        """Test expired entries not returned."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Save value with short ttl"):
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
            cache.set("GET", "https://api.example.com/test", result, ttl=1)

        with allure.step("Wait for expiration"):
            time.sleep(2)

        with allure.step("Get expired value"):
            cached_result = cache.get("GET", "https://api.example.com/test")

        with allure.step("Verify None returned and entry removed"):
            assert cached_result is None
            assert cache.size() == 0

    @allure.title("TC-CACHE-004: ResponseCache - max_size ограничение")
    @allure.description("Test max_size limits cache size. TC-CACHE-004")
    def test_cache_max_size(self):
        """Test max_size limits cache size."""
        with allure.step("Create ResponseCache with max_size=2"):
            cache = ResponseCache(max_size=2)

        with allure.step("Save 3 values"):
            for i in range(3):
                result = ApiResult(
                    endpoint=f"/test{i}",
                    method="GET",
                    status_code=200,
                    response_time=0.5,
                    success=True,
                    redirect=False,
                    client_error=False,
                    server_error=False,
                    informational=False,
                )
                cache.set("GET", f"https://api.example.com/test{i}", result)

        with allure.step("Verify cache size = 2"):
            assert cache.size() == 2

        with allure.step("Verify oldest value removed (FIFO)"):
            # First value should be removed
            assert cache.get("GET", "https://api.example.com/test0") is None
            # Last two should be present
            assert cache.get("GET", "https://api.example.com/test1") is not None
            assert cache.get("GET", "https://api.example.com/test2") is not None

    @allure.title("TC-CACHE-005: ResponseCache - _make_key одинаковые параметры")
    @allure.description("Test same parameters create same key. TC-CACHE-005")
    def test_cache_make_key_same_params(self):
        """Test same parameters create same key."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Create keys for same parameters"):
            key1 = cache._make_key("GET", "/test", None, None, None)
            key2 = cache._make_key("GET", "/test", None, None, None)

        with allure.step("Verify keys match"):
            assert key1 == key2

    @allure.title("TC-CACHE-006: ResponseCache - _make_key разные параметры")
    @allure.description("Test different parameters create different keys. TC-CACHE-006")
    def test_cache_make_key_different_params(self):
        """Test different parameters create different keys."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Create keys for different URLs"):
            key1 = cache._make_key("GET", "/test1")
            key2 = cache._make_key("GET", "/test2")

        with allure.step("Verify keys differ"):
            assert key1 != key2

    @allure.title("TC-CACHE-007: ResponseCache - _make_key нормализация headers")
    @allure.description("Test sensitive headers excluded from key. TC-CACHE-007")
    def test_cache_make_key_normalize_headers(self):
        """Test sensitive headers excluded from key."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Create keys with and without Authorization header"):
            key1 = cache._make_key("GET", "/test", headers={"Authorization": "Bearer token"})
            key2 = cache._make_key("GET", "/test", headers={})

        with allure.step("Verify keys match (Authorization excluded)"):
            assert key1 == key2

    @allure.title("TC-CACHE-008: ResponseCache - _make_key с params")
    @allure.description("Test params included in key. TC-CACHE-008")
    def test_cache_make_key_with_params(self):
        """Test params included in key."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Create keys with different params"):
            key1 = cache._make_key("GET", "/test", params={"page": 1})
            key2 = cache._make_key("GET", "/test", params={"page": 2})

        with allure.step("Verify keys differ"):
            assert key1 != key2

    @allure.title("TC-CACHE-009: ResponseCache - invalidate")
    @allure.description("Test cache invalidation. TC-CACHE-009")
    def test_cache_invalidate(self):
        """Test cache invalidation."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Save several values"):
            for i in range(3):
                result = ApiResult(
                    endpoint=f"/test{i}",
                    method="GET",
                    status_code=200,
                    response_time=0.5,
                    success=True,
                    redirect=False,
                    client_error=False,
                    server_error=False,
                    informational=False,
                )
                cache.set("GET", f"https://api.example.com/test{i}", result)

        with allure.step("Verify cache has entries"):
            assert cache.size() == 3

        with allure.step("Invalidate cache"):
            cache.invalidate()

        with allure.step("Verify cache is empty"):
            assert cache.size() == 0

    @allure.title("TC-CACHE-010: ResponseCache - cleanup_expired")
    @allure.description("Test expired entries cleanup. TC-CACHE-010")
    def test_cache_cleanup_expired(self):
        """Test expired entries cleanup."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Save value with short ttl"):
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
            cache.set("GET", "https://api.example.com/test", result, ttl=1)

        with allure.step("Wait for expiration"):
            time.sleep(2)

        with allure.step("Cleanup expired entries"):
            count = cache.cleanup_expired()

        with allure.step("Verify expired entry removed"):
            assert count == 1
            assert cache.size() == 0

    @allure.title("TC-CACHE-011: ResponseCache - size")
    @allure.description("Test cache size calculation. TC-CACHE-011")
    def test_cache_size(self):
        """Test cache size calculation."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Save 3 values"):
            for i in range(3):
                result = ApiResult(
                    endpoint=f"/test{i}",
                    method="GET",
                    status_code=200,
                    response_time=0.5,
                    success=True,
                    redirect=False,
                    client_error=False,
                    server_error=False,
                    informational=False,
                )
                cache.set("GET", f"https://api.example.com/test{i}", result)

        with allure.step("Verify size = 3"):
            assert cache.size() == 3

    @allure.title("TC-CACHE-012: ResponseCache - clear")
    @allure.description("Test cache clearing. TC-CACHE-012")
    def test_cache_clear(self):
        """Test cache clearing."""
        with allure.step("Create ResponseCache"):
            cache = ResponseCache()

        with allure.step("Save several values"):
            for i in range(3):
                result = ApiResult(
                    endpoint=f"/test{i}",
                    method="GET",
                    status_code=200,
                    response_time=0.5,
                    success=True,
                    redirect=False,
                    client_error=False,
                    server_error=False,
                    informational=False,
                )
                cache.set("GET", f"https://api.example.com/test{i}", result)

        with allure.step("Clear cache"):
            cache.clear()

        with allure.step("Verify cache is empty"):
            assert cache.size() == 0


@pytest.mark.unit
class TestCacheEntry:
    """Test CacheEntry class."""

    @allure.title("TC-CACHE-013: CacheEntry - is_expired False")
    @allure.description("Test is_expired returns False for valid entry. TC-CACHE-013")
    def test_cache_entry_is_expired_false(self):
        """Test is_expired returns False for valid entry."""
        with allure.step("Create CacheEntry with ttl=300"):
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
            entry = CacheEntry(value=result, ttl=300)

        with allure.step("Call is_expired immediately"):
            is_expired = entry.is_expired()

        with allure.step("Verify False returned"):
            assert is_expired is False

    @allure.title("TC-CACHE-014: CacheEntry - is_expired True")
    @allure.description("Test is_expired returns True for expired entry. TC-CACHE-014")
    def test_cache_entry_is_expired_true(self):
        """Test is_expired returns True for expired entry."""
        with allure.step("Create CacheEntry with ttl=1"):
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
            entry = CacheEntry(value=result, ttl=1)

        with allure.step("Wait for expiration"):
            time.sleep(2)

        with allure.step("Call is_expired"):
            is_expired = entry.is_expired()

        with allure.step("Verify True returned"):
            assert is_expired is True

    @allure.title("TC-CACHE-015: CacheEntry - timestamp")
    @allure.description("Test timestamp set on creation. TC-CACHE-015")
    def test_cache_entry_timestamp(self):
        """Test timestamp set on creation."""
        with allure.step("Record current time"):
            before = datetime.now()

        with allure.step("Create CacheEntry"):
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
            entry = CacheEntry(value=result)

        with allure.step("Verify timestamp is recent"):
            after = datetime.now()
            assert before <= entry.timestamp <= after

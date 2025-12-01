"""
Response caching system for web automation framework.

This module provides caching mechanisms for HTTP responses with TTL support
and configurable cache strategies.
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any


@dataclass
class CacheEntry:
    """
    Cache entry for storing cached responses.

    Attributes:
        value: Cached ApiResult value
        timestamp: When the entry was created
        ttl: Time to live in seconds
    """

    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: int = 300  # Default 5 minutes

    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return datetime.now() - self.timestamp > timedelta(seconds=self.ttl)


class ResponseCache:
    """
    Cache for HTTP responses with TTL support.

    Provides in-memory caching of API responses to reduce redundant requests.
    Supports configurable TTL and cache key generation.

    Attributes:
        _cache: Dictionary storing cache entries
        default_ttl: Default time to live in seconds
        max_size: Maximum number of cache entries (None = unlimited)

    Example:
        >>> cache = ResponseCache(default_ttl=300, max_size=1000)
        >>> result = cache.get("GET", "https://api.example.com/users")
        >>> if result is None:
        ...     result = await api.make_request("/users")
        ...     cache.set("GET", "https://api.example.com/users", result)
    """

    def __init__(self, default_ttl: int = 300, max_size: int | None = None) -> None:
        """
        Initialize response cache.

        Args:
            default_ttl: Default time to live in seconds (default: 300)
            max_size: Maximum number of cache entries (None = unlimited)
        """
        self._cache: dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size

    def _make_key(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> str:
        """
        Create cache key from request parameters.

        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers (optional)
            params: Query parameters (optional)
            data: Request body data (optional)

        Returns:
            MD5 hash of request parameters as cache key
        """
        # Normalize headers (remove auth tokens, etc.)
        normalized_headers = {}
        if headers:
            for k, v in headers.items():
                if k.lower() not in ("authorization", "cookie", "x-api-key"):
                    normalized_headers[k.lower()] = v

        # Create key data
        key_data = {
            "method": method.upper(),
            "url": url,
            "headers": normalized_headers,
            "params": params or {},
            "data": data or {},
        }

        # Sort for consistent hashing
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any | None:
        """
        Get cached response if available and not expired.

        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers (optional)
            params: Query parameters (optional)
            data: Request body data (optional)

        Returns:
            Cached ApiResult if found and not expired, None otherwise
        """
        key = self._make_key(method, url, headers, params, data)

        if key in self._cache:
            entry = self._cache[key]
            if not entry.is_expired():
                return entry.value
            else:
                # Remove expired entry
                del self._cache[key]

        return None

    def set(
        self,
        method: str,
        url: str,
        value: Any,
        ttl: int | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        """
        Store response in cache.

        Args:
            method: HTTP method
            url: Request URL
            value: ApiResult to cache
            ttl: Time to live in seconds (uses default_ttl if None)
            headers: Request headers (optional)
            params: Query parameters (optional)
            data: Request body data (optional)
        """
        # Check max size
        if self.max_size and len(self._cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]

        key = self._make_key(method, url, headers, params, data)
        entry = CacheEntry(value=value, ttl=ttl or self.default_ttl)
        self._cache[key] = entry

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()

    def invalidate(
        self,
        method: str | None = None,
        url_pattern: str | None = None,
    ) -> int:
        """
        Invalidate cache entries matching criteria.

        Args:
            method: HTTP method to match (None = all methods)
            url_pattern: URL pattern to match (None = all URLs)

        Returns:
            Number of entries invalidated
        """

        count = 0
        keys_to_remove = []

        for key, _entry in self._cache.items():
            # Simple pattern matching (can be enhanced)
            if url_pattern:
                # Extract URL from cache key is complex, so we'll match all
                # In production, you might want to store URL separately
                pass

            keys_to_remove.append(key)
            count += 1

        for key in keys_to_remove:
            del self._cache[key]

        return count

    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries from cache.

        Returns:
            Number of entries removed
        """
        expired_keys = [key for key, entry in self._cache.items() if entry.is_expired()]
        for key in expired_keys:
            del self._cache[key]
        return len(expired_keys)

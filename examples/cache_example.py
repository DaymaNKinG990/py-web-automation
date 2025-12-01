"""
Response caching usage example.

This example demonstrates how to use ResponseCache for caching
API responses to reduce redundant requests.
"""

import asyncio

from py_web_automation import ApiClient, Config
from py_web_automation.cache import ResponseCache


async def main():
    """Main function demonstrating cache usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Response Cache Examples ===\n")

        # Example 1: Basic Caching
        print("1. Basic response caching...")
        cache = ResponseCache(default_ttl=60)  # 60 seconds TTL

        async with ApiClient(base_url, config) as api:
            # First request - cache miss
            result1 = await api.make_request("/api/users", method="GET")
            cache.set("GET", f"{base_url}/api/users", result1)
            print(f"   First request - Status: {result1.status_code} (cache miss)")

            # Second request - cache hit
            cached_result = cache.get("GET", f"{base_url}/api/users")
            if cached_result:
                print(f"   Second request - Status: {cached_result.status_code} (cache hit)")
            else:
                print("   Second request - Cache miss (unexpected)")

        # Example 2: TTL Expiration
        print("\n2. TTL expiration...")
        cache = ResponseCache(default_ttl=2)  # 2 seconds TTL

        async with ApiClient(base_url, config) as api:
            result = await api.make_request("/api/data", method="GET")
            cache.set("GET", f"{base_url}/api/data", result, ttl=2)
            print("   Cached result with 2s TTL")

            # Check immediately - should be cached
            cached = cache.get("GET", f"{base_url}/api/data")
            print(f"   Immediately after: {'Cached' if cached else 'Expired'}")

            # Wait for expiration
            await asyncio.sleep(3)
            cached = cache.get("GET", f"{base_url}/api/data")
            print(f"   After 3 seconds: {'Cached' if cached else 'Expired'}")

        # Example 3: Cache Invalidation
        print("\n3. Cache invalidation...")
        cache = ResponseCache(default_ttl=300)

        async with ApiClient(base_url, config) as api:
            # Cache multiple endpoints
            for endpoint in ["/api/users", "/api/posts", "/api/comments"]:
                result = await api.make_request(endpoint, method="GET")
                cache.set("GET", f"{base_url}{endpoint}", result)
                print(f"   Cached: {endpoint}")

            # Invalidate specific endpoint
            cache.invalidate("GET", f"{base_url}/api/users")
            print("   Invalidated /api/users")

            # Check cache
            cached = cache.get("GET", f"{base_url}/api/users")
            print(f"   /api/users: {'Cached' if cached else 'Invalidated'}")

            cached = cache.get("GET", f"{base_url}/api/posts")
            print(f"   /api/posts: {'Cached' if cached else 'Invalidated'}")

            # Invalidate all
            cache.invalidate()
            print("   Invalidated all cache entries")

            cached = cache.get("GET", f"{base_url}/api/posts")
            print(f"   /api/posts after full invalidation: {'Cached' if cached else 'Invalidated'}")

        # Example 4: Cache with Different TTLs
        print("\n4. Cache with different TTLs...")
        cache = ResponseCache(default_ttl=60)

        async with ApiClient(base_url, config) as api:
            # Cache with default TTL
            result1 = await api.make_request("/api/static", method="GET")
            cache.set("GET", f"{base_url}/api/static", result1)
            print("   Cached /api/static with default TTL (60s)")

            # Cache with custom TTL
            result2 = await api.make_request("/api/dynamic", method="GET")
            cache.set("GET", f"{base_url}/api/dynamic", result2, ttl=5)
            print("   Cached /api/dynamic with custom TTL (5s)")

        # Example 5: Cache Size Limit
        print("\n5. Cache with size limit...")
        cache = ResponseCache(default_ttl=300, max_size=3)

        async with ApiClient(base_url, config) as api:
            # Add more entries than max_size
            for i in range(5):
                result = await api.make_request(f"/api/item-{i}", method="GET")
                cache.set("GET", f"{base_url}/api/item-{i}", result)
                print(f"   Cached item-{i}")

            # Check cache size
            print(f"   Cache entries (should be <= 3): {len(cache._cache)}")

        # Example 6: Cache Statistics
        print("\n6. Cache statistics...")
        cache = ResponseCache(default_ttl=300)

        async with ApiClient(base_url, config) as api:
            # Make requests and cache
            for endpoint in ["/api/a", "/api/b", "/api/c"]:
                result = await api.make_request(endpoint, method="GET")
                cache.set("GET", f"{base_url}{endpoint}", result)

            # Get cache statistics
            print(f"   Total cache entries: {len(cache._cache)}")
            print(f"   Default TTL: {cache.default_ttl}s")
            print(f"   Max size: {cache.max_size}")

        print("\n=== Cache Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

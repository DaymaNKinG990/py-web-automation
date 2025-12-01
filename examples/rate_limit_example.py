"""
Rate limiting usage example.

This example demonstrates how to use RateLimiter to prevent
exceeding API rate limits.
"""

import asyncio

from py_web_automation import ApiClient, Config
from py_web_automation.rate_limit import RateLimitConfig, RateLimiter


async def main():
    """Main function demonstrating rate limiter usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Rate Limiter Examples ===\n")

        # Example 1: Basic Rate Limiting
        print("1. Basic rate limiting...")
        limiter = RateLimiter(max_requests=5, window=10)  # 5 requests per 10 seconds

        async with ApiClient(base_url, config) as api:
            for i in range(7):
                await limiter.acquire()
                result = await api.make_request(f"/api/endpoint-{i}", method="GET")
                print(f"   Request {i + 1}: Status {result.status_code}")

        # Example 2: Rate Limiter with Burst
        print("\n2. Rate limiter with burst...")
        limiter = RateLimiter(max_requests=10, window=60, burst=5)

        async with ApiClient(base_url, config) as api:
            print(f"   Max requests: {limiter.config.max_requests}")
            print(f"   Window: {limiter.config.window}s")
            print(f"   Burst: {limiter.config.burst}")

            for i in range(12):
                await limiter.acquire()
                result = await api.make_request(f"/api/data-{i}", method="GET")
                print(f"   Request {i + 1}: Status {result.status_code}")

        # Example 3: Rate Limiter with Custom Config
        print("\n3. Rate limiter with custom config...")
        rate_config = RateLimitConfig(max_requests=3, window=5, burst=1)
        limiter = RateLimiter(
            max_requests=rate_config.max_requests,
            window=rate_config.window,
            burst=rate_config.burst,
        )

        async with ApiClient(base_url, config) as api:
            for i in range(5):
                await limiter.acquire()
                result = await api.make_request(f"/api/item-{i}", method="GET")
                print(f"   Request {i + 1}: Status {result.status_code}")

        # Example 4: Rate Limiter Statistics
        print("\n4. Rate limiter statistics...")
        limiter = RateLimiter(max_requests=5, window=10)

        async with ApiClient(base_url, config) as api:
            for i in range(3):
                await limiter.acquire()
                result = await api.make_request(f"/api/test-{i}", method="GET")
                print(f"   Request {i + 1}: Status {result.status_code}")

            print(f"   Active requests in window: {len(limiter.requests)}")
            print(f"   Max requests: {limiter.config.max_requests}")

        # Example 5: Rate Limiter with Different Windows
        print("\n5. Rate limiter with different time windows...")
        limiter_short = RateLimiter(max_requests=3, window=5)  # 3 per 5 seconds
        limiter_long = RateLimiter(max_requests=10, window=60)  # 10 per minute

        async with ApiClient(base_url, config) as api:
            print("   Short window (3 per 5s):")
            for i in range(4):
                await limiter_short.acquire()
                result = await api.make_request(f"/api/short-{i}", method="GET")
                print(f"     Request {i + 1}: Status {result.status_code}")

            print("   Long window (10 per 60s):")
            for i in range(5):
                await limiter_long.acquire()
                result = await api.make_request(f"/api/long-{i}", method="GET")
                print(f"     Request {i + 1}: Status {result.status_code}")

        print("\n=== Rate Limiter Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

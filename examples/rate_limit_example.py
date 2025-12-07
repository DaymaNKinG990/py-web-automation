"""
Rate limiting usage example.

This example demonstrates how to use RateLimitMiddleware to prevent
exceeding API rate limits.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.api_clients.http_client.middleware import MiddlewareChain
from py_web_automation.clients.api_clients.http_client.middleware.rate_limit_middleware import (
    RateLimitMiddleware,
)
from py_web_automation.clients.api_clients.http_client.rate_limit import (
    RateLimitConfig,
    RateLimiter,
)


async def main():
    """Main function demonstrating rate limiter usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Rate Limiter Examples ===\n")

        # Example 1: Basic Rate Limiting with Middleware
        print("1. Basic rate limiting with middleware...")
        rate_limiter = RateLimiter(max_requests=5, window=10)  # 5 requests per 10 seconds
        rate_limit_middleware = RateLimitMiddleware(rate_limiter)

        chain = MiddlewareChain()
        chain.add(rate_limit_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            for i in range(7):
                result = await api.make_request(f"/api/endpoint-{i}", method="GET")
                print(f"   Request {i + 1}: Status {result.status_code}")

        # Example 2: Rate Limiter with Burst
        print("\n2. Rate limiter with burst...")
        rate_limiter = RateLimiter(max_requests=10, window=60, burst=5)
        rate_limit_middleware = RateLimitMiddleware(rate_limiter)

        chain = MiddlewareChain()
        chain.add(rate_limit_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            print(f"   Max requests: {rate_limiter.config.max_requests}")
            print(f"   Window: {rate_limiter.config.window}s")
            print(f"   Burst: {rate_limiter.config.burst}")

            for i in range(12):
                result = await api.make_request(f"/api/data-{i}", method="GET")
                print(f"   Request {i + 1}: Status {result.status_code}")

        # Example 3: Rate Limiter with Custom Config
        print("\n3. Rate limiter with custom config...")
        rate_config = RateLimitConfig(max_requests=3, window=5, burst=1)
        rate_limiter = RateLimiter(
            max_requests=rate_config.max_requests,
            window=rate_config.window,
            burst=rate_config.burst,
        )
        rate_limit_middleware = RateLimitMiddleware(rate_limiter)

        chain = MiddlewareChain()
        chain.add(rate_limit_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            for i in range(5):
                result = await api.make_request(f"/api/item-{i}", method="GET")
                print(f"   Request {i + 1}: Status {result.status_code}")

        # Example 4: Rate Limiter Statistics
        print("\n4. Rate limiter statistics...")
        rate_limiter = RateLimiter(max_requests=5, window=10)
        rate_limit_middleware = RateLimitMiddleware(rate_limiter)

        chain = MiddlewareChain()
        chain.add(rate_limit_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            for i in range(3):
                result = await api.make_request(f"/api/test-{i}", method="GET")
                print(f"   Request {i + 1}: Status {result.status_code}")

            print(f"   Max requests: {rate_limiter.config.max_requests}")
            print(f"   Window: {rate_limiter.config.window}s")

        # Example 5: Rate Limiter with Different Windows
        print("\n5. Rate limiter with different time windows...")
        rate_limiter_short = RateLimiter(max_requests=3, window=5)  # 3 per 5 seconds
        rate_limit_middleware_short = RateLimitMiddleware(rate_limiter_short)

        chain_short = MiddlewareChain()
        chain_short.add(rate_limit_middleware_short)

        async with HttpClient(base_url, config, middleware=chain_short) as api:
            print("   Short window (3 per 5s):")
            for i in range(4):
                result = await api.make_request(f"/api/short-{i}", method="GET")
                print(f"     Request {i + 1}: Status {result.status_code}")

        print("\n=== Rate Limiter Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

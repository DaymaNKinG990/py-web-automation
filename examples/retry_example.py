"""
Retry mechanism usage example.

This example demonstrates how to use RetryMiddleware for automatic
retry of failed operations with exponential backoff.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.api_clients.http_client.middleware import MiddlewareChain
from py_web_automation.clients.api_clients.http_client.middleware.retry_middleware import (
    RetryMiddleware,
)
from py_web_automation.clients.api_clients.http_client.retry import (
    RetryConfig,
    RetryHandler,
)


async def main():
    """Main function demonstrating retry usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Retry Mechanism Examples ===\n")

        # Example 1: Basic Retry with Middleware
        print("1. Basic retry with middleware...")
        retry_config = RetryConfig(
            max_attempts=3,
            delay=1.0,
            backoff=2.0,
        )
        retry_handler = RetryHandler(retry_config)
        retry_middleware = RetryMiddleware(retry_handler)

        chain = MiddlewareChain()
        chain.add(retry_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/data", method="GET")
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

        # Example 2: Retry with Custom Configuration
        print("\n2. Retry with custom configuration...")
        retry_config = RetryConfig(
            max_attempts=5,
            delay=0.5,
            backoff=2.0,
        )
        retry_handler = RetryHandler(retry_config)
        retry_middleware = RetryMiddleware(retry_handler)

        chain = MiddlewareChain()
        chain.add(retry_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/unreliable", method="GET")
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

        # Example 3: Retry with Logging
        print("\n3. Retry with logging middleware...")
        from py_web_automation.clients.api_clients.http_client.middleware import (
            LoggingMiddleware,
        )

        retry_config = RetryConfig(max_attempts=3, delay=1.0, backoff=2.0)
        retry_handler = RetryHandler(retry_config)
        retry_middleware = RetryMiddleware(retry_handler)

        chain = MiddlewareChain()
        chain.add(LoggingMiddleware())
        chain.add(retry_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/data", method="GET")
            print(f"   Status: {result.status_code}")

        # Example 4: Exponential Backoff Demonstration
        print("\n4. Exponential backoff demonstration...")
        retry_config = RetryConfig(
            max_attempts=4,
            delay=0.5,
            backoff=2.0,
        )
        retry_handler = RetryHandler(retry_config)
        retry_middleware = RetryMiddleware(retry_handler)

        chain = MiddlewareChain()
        chain.add(retry_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            start_time = asyncio.get_event_loop().time()
            result = await api.make_request("/api/data", method="GET")
            elapsed = asyncio.get_event_loop().time() - start_time
            print(f"   Request completed in {elapsed:.2f}s")
            print(f"   Status: {result.status_code}")

        # Example 5: Retry Configuration
        print("\n5. Using RetryConfig...")
        retry_config = RetryConfig(
            max_attempts=5,
            delay=1.0,
            backoff=2.0,
        )

        retry_handler = RetryHandler(retry_config)
        retry_middleware = RetryMiddleware(retry_handler)

        chain = MiddlewareChain()
        chain.add(retry_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/data", method="GET")
            print(f"   Status: {result.status_code}")

        # Example 6: Retry for Different Operations
        print("\n6. Retry for different operations...")
        retry_config = RetryConfig(max_attempts=3, delay=1.0, backoff=2.0)
        retry_handler = RetryHandler(retry_config)
        retry_middleware = RetryMiddleware(retry_handler)

        chain = MiddlewareChain()
        chain.add(retry_middleware)

        async with HttpClient(base_url, config, middleware=chain) as api:
            # Create user with retry
            result = await api.make_request(
                "/api/users", method="POST", data={"name": "John", "email": "john@example.com"}
            )
            print(f"   Create user - Status: {result.status_code}")

            # Update user with retry
            result = await api.make_request(
                "/api/users/1", method="PUT", data={"name": "Jane"}
            )
            print(f"   Update user - Status: {result.status_code}")

        print("\n=== Retry Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

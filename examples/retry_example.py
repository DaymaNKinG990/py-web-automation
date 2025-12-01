"""
Retry mechanism usage example.

This example demonstrates how to use retry decorators for automatic
retry of failed operations with exponential backoff.
"""

import asyncio

from py_web_automation import ApiClient, Config
from py_web_automation.exceptions import ConnectionError, TimeoutError
from py_web_automation.retry import RetryConfig, retry_on_connection_error, retry_on_failure


async def main():
    """Main function demonstrating retry usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Retry Mechanism Examples ===\n")

        # Example 1: Basic Retry with retry_on_connection_error
        print("1. Basic retry on connection errors...")

        @retry_on_connection_error(max_attempts=3, delay=1.0, backoff=2.0)
        async def fetch_with_retry():
            async with ApiClient(base_url, config) as api:
                return await api.make_request("/api/data", method="GET")

        try:
            result = await fetch_with_retry()
            print(f"   Status: {result.status_code}")
        except Exception as e:
            print(f"   Failed after retries: {e}")

        # Example 2: Retry with Custom Exceptions
        print("\n2. Retry with custom exceptions...")

        @retry_on_failure(
            max_attempts=3,
            delay=0.5,
            backoff=2.0,
            exceptions=(ConnectionError, TimeoutError),
        )
        async def fetch_with_custom_retry():
            async with ApiClient(base_url, config) as api:
                return await api.make_request("/api/unreliable", method="GET")

        try:
            result = await fetch_with_custom_retry()
            print(f"   Status: {result.status_code}")
        except Exception as e:
            print(f"   Failed after retries: {e}")

        # Example 3: Retry with Callback
        print("\n3. Retry with callback...")

        retry_count = 0

        def on_retry(attempt: int, exception: Exception) -> None:
            nonlocal retry_count
            retry_count += 1
            print(f"   Retry attempt {attempt}: {type(exception).__name__}")

        @retry_on_failure(
            max_attempts=3,
            delay=1.0,
            backoff=2.0,
            exceptions=(ConnectionError,),
            on_retry=on_retry,
        )
        async def fetch_with_callback():
            async with ApiClient(base_url, config) as api:
                return await api.make_request("/api/data", method="GET")

        try:
            result = await fetch_with_callback()
            print(f"   Total retries: {retry_count}")
            print(f"   Status: {result.status_code}")
        except Exception as e:
            print(f"   Failed after {retry_count} retries: {e}")

        # Example 4: Exponential Backoff
        print("\n4. Exponential backoff demonstration...")

        @retry_on_connection_error(max_attempts=4, delay=0.5, backoff=2.0)
        async def fetch_with_backoff():
            start_time = asyncio.get_event_loop().time()
            async with ApiClient(base_url, config) as api:
                result = await api.make_request("/api/data", method="GET")
                elapsed = asyncio.get_event_loop().time() - start_time
                print(f"   Request completed in {elapsed:.2f}s")
                return result

        try:
            result = await fetch_with_backoff()
            print(f"   Status: {result.status_code}")
        except Exception as e:
            print(f"   Failed: {e}")

        # Example 5: Retry Configuration
        print("\n5. Using RetryConfig...")
        retry_config = RetryConfig(
            max_attempts=5,
            delay=1.0,
            backoff=2.0,
            exceptions=(ConnectionError, TimeoutError),
        )

        @retry_on_failure(
            max_attempts=retry_config.max_attempts,
            delay=retry_config.delay,
            backoff=retry_config.backoff,
            exceptions=retry_config.exceptions,
        )
        async def fetch_with_config():
            async with ApiClient(base_url, config) as api:
                return await api.make_request("/api/data", method="GET")

        try:
            result = await fetch_with_config()
            print(f"   Status: {result.status_code}")
        except Exception as e:
            print(f"   Failed: {e}")

        # Example 6: Retry for Different Operations
        print("\n6. Retry for different operations...")

        @retry_on_connection_error(max_attempts=3, delay=1.0)
        async def create_user(user_data: dict):
            async with ApiClient(base_url, config) as api:
                return await api.make_request("/api/users", method="POST", data=user_data)

        @retry_on_connection_error(max_attempts=3, delay=1.0)
        async def update_user(user_id: str, user_data: dict):
            async with ApiClient(base_url, config) as api:
                return await api.make_request(f"/api/users/{user_id}", method="PUT", data=user_data)

        try:
            result = await create_user({"name": "John", "email": "john@example.com"})
            print(f"   Create user - Status: {result.status_code}")

            result = await update_user("1", {"name": "Jane"})
            print(f"   Update user - Status: {result.status_code}")
        except Exception as e:
            print(f"   Operation failed: {e}")

        print("\n=== Retry Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

"""
Example: Using only HttpClient for HTTP REST API testing.

This example demonstrates how to use HttpClient class independently
for testing HTTP REST API functionality.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient


async def test_api_only():
    """Test using only API functionality."""

    # Create config
    config = Config(
        timeout=30,
        retry_count=3,
        retry_delay=1.0,
        log_level="INFO",
    )

    # Initialize HTTP client
    api = HttpClient("https://api.example.com", config)

    try:
        print("=== HttpClient Testing ===")

        # 1. Test HTTP API endpoints
        print("\n1. Testing HTTP API endpoints...")

        # Test GET endpoint
        get_result = await api.make_request("/api/status", method="GET")
        print(
            f"   GET /api/status: {'[OK]' if get_result.success else '[ERROR]'} "
            f"({get_result.status_code}) - {get_result.response_time:.3f}s"
        )

        # Test POST endpoint
        post_result = await api.make_request(
            "/api/data",
            method="POST",
            data={"key": "value"},
            headers={"Content-Type": "application/json"},
        )
        print(
            f"   POST /api/data: {'[OK]' if post_result.success else '[ERROR]'} "
            f"({post_result.status_code}) - {post_result.response_time:.3f}s"
        )

        # Test PUT endpoint
        put_result = await api.make_request(
            "/api/data/1",
            method="PUT",
            data={"key": "updated_value"},
        )
        print(
            f"   PUT /api/data/1: {'[OK]' if put_result.success else '[ERROR]'} "
            f"({put_result.status_code}) - {put_result.response_time:.3f}s"
        )

        # Test DELETE endpoint
        delete_result = await api.make_request("/api/data/1", method="DELETE")
        print(
            f"   DELETE /api/data/1: {'[OK]' if delete_result.success else '[ERROR]'} "
            f"({delete_result.status_code}) - {delete_result.response_time:.3f}s"
        )

        print("\n=== API Testing Complete ===")

    except Exception as e:
        print(f"[ERROR] Error during API testing: {e}")

    finally:
        # Clean up
        await api.close()


async def test_api_with_context_manager():
    """Test HttpClient using context manager."""

    config = Config(
        timeout=30,
        retry_count=3,
        retry_delay=1.0,
        log_level="INFO",
    )

    print("\n=== Context Manager Testing ===")

    async with HttpClient("https://api.example.com", config) as api:
        # Quick API test
        result = await api.make_request("/api/health", method="GET")
        print(
            f"Health check: {'[OK]' if result.success else '[ERROR]'} "
            f"({result.status_code}) - {result.response_time:.3f}s"
        )

    print("Context manager cleanup completed")


async def main():
    """Main function to run all examples."""
    print("HttpClient Examples")
    print("===================")

    # Run API-only testing
    await test_api_only()

    # Run context manager testing
    await test_api_with_context_manager()

    print("\nAll examples completed!")


if __name__ == "__main__":
    asyncio.run(main())

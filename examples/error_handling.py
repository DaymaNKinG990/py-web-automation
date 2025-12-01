"""
Error handling examples for Web Automation Framework.

Shows proper error handling for API requests, UI interactions, and configuration.
"""

import asyncio

from py_web_automation import ApiClient, Config, UiClient
from py_web_automation.exceptions import (
    ConnectionError,
    NotFoundError,
    TimeoutError,
    WebAutomationError,
)


async def test_invalid_configuration():
    """Test with invalid configuration."""
    print("=== Testing Invalid Configuration ===")

    try:
        # Invalid timeout (too high)
        Config(timeout=500)  # Should fail validation
        print("❌ Configuration validation failed (expected)")
    except ValueError as e:
        print(f"✅ Expected error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def test_connection_errors():
    """Test connection error handling."""
    print("\n=== Testing Connection Errors ===")

    config = Config(timeout=5)  # Short timeout for testing

    try:
        async with ApiClient("https://invalid-url-that-does-not-exist-12345.com", config) as api:
            result = await api.make_request("/api/test", method="GET")
            print(f"Connection test: {'✅ OK' if result.success else '❌ FAILED'}")
            if result.error_message:
                print(f"Error message: {result.error_message}")

    except ConnectionError as e:
        print(f"✅ Connection error caught: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def test_timeout_handling():
    """Test timeout error handling."""
    print("\n=== Testing Timeout Handling ===")

    config = Config(timeout=2)  # Very short timeout

    try:
        async with ApiClient("https://httpbin.org", config) as api:
            # This might timeout depending on network
            result = await api.make_request("/delay/5", method="GET")
            if result.error_message and "timeout" in result.error_message.lower():
                print("✅ Timeout correctly detected")
            else:
                print(f"⚠️ Request completed: {result.status_code}")

    except TimeoutError as e:
        print(f"✅ Timeout error caught: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def test_ui_errors():
    """Test UI error handling."""
    print("\n=== Testing UI Errors ===")

    config = Config(timeout=30, browser_headless=True)

    try:
        async with UiClient("https://example.com", config) as ui:
            await ui.setup_browser()
            await ui.page.goto("https://example.com", wait_until="networkidle")

            # Try to interact with non-existent element
            try:
                await ui.click_element("#non-existent-element-12345")
                print("❌ Should have raised NotFoundError")
            except NotFoundError as e:
                print(f"✅ NotFoundError correctly raised: {e}")
            except Exception as e:
                print(f"⚠️ Different error: {e}")

            # Try to wait for non-existent element (timeout)
            try:
                await ui.wait_for_element("#non-existent-element-12345", timeout=2000)
                print("❌ Should have timed out")
            except (TimeoutError, NotFoundError) as e:
                print(f"✅ Timeout/NotFound error correctly raised: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def test_api_error_responses():
    """Test API error response handling."""
    print("\n=== Testing API Error Responses ===")

    config = Config(timeout=30)

    try:
        async with ApiClient("https://httpbin.org", config) as api:
            # Test 404 error
            result = await api.make_request("/status/404", method="GET")
            print(f"404 test: {'✅ OK' if not result.success else '❌ FAILED'}")
            print(f"  Status: {result.status_code}, Client Error: {result.client_error}")

            # Test 500 error
            result = await api.make_request("/status/500", method="GET")
            print(f"500 test: {'✅ OK' if not result.success else '❌ FAILED'}")
            print(f"  Status: {result.status_code}, Server Error: {result.server_error}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def test_environment_variables():
    """Test environment variable loading."""
    print("\n=== Testing Environment Variables ===")

    try:
        # Try to create config from environment
        config = Config.from_env()
        print("✅ Configuration loaded from environment")
        print(f"  Timeout: {config.timeout}")
        print(f"  Retry count: {config.retry_count}")
        print(f"  Log level: {config.log_level}")

    except Exception as e:
        print(f"⚠️ Environment variables not set: {e}")
        print("  (This is OK if environment variables are not configured)")


async def test_comprehensive_error_handling():
    """Test comprehensive error handling."""
    print("\n=== Comprehensive Error Handling ===")

    config = Config(timeout=30)

    endpoints = [
        ("/api/health", "GET"),  # Should succeed
        ("/api/not-found", "GET"),  # Should return 404
        ("/api/error", "GET"),  # Might return 500
    ]

    async with ApiClient("https://api.example.com", config) as api:
        for endpoint, method in endpoints:
            try:
                result = await api.make_request(endpoint, method=method)

                if result.success:
                    print(f"✅ {method} {endpoint}: Success ({result.status_code})")
                elif result.client_error:
                    print(f"⚠️ {method} {endpoint}: Client Error ({result.status_code})")
                elif result.server_error:
                    print(f"⚠️ {method} {endpoint}: Server Error ({result.status_code})")
                else:
                    print(f"❓ {method} {endpoint}: Unknown status ({result.status_code})")

            except ConnectionError as e:
                print(f"🔌 {method} {endpoint}: Connection error - {e}")
            except TimeoutError as e:
                print(f"⏱️ {method} {endpoint}: Timeout - {e}")
            except WebAutomationError as e:
                print(f"⚠️ {method} {endpoint}: Framework error - {e}")
            except Exception as e:
                print(f"💥 {method} {endpoint}: Unexpected error - {e}")


async def main():
    """Run all error handling tests."""
    print("Web Automation Framework - Error Handling Examples")
    print("=" * 60)

    await test_invalid_configuration()
    await test_connection_errors()
    await test_timeout_handling()
    await test_ui_errors()
    await test_api_error_responses()
    test_environment_variables()
    await test_comprehensive_error_handling()

    print("\n" + "=" * 60)
    print("✅ Error handling tests completed!")


if __name__ == "__main__":
    asyncio.run(main())

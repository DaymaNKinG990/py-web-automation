"""
Advanced usage example of Web Automation Framework.

This example demonstrates advanced usage patterns with HttpClient and AsyncUiClient,
including error handling, retry logic, and comprehensive testing scenarios.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.ui_clients import AsyncUiClient
from py_web_automation.exceptions import (
    NotFoundError,
    TimeoutError,
    WebAutomationError,
)


async def main():
    """Main function demonstrating advanced usage."""

    # Create configuration with custom settings
    config = Config(
        timeout=30,
        retry_count=3,
        retry_delay=1.0,
        log_level="DEBUG",
        browser_headless=True,
        browser_timeout=30000,
    )

    base_url = "https://api.example.com"
    web_url = "https://example.com"

    try:
        # Example 1: Advanced API Testing
        print("\n=== Example 1: Advanced API Testing ===")
        async with HttpClient(base_url, config) as api:
            # Test multiple API endpoints
            endpoints = [
                ("/api/status", "GET"),
                ("/api/users", "GET"),
                ("/api/data", "POST", {"key": "value"}),
            ]

            for endpoint_info in endpoints:
                if len(endpoint_info) == 2:
                    endpoint, method = endpoint_info
                    data = None
                else:
                    endpoint, method, data = endpoint_info

                print(f"Testing {method} {endpoint}...")
                result = await api.make_request(endpoint, method=method, data=data)

                print(f"  Status: {'PASSED' if result.success else 'FAILED'}")
                print(f"  Code: {result.status_code}")
                print(f"  Time: {result.response_time:.3f}s")

                if not result.success and result.error:
                    print(f"  Error: {result.error}")

        # Example 2: Advanced UI Testing
        print("\n=== Example 2: Advanced UI Testing ===")
        async with AsyncUiClient(web_url, config) as ui:
            # Setup browser and navigate
            await ui.setup_browser()
            if ui.page:
                await ui.page.goto(web_url, wait_until="networkidle")

            # Comprehensive UI testing
            print("Running comprehensive UI tests...")

            # Form interactions
            print("Testing form interactions...")
            await ui.fill_input("input[name='name']", "John Doe")
            await ui.fill_input("input[name='email']", "john@example.com")
            await ui.select_option("select[name='country']", "US")
            await ui.check_checkbox("input[name='terms']")

            # Mouse interactions
            print("Testing mouse interactions...")
            await ui.hover_element("a")
            await ui.double_click_element("button")
            await ui.right_click_element("div")

            # Keyboard interactions
            print("Testing keyboard interactions...")
            await ui.type_text("Hello, World!")
            await ui.press_key("Enter")

            # Element information
            print("Getting element information...")
            element_text = await ui.get_element_text(".status-message")
            element_class = await ui.get_element_attribute_value("button", "class")

            print(f"  Element text: {element_text or 'N/A'}")
            print(f"  Element class: {element_class or 'N/A'}")

            # Page information
            print("Getting page information...")
            page_title = await ui.get_page_title()
            page_url = await ui.get_page_url()

            print(f"  Page title: {page_title}")
            print(f"  Page URL: {page_url}")

            # JavaScript execution
            print("Testing JavaScript execution...")
            script_result = await ui.execute_script("return document.title;")
            print(f"  JavaScript result: {script_result}")

            # Screenshots
            print("Taking screenshots...")
            await ui.take_screenshot("advanced_ui_screenshot.png")

            print("Advanced UI interactions completed")

        # Example 3: Error Handling and Recovery
        print("\n=== Example 3: Error Handling and Recovery ===")

        # Test with invalid URL
        print("Testing error handling with invalid URL...")
        async with HttpClient("https://invalid-url-that-does-not-exist.com", config) as api:
            result = await api.make_request("/api/test", method="GET")
            print(f"  Invalid URL test: {'PASSED' if result.success else 'FAILED'}")
            if result.error:
                print(f"  Error message: {result.error}")

        # Test UI with timeout
        print("Testing UI timeout handling...")
        async with AsyncUiClient(web_url, config) as ui:
            await ui.setup_browser()
            if ui.page:
                await ui.page.goto(web_url, wait_until="networkidle")

            try:
                # This will timeout since element doesn't exist
                await ui.wait_for_element("#non-existent-element", timeout=2000)
                print("  Timeout test: FAILED (should have timed out)")
            except (TimeoutError, NotFoundError) as e:
                print(f"  Timeout test: PASSED (expected timeout: {e})")

        # Example 4: Performance Testing
        print("\n=== Example 4: Performance Testing ===")

        # API performance test
        print("Testing API performance...")
        async with HttpClient(base_url, config) as api:
            start_time = asyncio.get_event_loop().time()

            # Make multiple concurrent requests
            tasks = []
            for i in range(5):
                task = api.make_request(f"/api/test-{i}", method="GET")
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

            end_time = asyncio.get_event_loop().time()
            total_time = end_time - start_time

            print(f"  Made 5 concurrent requests in {total_time:.3f}s")
            print(f"  Average time per request: {total_time / 5:.3f}s")

            successful_requests = sum(
                1 for r in results if not isinstance(r, Exception) and hasattr(r, "success") and r.success
            )
            print(f"  Successful requests: {successful_requests}/5")

        # UI performance test
        print("Testing UI performance...")
        async with AsyncUiClient(web_url, config) as ui:
            await ui.setup_browser()

            start_time = asyncio.get_event_loop().time()
            if ui.page:
                await ui.page.goto(web_url, wait_until="networkidle")
            end_time = asyncio.get_event_loop().time()

            load_time = end_time - start_time
            print(f"  Page load time: {load_time:.3f}s")

            # Test screenshot performance
            start_time = asyncio.get_event_loop().time()
            await ui.take_screenshot("performance_test.png")
            end_time = asyncio.get_event_loop().time()

            screenshot_time = end_time - start_time
            print(f"  Screenshot time: {screenshot_time:.3f}s")

        print("\nAdvanced usage example completed!")

    except WebAutomationError as e:
        print(f"Framework error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

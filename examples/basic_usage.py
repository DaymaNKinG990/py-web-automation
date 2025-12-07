"""
Basic usage example of Web Automation Framework.

This example demonstrates the basic usage of the framework with
HttpClient and AsyncUiClient classes.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.ui_clients import AsyncUiClient


async def main():
    """Main function demonstrating basic usage."""

    # Create configuration
    config = Config(
        timeout=30,
        retry_count=3,
        retry_delay=1.0,
        log_level="INFO",
        browser_headless=True,
    )

    base_url = "https://api.example.com"
    web_url = "https://example.com"

    try:
        # Example 1: API Testing
        print("\n=== Example 1: API Testing ===")
        async with HttpClient(base_url, config) as api:
            # Test API endpoints
            result = await api.make_request("/api/status", method="GET")
            print(f"API Test: {'PASSED' if result.success else 'FAILED'}")
            print(f"Status Code: {result.status_code}")
            print(f"Response Time: {result.response_time:.3f}s")
            if result.body:
                print(f"Response: {result.json()}")

        # Example 2: UI Testing
        print("\n=== Example 2: UI Testing ===")
        async with AsyncUiClient(web_url, config) as ui:
            # Setup browser and navigate
            await ui.setup_browser()
            if ui.page:
                await ui.page.goto(web_url, wait_until="networkidle")

            # Basic UI interactions
            print("Testing UI interactions...")
            await ui.fill_input("#username", "test_user")
            await ui.click_element("#submit-button")
            await ui.take_screenshot("basic_ui_test.png")

            # Get page information
            title = await ui.get_page_title()
            url = await ui.get_page_url()
            print(f"Page title: {title}")
            print(f"Page URL: {url}")

        print("\nBasic usage example completed!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

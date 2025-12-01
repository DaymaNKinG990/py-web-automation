"""
Page Object Model usage example.

This example demonstrates how to use Page Objects and Components
for organizing UI tests with the Page Object Model pattern.
"""

import asyncio

from py_web_automation import Config, UiClient
from py_web_automation.page_objects import BasePage, Component, PageFactory


class LoginPage(BasePage):
    """Page object for login page."""

    def __init__(self, ui_client: UiClient):
        super().__init__(ui_client, "https://example.com/login")

    async def is_loaded(self) -> bool:
        """Check if login page is loaded."""
        return await self.is_element_visible("#login-form")

    async def login(self, username: str, password: str) -> None:
        """Perform login action."""
        await self.fill_input("#username", username)
        await self.fill_input("#password", password)
        await self.click_element("#login-button")
        await self.wait_for_navigation()


class DashboardPage(BasePage):
    """Page object for dashboard page."""

    def __init__(self, ui_client: UiClient):
        super().__init__(ui_client, "https://example.com/dashboard")

    async def is_loaded(self) -> bool:
        """Check if dashboard page is loaded."""
        return await self.is_element_visible("#dashboard-content")

    async def get_welcome_message(self) -> str:
        """Get welcome message text."""
        return await self.get_element_text("#welcome-message")


class NavigationComponent(Component):
    """Reusable navigation component."""

    def __init__(self, ui_client: UiClient):
        super().__init__(ui_client, "nav.main-nav")

    async def click_home(self) -> None:
        """Click home link."""
        await self.click_element("a.home")

    async def click_dashboard(self) -> None:
        """Click dashboard link."""
        await self.click_element("a.dashboard")

    async def click_profile(self) -> None:
        """Click profile link."""
        await self.click_element("a.profile")


async def main():
    """Main function demonstrating page objects usage."""

    config = Config(timeout=30, browser_headless=True, log_level="INFO")

    try:
        print("=== Page Objects Examples ===\n")

        async with UiClient("https://example.com", config) as ui:
            await ui.setup_browser()

            # Example 1: Using Page Objects
            print("1. Using page objects...")
            login_page = LoginPage(ui)
            await login_page.navigate()
            print("   Navigated to login page")

            is_loaded = await login_page.is_loaded()
            print(f"   Page loaded: {is_loaded}")

            # Example 2: Page Actions
            print("\n2. Performing page actions...")
            await login_page.login("testuser", "testpass")
            print("   Login action completed")

            # Example 3: Using Components
            print("\n3. Using reusable components...")
            nav = NavigationComponent(ui)
            await nav.click_dashboard()
            print("   Clicked dashboard via component")

            # Example 4: Page Factory
            print("\n4. Using page factory...")
            factory = PageFactory(ui)

            # Register pages
            factory.register("login", LoginPage)
            factory.register("dashboard", DashboardPage)

            # Get page instance
            dashboard = factory.get_page("dashboard")
            await dashboard.navigate()
            print("   Navigated to dashboard via factory")

            is_loaded = await dashboard.is_loaded()
            print(f"   Dashboard loaded: {is_loaded}")

            # Example 5: Component Reuse
            print("\n5. Reusing components across pages...")
            nav = NavigationComponent(ui)
            await nav.click_home()
            print("   Clicked home via component")

            # Example 6: Page State Verification
            print("\n6. Verifying page state...")
            dashboard = DashboardPage(ui)
            await dashboard.navigate()

            title = await dashboard.get_page_title()
            url = await dashboard.get_page_url()
            print(f"   Page title: {title}")
            print(f"   Page URL: {url}")

            welcome = await dashboard.get_welcome_message()
            print(f"   Welcome message: {welcome}")

            # Example 7: Screenshots with Page Objects
            print("\n7. Taking screenshots...")
            await dashboard.take_screenshot("dashboard_page.png")
            print("   Screenshot saved")

        print("\n=== Page Objects Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

"""
Browser-based UI testing client using Playwright.

This module provides UiClient for browser-based UI testing of web applications,
including element interaction, form handling, and visual testing capabilities.
"""

# Python imports
from typing import TYPE_CHECKING, Any, Self

from playwright.async_api import Browser, Page, Playwright, async_playwright

from ..config import Config

# Local imports
from .base_client import BaseClient

if TYPE_CHECKING:
    pass


class UiClient(BaseClient):
    """
    Browser-based UI testing client.

    Implements browser automation using Playwright for comprehensive UI testing.
    Follows the Single Responsibility Principle by focusing solely on UI testing.

    Provides comprehensive UI testing capabilities:
    - Browser automation and page navigation with automatic setup
    - Element interaction (click, fill, wait, hover, double-click, right-click)
    - Form handling (checkboxes, selects, file uploads)
    - Screenshots and visual testing
    - JavaScript execution in page context
    - Page state inspection (title, URL, element text/attributes)
    - Keyboard input simulation

    Attributes:
        _playwright: Playwright instance (private)
        browser: Browser instance (public, set after setup_browser)
        page: Page instance (public, set after setup_browser)

    Example:
        >>> from py_web_automation import Config, UiClient
        >>> config = Config(timeout=30)
        >>> async with UiClient("https://example.com", config) as ui:
        ...     await ui.setup_browser()
        ...     await ui.click_element("#button")
        ...     text = await ui.get_element_text("#result")
    """

    def __init__(self, url: str, config: Config | None = None) -> None:
        """
        Initialize UI client.

        Creates a UI client instance but does not start the browser.
        Call setup_browser() to initialize Playwright and navigate to the URL.

        Args:
            url: Application URL to test
            config: Configuration object with timeout and retry settings

        Raises:
            ValueError: If config is None (inherited from BaseClient)

        Example:
            >>> config = Config(timeout=30)
            >>> ui = UiClient("https://example.com", config)
        """
        super().__init__(url, config)
        self._playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def close(self) -> None:
        """
        Close browser and stop Playwright.

        Performs cleanup of all browser resources:
        - Closes browser instance
        - Stops Playwright process
        - Clears page reference

        This method is automatically called when exiting an async context manager.

        Example:
            >>> async with UiClient(url, config) as ui:
            ...     await ui.setup_browser()
            ...     # Use UI client
            ...     pass
            # Browser is automatically closed here
        """
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
        self.page = None

    async def setup_browser(self) -> Self:
        """
        Setup Playwright browser for UI testing.

        Initializes Playwright, launches a Chromium browser in headless mode,
        creates a new page, sets a standard user agent,
        and navigates to the application URL.

        Returns:
            Self for method chaining

        Raises:
            ValueError: If URL is not set or is empty
            RuntimeError: If navigation fails

        Example:
            >>> async with UiClient(url, config) as ui:
            ...     await ui.setup_browser()
            ...     # Browser is ready, page is loaded
            ...     await ui.click_element("#button")
        """
        if self.browser:
            self.logger.debug("Browser already setup")
        else:
            # Verify URL is set
            if not self.url or not isinstance(self.url, str) or not self.url.strip():
                error_msg = "URL is not set or is empty. Cannot setup browser without a valid URL."
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(headless=True)
            self.logger.debug("Browser launched")
            self.page = await self.browser.new_page()
            self.logger.debug("New page created")
            # Set standard user agent
            await self.page.set_extra_http_headers(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
            )
            self.logger.debug("User agent set")

            # Navigate to the application URL
            try:
                self.logger.debug(f"Navigating to {self.url}")
                await self.page.goto(self.url, wait_until="networkidle")
                self.logger.info(f"Successfully navigated to {self.url}")
            except Exception as e:
                error_msg = f"Failed to navigate to {self.url}: {e}"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg) from e
        return self

    async def click_element(self, selector: str) -> None:
        """
        Click element on the page.

        Args:
            selector: CSS selector for element

        Raises:
            RuntimeError: If browser is not initialized
            NotFoundError: If element is not found
            OperationError: If click operation fails

        Example:
            >>> await ui.click_element("#submit-button")
        """
        if not self.page:
            error_msg = "Browser not initialized. Call setup_browser() first."
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        try:
            await self.page.click(selector)
            self.logger.debug(f"Clicked element: {selector}")
        except Exception as e:
            error_msg = f"Failed to click element {selector}: {e}"
            self.logger.error(error_msg)
            from ..exceptions import NotFoundError, OperationError

            if "not found" in str(e).lower() or "timeout" in str(e).lower():
                raise NotFoundError(error_msg, str(e)) from e
            raise OperationError(error_msg, str(e)) from e

    async def fill_input(self, selector: str, text: str) -> None:
        """
        Fill input field on the page.

        Args:
            selector: CSS selector for input
            text: Text to fill

        Raises:
            RuntimeError: If browser is not initialized
            NotFoundError: If element is not found
            OperationError: If fill operation fails

        Example:
            >>> await ui.fill_input("#username", "john_doe")
        """
        if not self.page:
            error_msg = "Browser not initialized. Call setup_browser() first."
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        try:
            await self.page.fill(selector, text)
            self.logger.debug(f"Filled input {selector} with: {text}")
        except Exception as e:
            error_msg = f"Failed to fill input {selector}: {e}"
            self.logger.error(error_msg)
            from ..exceptions import NotFoundError, OperationError

            if "not found" in str(e).lower() or "timeout" in str(e).lower():
                raise NotFoundError(error_msg, str(e)) from e
            raise OperationError(error_msg, str(e)) from e

    async def wait_for_element(self, selector: str, timeout: int = 5000) -> None:
        """
        Wait for element to appear on the page.

        Args:
            selector: CSS selector for element
            timeout: Timeout in milliseconds

        Raises:
            RuntimeError: If browser is not initialized
            TimeoutError: If element does not appear within timeout
            NotFoundError: If element is not found

        Example:
            >>> await ui.wait_for_element("#loading-spinner", timeout=10000)
        """
        if not self.page:
            error_msg = "Browser not initialized. Call setup_browser() first."
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            self.logger.debug(f"Element appeared: {selector}")
        except Exception as e:
            error_msg = f"Element {selector} did not appear within {timeout}ms: {e}"
            self.logger.error(error_msg)
            from ..exceptions import NotFoundError, TimeoutError

            if "timeout" in str(e).lower():
                raise TimeoutError(error_msg, str(e)) from e
            raise NotFoundError(error_msg, str(e)) from e

    async def take_screenshot(self, path: str) -> None:
        """
        Take screenshot of the current page.

        Args:
            path: Path to save screenshot

        Raises:
            RuntimeError: If browser is not initialized
            OperationError: If screenshot fails

        Example:
            >>> await ui.take_screenshot("screenshot.png")
        """
        if not self.page:
            error_msg = "Browser not initialized. Call setup_browser() first."
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        try:
            await self.page.screenshot(path=path)
            self.logger.debug(f"Screenshot saved: {path}")
        except Exception as e:
            error_msg = f"Screenshot failed: {e}"
            self.logger.error(error_msg)
            from ..exceptions import OperationError

            raise OperationError(error_msg, str(e)) from e

    async def get_element_text(self, selector: str) -> str | None:
        """
        Get text content of an element.

        Args:
            selector: CSS selector for element

        Returns:
            Element text content or None if element not found

        Raises:
            RuntimeError: If browser is not initialized
            OperationError: If operation fails

        Example:
            >>> text = await ui.get_element_text("#result")
            >>> if text:
            ...     print(f"Result: {text}")
        """
        if not self.page:
            error_msg = "Browser not initialized. Call setup_browser() first."
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        try:
            element = await self.page.query_selector(selector)
            if element:
                text = await element.text_content()
                self.logger.debug(f"Element text ({selector}): {text}")
                return str(text) if text is not None else None
            return None
        except Exception as e:
            error_msg = f"Failed to get element text {selector}: {e}"
            self.logger.error(error_msg)
            from ..exceptions import OperationError

            raise OperationError(error_msg, str(e)) from e

    async def get_element_attribute_value(self, selector: str, attribute: str) -> str | None:
        """
        Get attribute value of an element.

        Args:
            selector: CSS selector for element
            attribute: Attribute name

        Returns:
            Attribute value or None if element or attribute not found

        Raises:
            RuntimeError: If browser is not initialized
            OperationError: If operation fails

        Example:
            >>> href = await ui.get_element_attribute_value("a.link", "href")
        """
        if not self.page:
            error_msg = "Browser not initialized. Call setup_browser() first."
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        try:
            element = await self.page.query_selector(selector)
            if element:
                value = await element.get_attribute(attribute)
                self.logger.debug(f"Element attribute ({selector}.{attribute}): {value}")
                return str(value) if value is not None else None
            return None
        except Exception as e:
            error_msg = f"Failed to get element attribute {selector}.{attribute}: {e}"
            self.logger.error(error_msg)
            from ..exceptions import OperationError

            raise OperationError(error_msg, str(e)) from e

    async def scroll_to_element(self, selector: str) -> None:
        """
        Scroll to element on the page.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.locator(selector).scroll_into_view_if_needed()
            self.logger.debug(f"Scrolled to element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to scroll to element {selector}: {e}")

    async def wait_for_navigation(self, timeout: int = 5000) -> None:
        """
        Wait for page navigation to complete.

        Args:
            timeout: Timeout in milliseconds
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.logger.debug("Navigation completed")
        except Exception as e:
            self.logger.error(f"Navigation timeout: {e}")

    async def execute_script(self, script: str) -> Any:
        """
        Execute JavaScript on the page.

        Args:
            script: JavaScript code to execute

        Returns:
            Script execution result
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return None
        try:
            result = await self.page.evaluate(script)
            self.logger.debug(f"Script executed, result: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Script execution failed: {e}")
            return None

    async def get_page_title(self) -> str:
        """
        Get page title.

        Returns:
            Page title
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return ""
        try:
            title = await self.page.title()
            self.logger.debug(f"Page title: {title}")
            return str(title)
        except Exception as e:
            self.logger.error(f"Failed to get page title: {e}")
            return ""

    async def get_page_url(self) -> str:
        """
        Get current page URL.

        Returns:
            Current page URL
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return ""
        try:
            url = self.page.url
            self.logger.debug(f"Page URL: {url}")
            return str(url)
        except Exception as e:
            self.logger.error(f"Failed to get page URL: {e}")
            return ""

    async def hover_element(self, selector: str) -> None:
        """
        Hover over element on the page.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.hover(selector)
            self.logger.debug(f"Hovered over element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to hover over element {selector}: {e}")

    async def double_click_element(self, selector: str) -> None:
        """
        Double click element on the page.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.dblclick(selector)
            self.logger.debug(f"Double clicked element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to double click element {selector}: {e}")

    async def right_click_element(self, selector: str) -> None:
        """
        Right click element on the page.

        Args:
            selector: CSS selector for element
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.click(selector, button="right")
            self.logger.debug(f"Right clicked element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to right click element {selector}: {e}")

    async def select_option(self, selector: str, value: str) -> None:
        """
        Select option from dropdown.

        Args:
            selector: CSS selector for select element
            value: Option value to select
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.select_option(selector, value)
            self.logger.debug(f"Selected option {value} in {selector}")
        except Exception as e:
            self.logger.error(f"Failed to select option {value} in {selector}: {e}")

    async def check_checkbox(self, selector: str) -> None:
        """
        Check checkbox on the page.

        Args:
            selector: CSS selector for checkbox
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.check(selector)
            self.logger.debug(f"Checked checkbox: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to check checkbox {selector}: {e}")

    async def uncheck_checkbox(self, selector: str) -> None:
        """
        Uncheck checkbox on the page.

        Args:
            selector: CSS selector for checkbox
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.uncheck(selector)
            self.logger.debug(f"Unchecked checkbox: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to uncheck checkbox {selector}: {e}")

    async def upload_file(self, selector: str, file_path: str) -> None:
        """
        Upload file to file input.

        Args:
            selector: CSS selector for file input
            file_path: Path to file to upload
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.set_input_files(selector, file_path)
            self.logger.debug(f"Uploaded file {file_path} to {selector}")
        except Exception as e:
            self.logger.error(f"Failed to upload file {file_path} to {selector}: {e}")

    async def press_key(self, key: str) -> None:
        """
        Press key on page.

        Args:
            key: Key to press (e.g., 'Enter', 'Escape', 'Tab')
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.keyboard.press(key)
            self.logger.debug(f"Pressed key: {key}")
        except Exception as e:
            self.logger.error(f"Failed to press key {key}: {e}")

    async def type_text(self, text: str) -> None:
        """
        Type text on page.

        Args:
            text: Text to type
        """
        if not self.page:
            self.logger.error("Browser not initialized. Call setup_browser() first.")
            return
        try:
            await self.page.keyboard.type(text)
            self.logger.debug(f"Typed text: {text}")
        except Exception as e:
            self.logger.error(f"Failed to type text: {e}")

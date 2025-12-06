"""
Asynchronous UI Client for web automation testing.

This module provides AsyncUiClient class for browser automation using Playwright async API.
Recommended for production use, multiple browsers, and async applications.
"""

# Python imports
from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Any

from playwright.async_api import Browser, Page, Playwright, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

# Local imports
from ....config import Config
from ....exceptions import NotFoundError, OperationError, TimeoutError

if TYPE_CHECKING:
    from pathlib import Path


class UiClient:
    """
    Asynchronous UI Client for browser automation using Playwright.

    This is the main UI client for production use. It uses Playwright's async API
    for non-blocking operations and supports parallel execution of multiple browsers.

    Attributes:
        url: Base URL for the application
        config: Configuration object
        browser: Playwright Browser instance (None until setup_browser is called)
        page: Playwright Page instance (None until setup_browser is called)
        _playwright: Playwright instance (internal)

    Example:
        >>> from py_web_automation.clients.ui_client import AsyncUiClient
        >>> from py_web_automation.config import Config
        >>> config = Config(timeout=30, browser_headless=True)
        >>> async with AsyncUiClient("https://example.com", config) as ui:
        ...     await ui.setup_browser()
        ...     await ui.page.goto("https://example.com")
        ...     await ui.click_element("#button")
    """

    def __init__(self, url: str, config: Config | None = None) -> None:
        """
        Initialize async UI client.

        Args:
            url: Base URL for the application
            config: Configuration object (uses default if None)

        Example:
            >>> ui = AsyncUiClient("https://example.com", Config(timeout=30))
        """
        if config is None:
            config = Config()
        elif not isinstance(config, Config):
            raise TypeError("config must be a Config object or None")
        self.url: str = url
        self.config: Config = config
        self.browser: Browser | None = None
        self.page: Page | None = None
        self._playwright: Playwright | None = None

    async def __aenter__(self) -> UiClient:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Async context manager exit - cleanup resources."""
        await self.close()

    async def setup_browser(self) -> UiClient:
        """
        Setup Playwright browser for UI testing.

        Launches Chromium browser and creates a new page. This method is
        idempotent - calling it multiple times will not create additional browsers.

        Returns:
            Self for method chaining

        Raises:
            ConnectionError: If browser setup fails

        Example:
            >>> ui = await ui.setup_browser()
            >>> await ui.page.goto("https://example.com")
        """
        if self.browser is not None:
            return self
        try:
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(
                headless=self.config.browser_headless
            )
            self.page = await self.browser.new_page()
            # Set custom User-Agent
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            await self.page.set_extra_http_headers({"User-Agent": user_agent})
            return self
        except Exception as e:
            error_msg = f"Failed to setup browser: {e}"
            raise ConnectionError(error_msg, str(e)) from e

    async def close(self) -> None:
        """
        Close browser and cleanup resources.

        This method is automatically called when exiting an async context manager.

        Example:
            >>> await ui.close()
        """
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

    def _ensure_browser_initialized(self) -> None:
        """Check if browser is initialized, raise error if not."""
        if self.browser is None or self.page is None:
            error_msg = "Browser not initialized. Call setup_browser() first."
            raise RuntimeError(error_msg)

    async def click_element(self, selector: str) -> None:
        """
        Click element by CSS selector.

        Args:
            selector: CSS selector for the element

        Raises:
            RuntimeError: If browser is not initialized
            NotFoundError: If element is not found or click fails

        Example:
            >>> await ui.click_element("#submit-button")
        """
        self._ensure_browser_initialized()
        try:
            await self.page.click(selector)  # type: ignore[union-attr]
        except Exception as e:
            error_msg = f"Failed to click element '{selector}': {e}"
            raise NotFoundError(error_msg, str(e)) from e

    async def fill_input(self, selector: str, value: str) -> None:
        """
        Fill input field by CSS selector.

        Args:
            selector: CSS selector for the input field
            value: Value to fill

        Raises:
            RuntimeError: If browser is not initialized
            NotFoundError: If input is not found or fill fails

        Example:
            >>> await ui.fill_input("#username", "testuser")
        """
        self._ensure_browser_initialized()
        try:
            await self.page.fill(selector, value)  # type: ignore[union-attr]
        except Exception as e:
            error_msg = f"Failed to fill input '{selector}': {e}"
            raise NotFoundError(error_msg, str(e)) from e

    async def wait_for_element(self, selector: str, timeout: float | None = None) -> None:
        """
        Wait for element to appear.

        Args:
            selector: CSS selector for the element
            timeout: Timeout in milliseconds (uses config timeout if None)

        Raises:
            RuntimeError: If browser is not initialized
            TimeoutError: If element does not appear within timeout

        Example:
            >>> await ui.wait_for_element("#content", timeout=5000)
        """
        self._ensure_browser_initialized()
        timeout_ms = timeout if timeout is not None else self.config.browser_timeout
        try:
            await self.page.wait_for_selector(selector, timeout=timeout_ms)  # type: ignore[union-attr]
        except PlaywrightTimeoutError as e:
            error_msg = f"Element '{selector}' did not appear within {timeout_ms}ms"
            raise TimeoutError(error_msg, str(e)) from e

    async def get_element_text(self, selector: str) -> str | None:
        """
        Get text content of element.

        Args:
            selector: CSS selector for the element

        Returns:
            Text content of element, or None if element not found

        Raises:
            RuntimeError: If browser is not initialized
            OperationError: If query fails

        Example:
            >>> text = await ui.get_element_text("#title")
        """
        self._ensure_browser_initialized()
        try:
            element = await self.page.query_selector(selector)  # type: ignore[union-attr]
            if element is None:
                return None
            text = await element.text_content()
            return text
        except Exception as e:
            error_msg = f"Failed to get element text '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def get_element_attribute_value(self, selector: str, attribute: str) -> str | None:
        """
        Get attribute value of element.

        Args:
            selector: CSS selector for the element
            attribute: Attribute name to retrieve

        Returns:
            Attribute value, or None if element or attribute not found

        Raises:
            RuntimeError: If browser is not initialized
            OperationError: If query fails

        Example:
            >>> href = await ui.get_element_attribute_value("a", "href")
        """
        self._ensure_browser_initialized()
        try:
            element = await self.page.query_selector(selector)  # type: ignore[union-attr]
            if element is None:
                return None
            value = await element.get_attribute(attribute)
            return value
        except Exception as e:
            error_msg = f"Failed to get element attribute '{attribute}' for '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def hover_element(self, selector: str) -> None:
        """
        Hover over element.

        Args:
            selector: CSS selector for the element

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.hover_element("#menu-item")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.hover(selector)
        except Exception as e:
            error_msg = f"Failed to hover over element '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def double_click_element(self, selector: str) -> None:
        """
        Double click element.

        Args:
            selector: CSS selector for the element

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.double_click_element("#button")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.dblclick(selector)
        except Exception as e:
            error_msg = f"Failed to double click element '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def right_click_element(self, selector: str) -> None:
        """
        Right click element.

        Args:
            selector: CSS selector for the element

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.right_click_element("#menu")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.click(selector, button="right")
        except Exception as e:
            error_msg = f"Failed to right click element '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def select_option(self, selector: str, value: str) -> None:
        """
        Select option in dropdown/select element.

        Args:
            selector: CSS selector for the select element
            value: Option value to select

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.select_option("#country", "USA")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.select_option(selector, value)
        except Exception as e:
            error_msg = f"Failed to select option '{value}' in '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def check_checkbox(self, selector: str) -> None:
        """
        Check checkbox.

        Args:
            selector: CSS selector for the checkbox

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.check_checkbox("#agree")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.check(selector)
        except Exception as e:
            error_msg = f"Failed to check checkbox '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def uncheck_checkbox(self, selector: str) -> None:
        """
        Uncheck checkbox.

        Args:
            selector: CSS selector for the checkbox

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.uncheck_checkbox("#agree")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.uncheck(selector)
        except Exception as e:
            error_msg = f"Failed to uncheck checkbox '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def upload_file(self, selector: str, file_path: str | Path) -> None:
        """
        Upload file to file input.

        Args:
            selector: CSS selector for the file input
            file_path: Path to file to upload

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.upload_file("#file-input", "document.pdf")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.set_input_files(selector, str(file_path))
        except Exception as e:
            error_msg = f"Failed to upload file '{file_path}' to '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def press_key(self, key: str) -> None:
        """
        Press keyboard key.

        Args:
            key: Key to press (e.g., "Enter", "Tab", "Escape")

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.press_key("Enter")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.keyboard.press(key)
        except Exception as e:
            error_msg = f"Failed to press key '{key}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def type_text(self, text: str) -> None:
        """
        Type text at current focus.

        Args:
            text: Text to type

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.type_text("Hello, World!")
        """
        if self.browser is None or self.page is None:
            return
        try:
            await self.page.keyboard.type(text)
        except Exception as e:
            error_msg = f"Failed to type text: {e}"
            raise OperationError(error_msg, str(e)) from e

    async def scroll_to_element(self, selector: str) -> None:
        """
        Scroll element into view.

        Args:
            selector: CSS selector for the element

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.scroll_to_element("#footer")
        """
        if self.browser is None or self.page is None:
            return
        try:
            locator = self.page.locator(selector)
            await locator.scroll_into_view_if_needed()
        except Exception as e:
            error_msg = f"Failed to scroll to element '{selector}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def wait_for_navigation(self, timeout: float | None = None) -> None:
        """
        Wait for page navigation to complete.

        Args:
            timeout: Timeout in milliseconds (uses config timeout if None)

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> await ui.wait_for_navigation(timeout=5000)
        """
        if self.browser is None or self.page is None:
            return
        timeout_ms = timeout if timeout is not None else self.config.browser_timeout
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout_ms)
        except PlaywrightTimeoutError as e:
            error_msg = f"Navigation timeout: {e}"
            raise TimeoutError(error_msg, str(e)) from e

    async def get_page_title(self) -> str:
        """
        Get page title.

        Returns:
            Page title, or empty string on error

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> title = await ui.get_page_title()
        """
        if self.browser is None or self.page is None:
            return ""
        try:
            title = await self.page.title()
            return title
        except Exception as e:
            error_msg = f"Failed to get page title: {e}"
            raise OperationError(error_msg, str(e)) from e

    async def get_page_url(self) -> str:
        """
        Get current page URL.

        Returns:
            Current page URL, or empty string on error

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> url = await ui.get_page_url()
        """
        if self.browser is None or self.page is None:
            return ""
        try:
            url = self.page.url
            return url
        except Exception as e:
            error_msg = f"Failed to get page URL: {e}"
            raise OperationError(error_msg, str(e)) from e

    async def take_screenshot(self, filename: str) -> None:
        """
        Take screenshot of current page.

        Args:
            filename: Path to save screenshot

        Raises:
            RuntimeError: If browser is not initialized
            OperationError: If screenshot fails

        Example:
            >>> await ui.take_screenshot("screenshot.png")
        """
        self._ensure_browser_initialized()
        try:
            await self.page.screenshot(path=filename)  # type: ignore[union-attr]
        except Exception as e:
            error_msg = f"Failed to take screenshot '{filename}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def execute_script(self, script: str) -> Any:
        """
        Execute JavaScript in page context.

        Args:
            script: JavaScript code to execute

        Returns:
            Result of script execution, or None on error

        Raises:
            RuntimeError: If browser is not initialized

        Example:
            >>> result = await ui.execute_script("return document.title")
        """
        if self.browser is None or self.page is None:
            return None
        try:
            result = await self.page.evaluate(script)
            return result
        except Exception as e:
            error_msg = f"Failed to execute script: {e}"
            raise OperationError(error_msg, str(e)) from e

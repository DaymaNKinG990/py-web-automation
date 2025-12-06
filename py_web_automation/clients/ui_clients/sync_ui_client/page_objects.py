"""
Synchronous Page Object Model (POM) support for UI testing.

This module provides base classes and utilities for implementing
Page Object Model pattern in synchronous UI tests using SyncUiClient.
"""

# Python imports
from abc import ABC, abstractmethod

# Local imports
from ....exceptions import NotFoundError, TimeoutError
from .ui_client import UiClient


class BasePage(ABC):
    """
    Base class for synchronous Page Objects.

    Provides common functionality for page objects following the
    Page Object Model pattern. Each page object represents a single
    page or component of a web application.

    Attributes:
        ui_client: SyncUiClient instance for browser interactions
        url: URL of the page
        config: Configuration object

    Example:
        >>> class LoginPage(BasePage):
        ...     def __init__(self, ui_client: SyncUiClient):
        ...         super().__init__(ui_client, "https://example.com/login")
        ...
        ...     def login(self, username: str, password: str):
        ...         self.fill_input("#username", username)
        ...         self.fill_input("#password", password)
        ...         self.click_element("#submit")
    """

    def __init__(self, ui_client: UiClient, url: str | None = None) -> None:
        """
        Initialize page object.

        Args:
            ui_client: SyncUiClient instance for browser interactions
            url: Optional URL of the page (can be set later)
        """
        self.ui_client = ui_client
        self.url = url

    def navigate(self, url: str | None = None) -> None:
        """
        Navigate to page URL.

        Args:
            url: URL to navigate to (uses self.url if not provided)

        Raises:
            ValueError: If no URL is provided and self.url is None
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("URL must be provided or set in page object")
        self.ui_client.setup_browser()
        if self.ui_client.page:
            self.ui_client.page.goto(target_url, wait_until="networkidle")

    def wait_for_page_load(self, timeout: float | None = None) -> None:
        """
        Wait for page to load completely.

        Args:
            timeout: Timeout in milliseconds (uses config timeout if None)
        """
        if timeout is not None:
            self.ui_client.wait_for_navigation(timeout=int(timeout))
        else:
            self.ui_client.wait_for_navigation()

    # Delegate common UI operations to ui_client
    def click_element(self, selector: str) -> None:
        """Click element by selector."""
        self.ui_client.click_element(selector)

    def fill_input(self, selector: str, value: str) -> None:
        """Fill input field by selector."""
        self.ui_client.fill_input(selector, value)

    def get_element_text(self, selector: str) -> str:
        """Get text content of element."""
        text = self.ui_client.get_element_text(selector)
        return text if text is not None else ""

    def get_element_attribute_value(self, selector: str, attribute: str) -> str:
        """Get attribute value of element."""
        value = self.ui_client.get_element_attribute_value(selector, attribute)
        return value if value is not None else ""

    def wait_for_element(self, selector: str, timeout: float | None = None) -> None:
        """Wait for element to appear."""
        if timeout is not None:
            self.ui_client.wait_for_element(selector, timeout=int(timeout))
        else:
            self.ui_client.wait_for_element(selector)

    def is_element_visible(self, selector: str) -> bool:
        """
        Check if element is visible.

        Args:
            selector: CSS selector

        Returns:
            True if element is visible, False otherwise
        """
        try:
            self.ui_client.wait_for_element(selector, timeout=1000)
            return True
        except (NotFoundError, TimeoutError):
            return False

    def get_page_title(self) -> str:
        """Get page title."""
        return self.ui_client.get_page_title()

    def get_page_url(self) -> str:
        """Get current page URL."""
        return self.ui_client.get_page_url()

    def take_screenshot(self, filename: str) -> None:
        """Take screenshot of page."""
        self.ui_client.take_screenshot(filename)

    @abstractmethod
    def is_loaded(self) -> bool:
        """
        Check if page is loaded.

        Should be implemented by subclasses to verify page-specific
        elements that indicate the page has loaded.

        Returns:
            True if page is loaded, False otherwise

        Example:
            >>> def is_loaded(self) -> bool:
            ...     return self.is_element_visible("#main-content")
        """
        pass


class Component:
    """
    Base class for reusable synchronous UI components.

    Represents a reusable component that can be used across multiple pages.
    Examples: Header, Footer, Navigation, Modal, etc.

    Attributes:
        ui_client: SyncUiClient instance
        base_selector: Base CSS selector for the component

    Example:
        >>> class NavigationComponent(Component):
        ...     def __init__(self, ui_client: SyncUiClient):
        ...         super().__init__(ui_client, "nav.main-nav")
        ...
        ...     def click_home(self):
        ...         self.click_element(f"{self.base_selector} a.home")
    """

    def __init__(self, ui_client: UiClient, base_selector: str) -> None:
        """
        Initialize component.

        Args:
            ui_client: SyncUiClient instance
            base_selector: Base CSS selector for the component
        """
        self.ui_client = ui_client
        self.base_selector = base_selector

    def _selector(self, child_selector: str) -> str:
        """
        Build full selector from base and child selector.

        Args:
            child_selector: Child selector (relative to base)

        Returns:
            Full CSS selector
        """
        if child_selector.startswith(self.base_selector):
            return child_selector
        return f"{self.base_selector} {child_selector}"

    def click_element(self, selector: str) -> None:
        """Click element within component."""
        self.ui_client.click_element(self._selector(selector))

    def fill_input(self, selector: str, value: str) -> None:
        """Fill input within component."""
        self.ui_client.fill_input(self._selector(selector), value)

    def get_element_text(self, selector: str) -> str:
        """Get text from element within component."""
        text = self.ui_client.get_element_text(self._selector(selector))
        return text if text is not None else ""

    def wait_for_element(self, selector: str, timeout: float | None = None) -> None:
        """Wait for element within component."""
        if timeout is not None:
            self.ui_client.wait_for_element(self._selector(selector), timeout=int(timeout))
        else:
            self.ui_client.wait_for_element(self._selector(selector))

    def is_visible(self) -> bool:
        """
        Check if component is visible.

        Returns:
            True if component is visible, False otherwise
        """
        try:
            self.ui_client.wait_for_element(self.base_selector, timeout=1000)
            return True
        except (NotFoundError, TimeoutError):
            return False


class PageFactory:
    """
    Factory for creating synchronous page objects.

    Provides a centralized way to create and manage page objects,
    ensuring proper initialization and URL management.

    Example:
        >>> factory = PageFactory(ui_client)
        >>> login_page = factory.create_page(LoginPage, "https://example.com/login")
        >>> login_page.navigate()
    """

    def __init__(self, ui_client: UiClient) -> None:
        """
        Initialize page factory.

        Args:
            ui_client: SyncUiClient instance to use for all pages
        """
        self.ui_client = ui_client
        self._pages: dict[str, BasePage] = {}

    def create_page(self, page_class: type[BasePage], url: str | None = None) -> BasePage:
        """
        Create a page object instance.

        Args:
            page_class: Page class to instantiate
            url: Optional URL for the page

        Returns:
            Page object instance

        Example:
            >>> login_page = factory.create_page(LoginPage, "https://example.com/login")
        """
        page = page_class(self.ui_client, url)
        if url:
            self._pages[url] = page
        return page

    def get_page(self, url: str) -> BasePage | None:
        """
        Get existing page object by URL.

        Args:
            url: URL of the page

        Returns:
            Page object if found, None otherwise
        """
        return self._pages.get(url)

"""
Unit tests for page_objects module.
"""

from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

from py_web_automation.clients.ui_client import UiClient
from py_web_automation.exceptions import NotFoundError, TimeoutError
from py_web_automation.page_objects import BasePage, Component, PageFactory

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.ui]


class _MockPage(BasePage):
    """Mock page implementation for testing."""

    async def is_loaded(self) -> bool:
        """Check if page is loaded."""
        return await self.is_element_visible("#main-content")


@pytest.mark.unit
class TestBasePage:
    """Test BasePage class."""

    @allure.title("TC-PO-001: BasePage - инициализация")
    @allure.description("Test BasePage initialization. TC-PO-001")
    def test_base_page_init(self):
        """Test BasePage initialization."""
        with allure.step("Create TestPage with UiClient and URL"):
            ui_client = MagicMock(spec=UiClient)
            page = _MockPage(ui_client, url="https://example.com")

        with allure.step("Verify ui_client and url set correctly"):
            assert page.ui_client == ui_client
            assert page.url == "https://example.com"

    @pytest.mark.asyncio
    @allure.title("TC-PO-002: BasePage - navigate")
    @allure.description("Test navigation to page URL. TC-PO-002")
    async def test_base_page_navigate(self):
        """Test navigation to page URL."""
        with allure.step("Create BasePage with URL"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.setup_browser = AsyncMock()
            ui_client.page = MagicMock()
            ui_client.page.goto = AsyncMock()
            page = _MockPage(ui_client, url="https://example.com")

        with allure.step("Call navigate"):
            await page.navigate()

        with allure.step("Verify setup_browser and page.goto called"):
            ui_client.setup_browser.assert_called_once()
            ui_client.page.goto.assert_called_once_with("https://example.com", wait_until="networkidle")

    @pytest.mark.asyncio
    @allure.title("TC-PO-003: BasePage - navigate без URL")
    @allure.description("Test ValueError when no URL provided. TC-PO-003")
    async def test_base_page_navigate_no_url(self):
        """Test ValueError when no URL provided."""
        with allure.step("Create BasePage without URL"):
            ui_client = MagicMock(spec=UiClient)
            page = _MockPage(ui_client)

        with allure.step("Call navigate without URL and expect ValueError"):
            with pytest.raises(ValueError, match="URL must be provided"):
                await page.navigate()

    @pytest.mark.asyncio
    @allure.title("TC-PO-004: BasePage - wait_for_page_load")
    @allure.description("Test waiting for page load. TC-PO-004")
    async def test_base_page_wait_for_page_load(self):
        """Test waiting for page load."""
        with allure.step("Create BasePage"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.wait_for_navigation = AsyncMock()
            page = _MockPage(ui_client)

        with allure.step("Call wait_for_page_load"):
            await page.wait_for_page_load(timeout=5000)

        with allure.step("Verify wait_for_navigation called with timeout"):
            ui_client.wait_for_navigation.assert_called_once_with(timeout=5000)

    @pytest.mark.asyncio
    @allure.title("TC-PO-005: BasePage - делегирование методов")
    @allure.description("Test methods delegate to ui_client. TC-PO-005")
    async def test_base_page_delegation(self):
        """Test methods delegate to ui_client."""
        with allure.step("Create BasePage with mocked UiClient"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.click_element = AsyncMock()
            ui_client.fill_input = AsyncMock()
            ui_client.get_element_text = AsyncMock(return_value="text")
            page = _MockPage(ui_client)

        with allure.step("Call delegated methods"):
            await page.click_element("#button")
            await page.fill_input("#input", "value")
            text = await page.get_element_text("#element")

        with allure.step("Verify ui_client methods called"):
            ui_client.click_element.assert_called_once_with("#button")
            ui_client.fill_input.assert_called_once_with("#input", "value")
            ui_client.get_element_text.assert_called_once_with("#element")
            assert text == "text"

    @pytest.mark.asyncio
    @allure.title("TC-PO-006: BasePage - is_element_visible")
    @allure.description("Test element visibility check. TC-PO-006")
    async def test_base_page_is_element_visible(self):
        """Test element visibility check."""
        with allure.step("Create BasePage with mocked UiClient"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.wait_for_element = AsyncMock()
            page = _MockPage(ui_client)

        with allure.step("Call is_element_visible"):
            result = await page.is_element_visible("#element")

        with allure.step("Verify True returned when element visible"):
            assert result is True
            ui_client.wait_for_element.assert_called_once_with("#element", timeout=1000)

    @pytest.mark.asyncio
    @allure.title("TC-PO-007: BasePage - is_element_visible невидимый элемент")
    @allure.description("Test False returned for invisible element. TC-PO-007")
    async def test_base_page_is_element_visible_not_found(self):
        """Test False returned for invisible element."""
        with allure.step("Create BasePage with mocked UiClient"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.wait_for_element = AsyncMock(side_effect=NotFoundError("Element not found"))
            page = _MockPage(ui_client)

        with allure.step("Call is_element_visible"):
            result = await page.is_element_visible("#element")

        with allure.step("Verify False returned when element not found"):
            assert result is False


@pytest.mark.unit
class TestComponent:
    """Test Component class."""

    @allure.title("TC-PO-008: Component - инициализация")
    @allure.description("Test Component initialization. TC-PO-008")
    def test_component_init(self):
        """Test Component initialization."""
        with allure.step("Create Component with UiClient and base_selector"):
            ui_client = MagicMock(spec=UiClient)
            component = Component(ui_client, base_selector="nav.main")

        with allure.step("Verify ui_client and base_selector set correctly"):
            assert component.ui_client == ui_client
            assert component.base_selector == "nav.main"

    @allure.title("TC-PO-009: Component - _selector")
    @allure.description("Test selector building. TC-PO-009")
    def test_component_selector(self):
        """Test selector building."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            component = Component(ui_client, base_selector="nav.main")

        with allure.step("Call _selector with child selector"):
            full_selector = component._selector("a.home")

        with allure.step("Verify full selector built correctly"):
            assert full_selector == "nav.main a.home"

    @allure.title("TC-PO-010: Component - _selector с полным селектором")
    @allure.description("Test full selector not modified. TC-PO-010")
    def test_component_selector_full(self):
        """Test full selector not modified."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            component = Component(ui_client, base_selector="nav.main")

        with allure.step("Call _selector with full selector"):
            full_selector = component._selector("nav.main a.home")

        with allure.step("Verify full selector returned as-is"):
            assert full_selector == "nav.main a.home"

    @pytest.mark.asyncio
    @allure.title("TC-PO-011: Component - делегирование методов")
    @allure.description("Test methods use _selector. TC-PO-011")
    async def test_component_delegation(self):
        """Test methods use _selector."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.click_element = AsyncMock()
            component = Component(ui_client, base_selector="nav")

        with allure.step("Call click_element with child selector"):
            await component.click_element("a.home")

        with allure.step("Verify ui_client.click_element called with full selector"):
            ui_client.click_element.assert_called_once_with("nav a.home")

    @pytest.mark.asyncio
    @allure.title("TC-PO-012: Component - is_visible")
    @allure.description("Test component visibility check. TC-PO-012")
    async def test_component_is_visible(self):
        """Test component visibility check."""
        with allure.step("Create Component with mocked UiClient"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.wait_for_element = AsyncMock()
            component = Component(ui_client, base_selector="nav")

        with allure.step("Call is_visible"):
            result = await component.is_visible()

        with allure.step("Verify True returned when component visible"):
            assert result is True
            ui_client.wait_for_element.assert_called_once_with("nav", timeout=1000)

    @pytest.mark.asyncio
    @allure.title("TC-PO-COMP-002: Component - wait_for_element")
    @allure.description("Test waiting for element within component. TC-PO-COMP-002")
    async def test_component_wait_for_element(self):
        """Test waiting for element within component."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.wait_for_element = AsyncMock()
            component = Component(ui_client, base_selector="nav")

        with allure.step("Call wait_for_element"):
            await component.wait_for_element("a.link")

        with allure.step("Verify ui_client.wait_for_element called with full selector"):
            ui_client.wait_for_element.assert_called_once_with("nav a.link")

    @pytest.mark.asyncio
    @allure.title("TC-PO-COMP-004: Component - fill_input")
    @allure.description("Test filling input within component. TC-PO-COMP-004")
    async def test_component_fill_input(self):
        """Test filling input within component."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.fill_input = AsyncMock()
            component = Component(ui_client, base_selector="form")

        with allure.step("Call fill_input"):
            await component.fill_input("input.name", "John")

        with allure.step("Verify ui_client.fill_input called with full selector"):
            ui_client.fill_input.assert_called_once_with("form input.name", "John")

    @pytest.mark.asyncio
    @allure.title("TC-PO-COMP-005: Component - get_element_text")
    @allure.description("Test getting element text within component. TC-PO-COMP-005")
    async def test_component_get_element_text(self):
        """Test getting element text within component."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.get_element_text = AsyncMock(return_value="Text")
            component = Component(ui_client, base_selector="div")

        with allure.step("Call get_element_text"):
            result = await component.get_element_text("span")

        with allure.step("Verify ui_client.get_element_text called with full selector"):
            ui_client.get_element_text.assert_called_once_with("div span")
            assert result == "Text"

    @pytest.mark.asyncio
    @allure.title("TC-PO-COMP-006: Component - wait_for_element с timeout")
    @allure.description("Test waiting for element with custom timeout. TC-PO-COMP-006")
    async def test_component_wait_for_element_with_timeout(self):
        """Test waiting for element with custom timeout."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.wait_for_element = AsyncMock()
            component = Component(ui_client, base_selector="nav")

        with allure.step("Call wait_for_element with timeout"):
            await component.wait_for_element("a.link", timeout=5000)

        with allure.step("Verify ui_client.wait_for_element called with timeout"):
            ui_client.wait_for_element.assert_called_once_with("nav a.link", timeout=5000)

    @pytest.mark.asyncio
    @allure.title("TC-PO-COMP-007: Component - is_visible с NotFoundError")
    @allure.description("Test False returned when component not found. TC-PO-COMP-007")
    async def test_component_is_visible_not_found_error(self):
        """Test False returned when component not found."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.wait_for_element = AsyncMock(side_effect=NotFoundError("Element not found"))
            component = Component(ui_client, base_selector="nav")

        with allure.step("Call is_visible"):
            result = await component.is_visible()

        with allure.step("Verify False returned when component not found"):
            assert result is False
            ui_client.wait_for_element.assert_called_once_with("nav", timeout=1000)

    @pytest.mark.asyncio
    @allure.title("TC-PO-COMP-008: Component - is_visible с TimeoutError")
    @allure.description("Test False returned when component timeout. TC-PO-COMP-008")
    async def test_component_is_visible_timeout_error(self):
        """Test False returned when component timeout."""
        with allure.step("Create Component with base_selector"):
            ui_client = MagicMock(spec=UiClient)
            ui_client.wait_for_element = AsyncMock(side_effect=TimeoutError("Timeout"))
            component = Component(ui_client, base_selector="nav")

        with allure.step("Call is_visible"):
            result = await component.is_visible()

        with allure.step("Verify False returned when component timeout"):
            assert result is False
            ui_client.wait_for_element.assert_called_once_with("nav", timeout=1000)


@pytest.mark.unit
class TestPageFactory:
    """Test PageFactory class."""

    @allure.title("TC-PO-013: PageFactory - инициализация")
    @allure.description("Test PageFactory initialization. TC-PO-013")
    def test_page_factory_init(self):
        """Test PageFactory initialization."""
        with allure.step("Create PageFactory with UiClient"):
            ui_client = MagicMock(spec=UiClient)
            factory = PageFactory(ui_client)

        with allure.step("Verify ui_client and _pages initialized"):
            assert factory.ui_client == ui_client
            assert factory._pages == {}

    @allure.title("TC-PO-014: PageFactory - create_page")
    @allure.description("Test page object creation. TC-PO-014")
    def test_page_factory_create_page(self):
        """Test page object creation."""
        with allure.step("Create PageFactory"):
            ui_client = MagicMock(spec=UiClient)
            factory = PageFactory(ui_client)

        with allure.step("Create page with URL"):
            page = factory.create_page(_MockPage, url="https://example.com")

        with allure.step("Verify page instance created and stored"):
            assert isinstance(page, _MockPage)
            assert factory.get_page("https://example.com") == page

    @allure.title("TC-PO-015: PageFactory - get_page")
    @allure.description("Test getting page by URL. TC-PO-015")
    def test_page_factory_get_page(self):
        """Test getting page by URL."""
        with allure.step("Create PageFactory"):
            ui_client = MagicMock(spec=UiClient)
            factory = PageFactory(ui_client)

        with allure.step("Create page with URL"):
            page = factory.create_page(_MockPage, url="https://example.com")

        with allure.step("Get page by URL"):
            retrieved_page = factory.get_page("https://example.com")

        with allure.step("Verify page returned"):
            assert retrieved_page == page

    @allure.title("TC-PO-016: PageFactory - get_page не найден")
    @allure.description("Test None returned when page not found. TC-PO-016")
    def test_page_factory_get_page_not_found(self):
        """Test None returned when page not found."""
        with allure.step("Create PageFactory without pages"):
            ui_client = MagicMock(spec=UiClient)
            factory = PageFactory(ui_client)

        with allure.step("Get non-existent page"):
            page = factory.get_page("https://nonexistent.com")

        with allure.step("Verify None returned"):
            assert page is None

"""
Fixtures for UiClient testing.
"""

# Python imports
import asyncio
from playwright.async_api import Browser, Page
from pytest import FixtureRequest, fixture
from pytest_mock import MockerFixture

# Local imports
from py_web_automation.clients.ui_clients import UiClient
from py_web_automation.config import Config


async def _cleanup_ui_client_async(client: UiClient) -> None:
    """Async cleanup function for UiClient resources."""
    if client.browser or client._playwright:
        try:
            await client.close()
        except Exception:
            pass  # Ignore errors during cleanup


@fixture
def mock_browser(mocker: MockerFixture) -> MockerFixture:
    """Create a mock Browser instance."""
    browser = mocker.AsyncMock(spec=Browser)
    browser.close = mocker.AsyncMock()
    browser.new_page = mocker.AsyncMock()
    return browser


@fixture
def mock_page(mocker: MockerFixture) -> MockerFixture:
    """Create a mock Page instance."""
    page = mocker.AsyncMock(spec=Page)
    page.click = mocker.AsyncMock()
    page.fill = mocker.AsyncMock()
    page.hover = mocker.AsyncMock()
    page.dblclick = mocker.AsyncMock()
    page.check = mocker.AsyncMock()
    page.uncheck = mocker.AsyncMock()
    page.select_option = mocker.AsyncMock()
    page.wait_for_selector = mocker.AsyncMock()
    page.wait_for_load_state = mocker.AsyncMock()
    page.screenshot = mocker.AsyncMock()
    page.query_selector = mocker.AsyncMock()
    page.locator = mocker.MagicMock()
    page.set_extra_http_headers = mocker.AsyncMock()
    page.set_input_files = mocker.AsyncMock()
    page.keyboard = mocker.MagicMock()
    page.keyboard.press = mocker.AsyncMock()
    page.keyboard.type = mocker.AsyncMock()
    page.evaluate = mocker.AsyncMock()
    page.title = mocker.AsyncMock(return_value="Test Page")
    page.url = "https://example.com/app"
    # Mock locator methods
    mock_locator = mocker.MagicMock()
    mock_locator.scroll_into_view_if_needed = mocker.AsyncMock()
    page.locator.return_value = mock_locator
    # Mock element for query_selector
    mock_element = mocker.MagicMock()
    mock_element.text_content = mocker.AsyncMock(return_value="Test text")
    mock_element.get_attribute = mocker.AsyncMock(return_value="test-value")
    page.query_selector.return_value = mock_element
    return page


@fixture
def ui_client_with_config(valid_config: Config, request: FixtureRequest) -> UiClient:
    """Create UiClient with valid config using async context manager."""
    ui_client = UiClient(base_url="https://example.com/app", config=valid_config)
    
    # Enter async context manager
    def enter_context() -> None:
        """Enter async context manager using event loop."""
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_running():
                loop.run_until_complete(ui_client.__aenter__())
            else:
                # If loop is running, schedule enter
                asyncio.create_task(ui_client.__aenter__())
        except RuntimeError:
            # No event loop exists, create new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        try:
                loop.run_until_complete(ui_client.__aenter__())
        except Exception:
            loop.close()
            raise
    
    # Exit async context manager on cleanup
    def cleanup() -> None:
        """Exit async context manager on cleanup."""
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_running():
                loop.run_until_complete(ui_client.__aexit__(None, None, None))
            else:
                asyncio.create_task(ui_client.__aexit__(None, None, None))
        except RuntimeError:
            # No event loop, create one for cleanup
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(ui_client.__aexit__(None, None, None))
            except Exception:
                pass
        finally:
                if not loop.is_closed():
                    loop.close()
    
    # Enter context manager
    enter_context()
    # Setup cleanup to exit context manager
    request.addfinalizer(cleanup)
    
    return ui_client


@fixture
def ui_client_with_browser(ui_client_with_config, mock_browser, mock_page, request):
    """Create UiClient with browser and page set up using async context manager."""
    # Set up browser and page
    ui_client_with_config.browser = mock_browser
    ui_client_with_config.page = mock_page
    
    # Client is already entered in context manager from ui_client_with_config
    # Just need to ensure proper cleanup on exit
    # The cleanup from ui_client_with_config will handle context manager exit
    return ui_client_with_config


@fixture
async def ui_client_context_manager(valid_config: Config):
    """Create UiClient as async context manager with automatic cleanup."""
    async with UiClient(base_url="https://example.com/app", config=valid_config) as ui_client:
        yield ui_client


@fixture
async def ui_client_with_browser_context_manager(
    valid_config: Config, mock_browser, mock_page
):
    """Create UiClient with browser and page as async context manager with automatic cleanup."""
    ui_client = UiClient(base_url="https://example.com/app", config=valid_config)
    ui_client.browser = mock_browser
    ui_client.page = mock_page
    
    async with ui_client as client:
        yield client



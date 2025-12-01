"""
Global test configuration and fixtures for Web Automation Framework tests.
"""

import asyncio
import logging
import tempfile

import pytest

# ApiClient fixtures
from fixtures.api_client import *  # noqa: F401, F403
from fixtures.base_client import (  # noqa: F401
    base_client_urls,
    base_client_with_config,
    invalid_urls,
)

# Import fixtures from tests.fixtures modules
# Pytest requires explicit imports for fixtures to be discovered
# Import order matters: more specific fixtures should be imported first
# to avoid conflicts with generic ones
# Config data fixtures (no conflicts)
from fixtures.config import *  # noqa: F401, F403

# General data fixtures (includes valid_config - this is the main one)
from fixtures.data_fixtures import (  # noqa: F401
    valid_config_data as valid_config_data_from_data,
)

# Integration test mocks
from fixtures.integration_mocks import *  # noqa: F401, F403

# Other component fixtures (they use valid_config from data_fixtures)
# Import only non-conflicting fixtures
from fixtures.ui_client import *  # noqa: F401, F403
from loguru import logger


# Configure loguru to work with pytest caplog
# Use a sink that sends loguru logs to standard logging
def loguru_sink(message):
    """Sink that redirects loguru logs to standard logging for caplog."""
    # Map loguru levels to logging levels
    level_map = {
        "TRACE": logging.DEBUG,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "SUCCESS": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    # Get the record from the message
    record = message.record

    # Get standard logging level
    log_level = level_map.get(record["level"].name, logging.INFO)

    # Get logger name
    logger_name = record.get("name", "loguru")

    # Create LogRecord for standard logging
    log_record = logging.LogRecord(
        name=logger_name,
        level=log_level,
        pathname=str(record.get("file", {}).path) if hasattr(record.get("file", None), "path") else "",
        lineno=record.get("line", 0),
        msg=str(record["message"]),
        args=(),
        exc_info=record.get("exception"),
    )

    # Send to standard logging
    std_logger = logging.getLogger(logger_name)
    std_logger.handle(log_record)


# Remove default loguru handler and add our sink
logger.remove()
logger.add(loguru_sink, format="{message}", serialize=False)


@pytest.fixture(scope="function")
def event_loop():
    """
    Create an instance of the default event loop for the test.

    Changed scope from "session" to "function" for better compatibility
    with pytest-xdist parallel execution. Each worker needs its own event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def mock_http_client(mocker):
    """Create a mock HTTP client."""
    client = mocker.AsyncMock()
    client.get = mocker.AsyncMock()
    client.post = mocker.AsyncMock()
    client.put = mocker.AsyncMock()
    client.delete = mocker.AsyncMock()
    return client


@pytest.fixture
def mock_playwright_browser(mocker):
    """Create a mock Playwright browser."""
    browser = mocker.AsyncMock()
    browser.close = mocker.AsyncMock()
    browser.new_page = mocker.AsyncMock()
    return browser


@pytest.fixture
def mock_playwright_page(mocker):
    """Create a mock Playwright page."""
    page = mocker.AsyncMock()
    page.goto = mocker.AsyncMock()
    page.close = mocker.AsyncMock()
    page.screenshot = mocker.AsyncMock()
    page.evaluate = mocker.AsyncMock()
    page.locator = mocker.AsyncMock()
    page.wait_for_selector = mocker.AsyncMock()
    page.click = mocker.AsyncMock()
    page.fill = mocker.AsyncMock()
    return page


@pytest.fixture
def mock_playwright_element(mocker):
    """Create a mock Playwright element."""
    element = mocker.AsyncMock()
    element.click = mocker.AsyncMock()
    element.fill = mocker.AsyncMock()
    element.text_content = mocker.AsyncMock()
    element.get_attribute = mocker.AsyncMock()
    element.is_visible = mocker.AsyncMock()
    element.is_enabled = mocker.AsyncMock()
    return element


# Async test helpers
@pytest.fixture
async def async_mock(mocker):
    """Create an async mock."""
    return mocker.AsyncMock()


# Error simulation fixtures
@pytest.fixture
def mock_connection_error():
    """Mock connection error."""
    return ConnectionError("Connection failed")


@pytest.fixture
def mock_timeout_error():
    """Mock timeout error."""
    return TimeoutError("Operation timed out")


# Performance testing fixtures
@pytest.fixture
def performance_timer():
    """Timer for performance testing."""
    import time

    start_time = time.perf_counter()
    yield lambda: time.perf_counter() - start_time


# ============================================================================
# Database Mock Fixtures (scope=function for isolation)
# ============================================================================


@pytest.fixture(scope="function")
def mock_asyncpg_module(mocker):
    """Create a mock asyncpg module for sys.modules."""
    import sys
    from unittest.mock import AsyncMock, MagicMock

    mock_asyncpg = MagicMock()
    mock_connection = AsyncMock()
    mock_connect = AsyncMock(return_value=mock_connection)
    mock_asyncpg.connect = mock_connect
    sys.modules["asyncpg"] = mock_asyncpg

    yield {
        "module": mock_asyncpg,
        "connection": mock_connection,
        "connect": mock_connect,
    }

    # Cleanup: remove from sys.modules if it was added
    if "asyncpg" in sys.modules and sys.modules["asyncpg"] is mock_asyncpg:
        del sys.modules["asyncpg"]


@pytest.fixture(scope="function")
def mock_psycopg_module(mocker):
    """Create a mock psycopg module for sys.modules."""
    import sys
    from unittest.mock import AsyncMock, MagicMock

    mock_psycopg = MagicMock()
    mock_connection = AsyncMock()
    mock_connect = AsyncMock(return_value=mock_connection)
    # psycopg uses AsyncConnection.connect pattern
    mock_async_connection = MagicMock()
    mock_async_connection.connect = mock_connect
    mock_psycopg.AsyncConnection = mock_async_connection
    sys.modules["psycopg"] = mock_psycopg

    yield {
        "module": mock_psycopg,
        "connection": mock_connection,
        "connect": mock_connect,
        "AsyncConnection": mock_async_connection,
    }

    # Cleanup: remove from sys.modules if it was added
    if "psycopg" in sys.modules and sys.modules["psycopg"] is mock_psycopg:
        del sys.modules["psycopg"]


@pytest.fixture(scope="function")
def mock_aiomysql_module(mocker):
    """Create a mock aiomysql module for sys.modules."""
    import sys
    from unittest.mock import AsyncMock, MagicMock

    mock_aiomysql = MagicMock()
    mock_connection = AsyncMock()
    mock_connect = AsyncMock(return_value=mock_connection)
    mock_aiomysql.connect = mock_connect
    mock_aiomysql.DictCursor = MagicMock()
    sys.modules["aiomysql"] = mock_aiomysql

    yield {
        "module": mock_aiomysql,
        "connection": mock_connection,
        "connect": mock_connect,
        "DictCursor": mock_aiomysql.DictCursor,
    }

    # Cleanup: remove from sys.modules if it was added
    if "aiomysql" in sys.modules and sys.modules["aiomysql"] is mock_aiomysql:
        del sys.modules["aiomysql"]


@pytest.fixture(scope="function")
def mock_pymysql_module(mocker):
    """Create a mock pymysql module for sys.modules."""
    import sys
    from unittest.mock import MagicMock

    mock_pymysql = MagicMock()
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_pymysql.connect = MagicMock(return_value=mock_connection)
    sys.modules["pymysql"] = mock_pymysql

    yield {
        "module": mock_pymysql,
        "connection": mock_connection,
        "cursor": mock_cursor,
        "connect": mock_pymysql.connect,
    }

    # Cleanup: remove from sys.modules if it was added
    if "pymysql" in sys.modules and sys.modules["pymysql"] is mock_pymysql:
        del sys.modules["pymysql"]


@pytest.fixture(scope="function")
def mock_db_connection(mocker):
    """Create a mock database connection (AsyncMock)."""
    from unittest.mock import AsyncMock

    connection = AsyncMock()
    connection.execute = AsyncMock()
    connection.fetch = AsyncMock()
    connection.fetchrow = AsyncMock()
    connection.fetchval = AsyncMock()
    connection.commit = AsyncMock()
    connection.rollback = AsyncMock()
    connection.close = AsyncMock()
    connection.begin = AsyncMock()

    return connection


@pytest.fixture(scope="function")
def mock_db_cursor(mocker):
    """Create a mock database cursor (AsyncMock) for MySQL/PostgreSQL adapters."""
    from unittest.mock import AsyncMock, MagicMock

    cursor = AsyncMock()
    cursor.execute = AsyncMock()
    cursor.fetchall = AsyncMock(return_value=[])
    cursor.fetchone = AsyncMock(return_value=None)
    cursor.fetchmany = AsyncMock(return_value=[])
    cursor.description = []
    cursor.rowcount = 0
    cursor.__aenter__ = AsyncMock(return_value=cursor)
    cursor.__aexit__ = AsyncMock(return_value=None)
    # For pymysql (synchronous)
    cursor.__enter__ = MagicMock(return_value=cursor)
    cursor.__exit__ = MagicMock(return_value=None)

    return cursor


@pytest.fixture(scope="function")
def mock_app_url(mocker):
    """Create a mock app URL for integration tests."""
    return "https://example.com/app"


@pytest.fixture(scope="function")
def mock_httpx_response_basic(mocker):
    """Create a basic mock httpx.Response for API tests."""
    from datetime import timedelta

    from httpx import Response

    response = mocker.MagicMock(spec=Response)
    response.status_code = 200
    response.elapsed = timedelta(seconds=0.5)
    response.is_informational = False
    response.is_success = True
    response.is_redirect = False
    response.is_client_error = False
    response.is_server_error = False
    response.content = b'{"status": "ok"}'
    response.headers = {"Content-Type": "application/json"}
    response.reason_phrase = "OK"
    response.json = mocker.MagicMock(return_value={"status": "ok"})

    return response


@pytest.fixture(scope="function")
def mock_playwright_browser_and_page(mocker):
    """Create mock Playwright browser and page for integration tests."""
    from unittest.mock import AsyncMock

    mock_browser = AsyncMock()
    mock_page = AsyncMock()
    mock_page.click = AsyncMock()
    mock_page.fill = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()
    mock_page.screenshot = AsyncMock()
    mock_page.evaluate = AsyncMock()
    mock_page.locator = AsyncMock()
    mock_page.title = AsyncMock(return_value="Test Page")
    mock_page.url = "https://example.com/app"
    mock_browser.new_page = AsyncMock(return_value=mock_page)

    mock_playwright = mocker.patch("py_web_automation.clients.ui_client.async_playwright")
    mock_playwright_instance = AsyncMock()
    mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
    mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)

    return {
        "browser": mock_browser,
        "page": mock_page,
        "playwright": mock_playwright,
        "playwright_instance": mock_playwright_instance,
    }


@pytest.fixture(scope="function")
def mock_httpx_response_elapsed_error(mocker):
    """Create a mock httpx.Response where elapsed raises AttributeError."""
    from httpx import Response

    mock_response = mocker.MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.is_informational = False
    mock_response.is_success = True
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"test": "data"}'
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.reason_phrase = "OK"

    # Create a mock elapsed object that raises AttributeError when total_seconds() is called
    mock_elapsed = mocker.MagicMock()
    mock_elapsed.total_seconds = mocker.Mock(side_effect=AttributeError("elapsed not available"))
    # Make elapsed property return the mock that raises error
    type(mock_response).elapsed = mocker.PropertyMock(return_value=mock_elapsed)

    return mock_response

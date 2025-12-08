"""
Global test configuration and fixtures for Web Automation Framework tests.
"""

from re import match
from datetime import timedelta
from httpx import Response
from sys import platform, modules
from asyncio import get_event_loop_policy
from time import perf_counter
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, LogRecord, getLogger
from tempfile import TemporaryDirectory
from tracemalloc import start, take_snapshot, is_tracing
from pytest import fixture, hookimpl, mark, fail
from loguru import logger



from fixtures.api_client import (
    api_client_with_config,
    mock_graphql_execute_operation,
    mock_httpx_client,
    mock_httpx_response_101,
    mock_httpx_response_200,
    mock_httpx_response_301,
    mock_httpx_response_404,
    mock_httpx_response_500,
    valid_config,
)
from fixtures.config import (
    config_data_for_both_session_methods,
    config_data_for_empty_strings,
    config_data_for_float_precision,
    config_data_for_invalid_log_level,
    config_data_for_invalid_retry_count,
    config_data_for_invalid_retry_delay,
    config_data_for_large_numbers,
    config_data_for_log_level_case_sensitivity,
    config_data_for_log_level_critical,
    config_data_for_log_level_debug,
    config_data_for_log_level_error,
    config_data_for_log_level_info,
    config_data_for_log_level_warning,
    config_data_for_missing_session,
    config_data_for_none_values,
    config_data_for_special_characters,
    config_data_for_unicode_characters,
    config_data_for_very_long_strings,
    config_data_for_whitespace_strings,
    invalid_config_data_maximal_retry_count,
    invalid_config_data_maximal_retry_delay,
    invalid_config_data_minimal_retry_count,
    invalid_config_data_minimal_retry_delay,
    invalid_config_data_timeout,
    mock_environment,
    mock_environment_default_values,
    mock_environment_optional_variables,
    mock_environment_override_defaults,
    valid_config_data,
    valid_config_data_maximal,
    valid_config_data_minimal,
    valid_config_with_file_data,
    yaml_config_data_minimal,
    yaml_config_data_valid,
    yaml_config_file_empty,
    yaml_config_file_invalid,
    yaml_config_file_invalid_format,
    yaml_config_file_minimal,
    yaml_config_file_missing_session,
    yaml_config_file_valid,
    yaml_config_file_with_file_session,
    yaml_config_file_with_mini_app,
)
# All fixtures from data_fixtures.py have been removed as they were not used in tests
from fixtures.streaming_client import mock_websocket_connection
from fixtures.metrics import metrics
from fixtures.middleware import (
    metrics_for_middleware,
    middleware_chain,
    request_context,
    response_context,
)
from fixtures.rate_limit import (
    rate_limiter,
    rate_limiter_short_window,
    rate_limiter_single,
)
from fixtures.ui_client import (
    mock_browser,
    mock_page,
    ui_client_with_browser,
    ui_client_with_config,
)


def loguru_sink(message):
    """Sink that redirects loguru logs to standard logging for caplog."""
    level_map = {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL,
    }
    record = message.record
    log_level = level_map.get(record["level"].name, INFO)
    logger_name = record.get("name", "loguru")
    log_record = LogRecord(
        name=logger_name,
        level=log_level,
        pathname=str(record.get("file", {}).path) if hasattr(record.get("file", None), "path") else "",
        lineno=record.get("line", 0),
        msg=str(record["message"]),
        args=(),
        exc_info=record.get("exception"),
    )
    std_logger = getLogger(logger_name)
    std_logger.handle(log_record)


logger.remove()
logger.add(loguru_sink, format="{message}", serialize=False)


# ============================================================================
# pytest-resource-usage: Auto-apply memory tracking markers to all tests
# ============================================================================


def pytest_collection_modifyitems(config, items):
    """
    Automatically apply pytest-resource-usage markers to all test items.

    This hook applies memory tracking markers to all tests:
    - report_duration: Track test execution time
    - report_tracemalloc: Track memory allocations (standard library)
    - report_uss: Track unique set size (requires psutil, lower overhead)
      NOTE: report_uss is disabled on Windows and with pytest-xdist due to
      multiprocessing compatibility issues (RLock pickle errors).
    - limit_memory("500MB"): Fail test if memory exceeds 500MB
      NOTE: Automatically applied to all tests. Individual tests can override
      by adding their own limit_memory marker with different limit.
      Works correctly with pytest-xdist as each worker process tracks memory independently.

    Args:
        config: Pytest configuration object
        items: List of test items collected by pytest
    """
    # Check if pytest-xdist is active (parallel execution)
    # xdist is active if plugin is loaded and numprocesses option is set
    is_xdist_active = (
        config.pluginmanager.hasplugin("xdist")
        and config.getoption("numprocesses", default=None) is not None
    )
    # Check if running on Windows
    is_windows = platform == "win32"
    # Base markers that work everywhere
    resource_markers = [
        mark.report_duration,
        mark.report_tracemalloc,
    ]
    # report_uss uses multiprocessing which has issues on Windows and with pytest-xdist
    # It causes "TypeError: cannot pickle '_thread.RLock' object" errors
    # On Windows, multiprocessing uses spawn method which requires pickle serialization
    # RLock objects (from threading) cannot be pickled, causing failures
    # Only enable report_uss on non-Windows platforms and when not using xdist
    if not is_windows and not is_xdist_active:
        resource_markers.append(mark.report_uss)
    for item in items:
        for marker in resource_markers:
            if marker.name not in [m.name for m in item.iter_markers()]:
                item.add_marker(marker)
        if "limit_memory" not in [m.name for m in item.iter_markers()]:
            item.add_marker(mark.limit_memory("300MB"))


# ============================================================================
# Custom memory limit enforcement (Windows-compatible alternative to pytest-memray)
# ============================================================================


def _parse_memory_limit(limit_str: str) -> int:
    """
    Parse memory limit string to bytes.

    Supports formats: "100MB", "50KB", "1GB", "500B", etc.

    Args:
        limit_str: Memory limit string (e.g., "100MB", "50KB")

    Returns:
        Memory limit in bytes

    Raises:
        ValueError: If limit string format is invalid
    """
    limit_str = limit_str.strip().upper()
    # Match pattern: number + optional unit (B, KB, MB, GB, TB, PB)
    _match = match(r"^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$", limit_str)
    if not _match:
        raise ValueError(f"Invalid memory limit format: {limit_str}. Use format like '100MB', '50KB'")
    value = float(_match.group(1))
    unit = _match.group(2) or "B"
    multipliers = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
        "TB": 1024**4,
        "PB": 1024**5,
    }
    if unit not in multipliers:
        raise ValueError(f"Invalid memory unit: {unit}. Use B, KB, MB, GB, TB, or PB")
    return int(value * multipliers[unit])


@hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    Setup memory tracking for tests with limit_memory marker.

    Starts tracemalloc tracking if test has limit_memory marker.
    Works correctly with pytest-xdist as each worker process has its own tracemalloc state.

    Args:
        item: Test item (pytest.Item)
    """
    limit_marker = item.get_closest_marker("limit_memory")
    if limit_marker:
        # Start tracemalloc if not already started
        # Each worker process in xdist has its own tracemalloc state, so this works correctly
        if not is_tracing():
            start()
        # Store snapshot at test start
        # This snapshot is process-local and works correctly with xdist
        item._memory_start_snapshot = take_snapshot()


@hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """
    Check memory limit and fail test if exceeded.

    Compares peak memory usage against limit_memory marker threshold.
    Works correctly with pytest-xdist as each worker process tracks its own memory independently.

    Args:
        item: Test item (pytest.Item)
        nextitem: Next test item (pytest.Item | None)
    """
    limit_marker = item.get_closest_marker("limit_memory")
    if not limit_marker:
        return
    if not is_tracing():
        # tracemalloc might have been stopped or not started
        # This can happen if test failed before setup completed
        return
    # Get memory limit from marker
    limit_str = limit_marker.args[0] if limit_marker.args else None
    if not limit_str:
        # Try to get from marker.kwargs if passed as keyword
        limit_str = limit_marker.kwargs.get("size", None)
    if not limit_str:
        fail("limit_memory marker requires memory limit (e.g., '100MB')")
    try:
        memory_limit_bytes = _parse_memory_limit(limit_str)
    except ValueError as e:
        fail(f"Invalid memory limit format: {e}")
    # Take snapshot at test end
    end_snapshot = take_snapshot()
    # Calculate peak memory (difference between start and end)
    if hasattr(item, "_memory_start_snapshot"):
        start_snapshot = item._memory_start_snapshot
        # Get statistics and calculate peak
        stats = end_snapshot.compare_to(start_snapshot, "lineno")
        peak_memory = sum(stat.size_diff for stat in stats if stat.size_diff > 0)
    else:
        # Fallback: use current snapshot statistics
        stats = end_snapshot.statistics("lineno")
        peak_memory = sum(stat.size for stat in stats)

    # Format memory for error message
    def format_bytes(bytes_val: int) -> str:
        """Format bytes to human-readable format."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f}{unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f}TB"

    # Store memory usage info for reporting (before potential fail)
    item._memory_usage_bytes = peak_memory
    item._memory_limit_bytes = memory_limit_bytes
    item._memory_exceeded = peak_memory > memory_limit_bytes
    
    # Store in global set for terminal summary filtering
    if peak_memory > memory_limit_bytes:
        _memory_exceeded_tests.add(item.nodeid)

    # Fail test if memory limit exceeded
    if peak_memory > memory_limit_bytes:
        fail(
            f"Test exceeded memory limit: allocated {format_bytes(peak_memory)}, "
            f"limit was {format_bytes(memory_limit_bytes)} "
            f"({format_bytes(peak_memory - memory_limit_bytes)} over limit)"
        )


# Store test items that exceeded memory limits for filtering
_memory_exceeded_tests: set[str] = set()


@hookimpl(trylast=True)
def pytest_runtest_logreport(report):
    """
    Track tests that exceeded memory limits and filter resource usage output.

    This hook tracks which tests exceeded their memory limits and filters
    resource usage sections in report.sections to show only tests that exceeded limits.

    Args:
        report: Test report object from pytest
    """
    # Only track call phase reports
    if report.when != "call":
        return

    # Check if this test exceeded memory limit
    test_item = getattr(report, "item", None)
    memory_exceeded = False
    if test_item and hasattr(test_item, "_memory_exceeded"):
        if test_item._memory_exceeded:
            memory_exceeded = True
            # Store test nodeid for filtering
            _memory_exceeded_tests.add(test_item.nodeid)

    # Filter resource usage sections in report.sections
    # pytest-resource-usage may add sections to report.sections
    if hasattr(report, "sections") and report.sections:
        config = getattr(report, "config", None)
        if config:
            filter_enabled = config.getoption("--filter-resource-usage", default=True)
            if filter_enabled:
                filtered_sections = []
                for header, content in report.sections:
                    # Check if this is a resource usage section
                    if "resource usage" in header.lower() or "peak allocated memory" in header.lower() or "running time" in header.lower():
                        # Only include if this test exceeded memory limit
                        if memory_exceeded:
                            filtered_sections.append((header, content))
                        # Otherwise, skip this section
                    else:
                        # Keep non-resource-usage sections
                        filtered_sections.append((header, content))
                report.sections = filtered_sections


@hookimpl(trylast=True, hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Filter pytest-resource-usage output AFTER it has been added.

    This wrapper hook runs after pytest-resource-usage adds its sections,
    then filters them to show only tests that exceeded memory limits.

    Can be controlled via command-line option `--no-filter-resource-usage` to disable.

    Args:
        terminalreporter: Terminal reporter object
        exitstatus: Exit status code
        config: Pytest configuration object
    """
    # Let pytest-resource-usage and other plugins add their sections first
    yield
    
    # Check if filtering is enabled (default: true)
    filter_enabled = config.getoption("--filter-resource-usage", default=True)
    if not filter_enabled:
        return

    # Filter sections that contain resource usage info
    # pytest-resource-usage stores sections in terminalreporter._tw.sections
    if hasattr(terminalreporter, "_tw"):
        # Get sections from terminal writer
        tw_sections = getattr(terminalreporter._tw, "sections", [])
        if tw_sections:
            filtered_sections = []
            for header, content in tw_sections:
                # Check if this is a resource usage section
                if "resource usage" in header.lower():
                    # Only include lines for tests that exceeded memory limits
                    if isinstance(content, str):
                        lines = content.split("\n")
                        filtered_lines = []
                        for line in lines:
                            # Skip empty lines and header separators
                            stripped_line = line.strip()
                            if not stripped_line or stripped_line.startswith("="):
                                # Keep separators only if we have filtered lines
                                if filtered_lines:
                                    filtered_lines.append(line)
                                continue
                            # Check if line contains a test nodeid that exceeded memory
                            line_included = False
                            if _memory_exceeded_tests:
                                for test_nodeid in _memory_exceeded_tests:
                                    if test_nodeid in line:
                                        filtered_lines.append(line)
                                        line_included = True
                                        break
                        # Only add section if there are filtered lines
                        if filtered_lines:
                            filtered_sections.append((header, "\n".join(filtered_lines)))
                        # If no tests exceeded, don't add the section at all
                    else:
                        # Non-string content - keep as is (shouldn't happen for resource usage)
                        filtered_sections.append((header, content))
                else:
                    # Keep non-resource-usage sections
                    filtered_sections.append((header, content))
            # Replace sections with filtered version
            terminalreporter._tw.sections = filtered_sections
        
        # Also check terminalreporter.stats for resource usage stats
        if hasattr(terminalreporter, "stats") and "resource usage" in terminalreporter.stats:
            resource_stats = terminalreporter.stats.get("resource usage", [])
            if resource_stats and _memory_exceeded_tests:
                # Filter stats to only include tests that exceeded memory
                filtered_stats = [
                    stat
                    for stat in resource_stats
                    if hasattr(stat, "nodeid") and stat.nodeid in _memory_exceeded_tests
                ]
                terminalreporter.stats["resource usage"] = filtered_stats
            elif not _memory_exceeded_tests:
                # If no tests exceeded, remove resource usage stats
                terminalreporter.stats.pop("resource usage", None)


def pytest_addoption(parser):
    """
    Add command-line option to control resource usage filtering.

    Args:
        parser: Pytest argument parser
    """
    group = parser.getgroup("resource-usage-filtering", "Resource usage filtering options")
    group.addoption(
        "--filter-resource-usage",
        action="store_true",
        default=True,
        help="Filter pytest-resource-usage output to show only tests exceeding memory limits (default: True)",
    )
    group.addoption(
        "--no-filter-resource-usage",
        action="store_false",
        dest="filter_resource_usage",
        help="Show all resource usage information (disable filtering)",
    )


@fixture(scope="function")
def event_loop():
    """
    Create an instance of the default event loop for the test.

    Changed scope from "session" to "function" for better compatibility
    with pytest-xdist parallel execution. Each worker needs its own event loop.
    """
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@fixture
def mock_http_client(mocker):
    """Create a mock HTTP client."""
    client = mocker.AsyncMock()
    client.get = mocker.AsyncMock()
    client.post = mocker.AsyncMock()
    client.put = mocker.AsyncMock()
    client.delete = mocker.AsyncMock()
    return client


@fixture
def mock_playwright_browser(mocker):
    """Create a mock Playwright browser."""
    browser = mocker.AsyncMock()
    browser.close = mocker.AsyncMock()
    browser.new_page = mocker.AsyncMock()
    return browser


@fixture
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


@fixture
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
@fixture
async def async_mock(mocker):
    """Create an async mock."""
    return mocker.AsyncMock()


# Error simulation fixtures
@fixture
def mock_connection_error():
    """Mock connection error."""
    return ConnectionError("Connection failed")


@fixture
def mock_timeout_error():
    """Mock timeout error."""
    return TimeoutError("Operation timed out")


# Performance testing fixtures
@fixture
def performance_timer():
    """Timer for performance testing."""
    start_time = perf_counter()
    yield lambda: perf_counter() - start_time


# ============================================================================
# Database Mock Fixtures (scope=function for isolation)
# ============================================================================


@fixture(scope="function")
def mock_asyncpg_module(mocker):
    """Create a mock asyncpg module for sys.modules."""
    mock_asyncpg = mocker.MagicMock()
    mock_connection = mocker.AsyncMock()
    mock_connect = mocker.AsyncMock(return_value=mock_connection)
    mock_asyncpg.connect = mock_connect
    mocker.patch.dict(modules, {"asyncpg": mock_asyncpg})
    yield {
        "module": mock_asyncpg,
        "connection": mock_connection,
        "connect": mock_connect,
    }
    # Cleanup: remove from sys.modules if it was added
    if "asyncpg" in modules and modules["asyncpg"] is mock_asyncpg:
        del modules["asyncpg"]


@fixture(scope="function")
def mock_psycopg_module(mocker):
    """Create a mock psycopg module for sys.modules."""
    mock_psycopg = mocker.MagicMock()
    mock_connection = mocker.AsyncMock()
    mock_connect = mocker.AsyncMock(return_value=mock_connection)
    # psycopg uses AsyncConnection.connect pattern
    mock_async_connection = mocker.MagicMock()
    mock_async_connection.connect = mock_connect
    mock_psycopg.AsyncConnection = mock_async_connection
    mocker.patch.dict(modules, {"psycopg": mock_psycopg})
    yield {
        "module": mock_psycopg,
        "connection": mock_connection,
        "connect": mock_connect,
        "AsyncConnection": mock_async_connection,
    }
    # Cleanup: remove from sys.modules if it was added
    if "psycopg" in modules and modules["psycopg"] is mock_psycopg:
        del modules["psycopg"]


@fixture(scope="function")
def mock_aiomysql_module(mocker):
    """Create a mock aiomysql module for sys.modules."""
    mock_aiomysql = mocker.MagicMock()
    mock_connection = mocker.AsyncMock()
    mock_connect = mocker.AsyncMock(return_value=mock_connection)
    mock_aiomysql.connect = mock_connect
    mock_aiomysql.DictCursor = mocker.MagicMock()
    mocker.patch.dict(modules, {"aiomysql": mock_aiomysql})
    yield {
        "module": mock_aiomysql,
        "connection": mock_connection,
        "connect": mock_connect,
        "DictCursor": mock_aiomysql.DictCursor,
    }
    # Cleanup: remove from sys.modules if it was added
    if "aiomysql" in modules and modules["aiomysql"] is mock_aiomysql:
        del modules["aiomysql"]


@fixture(scope="function")
def mock_pymysql_module(mocker):
    """Create a mock pymysql module for sys.modules."""
    mock_pymysql = mocker.MagicMock()
    mock_connection = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_pymysql.connect = mocker.AsyncMock(return_value=mock_connection)
    mocker.patch.dict(modules, {"pymysql": mock_pymysql})
    yield {
        "module": mock_pymysql,
        "connection": mock_connection,
        "cursor": mock_cursor,
        "connect": mock_pymysql.connect,
    }
    # Cleanup: remove from sys.modules if it was added
    if "pymysql" in modules and modules["pymysql"] is mock_pymysql:
        del modules["pymysql"]


@fixture(scope="function")
def mock_db_connection(mocker):
    """Create a mock database connection (AsyncMock)."""
    connection = mocker.AsyncMock()
    connection.execute = mocker.AsyncMock()
    connection.fetch = mocker.AsyncMock()
    connection.fetchrow = mocker.AsyncMock()
    connection.fetchval = mocker.AsyncMock()
    connection.commit = mocker.AsyncMock()
    connection.rollback = mocker.AsyncMock()
    connection.close = mocker.AsyncMock()
    connection.begin = mocker.AsyncMock()
    return connection


@fixture(scope="function")
def mock_db_cursor(mocker):
    """Create a mock database cursor (AsyncMock) for MySQL/PostgreSQL adapters."""
    cursor = mocker.AsyncMock()
    cursor.execute = mocker.AsyncMock()
    cursor.fetchall = mocker.AsyncMock(return_value=[])
    cursor.fetchone = mocker.AsyncMock(return_value=None)
    cursor.fetchmany = mocker.AsyncMock(return_value=[])
    cursor.description = []
    cursor.rowcount = 0
    cursor.__aenter__ = mocker.AsyncMock(return_value=cursor)
    cursor.__aexit__ = mocker.AsyncMock(return_value=None)
    # For pymysql (synchronous)
    cursor.__enter__ = mocker.MagicMock(return_value=cursor)
    cursor.__exit__ = mocker.MagicMock(return_value=None)
    return cursor


@fixture(scope="function")
def mock_app_url(mocker):
    """Create a mock app URL for integration tests."""
    return "https://example.com/app"


@fixture(scope="function")
def mock_httpx_response_basic(mocker):
    """Create a basic mock httpx.Response for API tests."""
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


@fixture(scope="function")
def mock_playwright_browser_and_page(mocker):
    """Create mock Playwright browser and page for integration tests."""
    mock_browser = mocker.AsyncMock()
    mock_page = mocker.AsyncMock()
    mock_page.click = mocker.AsyncMock()
    mock_page.fill = mocker.AsyncMock()
    mock_page.goto = mocker.AsyncMock()
    mock_page.wait_for_selector = mocker.AsyncMock()
    mock_page.screenshot = mocker.AsyncMock()
    mock_page.evaluate = mocker.AsyncMock()
    mock_page.locator = mocker.AsyncMock()
    mock_page.title = mocker.AsyncMock(return_value="Test Page")
    mock_page.url = "https://example.com/app"
    mock_browser.new_page = mocker.AsyncMock(return_value=mock_page)
    mock_playwright = mocker.patch("py_web_automation.clients.ui_client.async_playwright")
    mock_playwright_instance = mocker.AsyncMock()
    mock_playwright_instance.chromium.launch = mocker.AsyncMock(return_value=mock_browser)
    mock_playwright.return_value.start = mocker.AsyncMock(return_value=mock_playwright_instance)
    return {
        "browser": mock_browser,
        "page": mock_page,
        "playwright": mock_playwright,
        "playwright_instance": mock_playwright_instance,
    }


@fixture(scope="function")
def mock_httpx_response_elapsed_error(mocker):
    """Create a mock httpx.Response where elapsed raises AttributeError."""
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
    mock_elapsed = mocker.MagicMock()
    mock_elapsed.total_seconds = mocker.Mock(side_effect=AttributeError("elapsed not available"))
    mock_response.elapsed = mock_elapsed
    return mock_response

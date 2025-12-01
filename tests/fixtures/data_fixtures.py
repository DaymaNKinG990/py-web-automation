"""
Pytest fixtures for test data.
"""

# Python imports
import pytest

from py_web_automation.clients.models import ApiResult

# Local imports
from py_web_automation.config import Config
from tests.data.constants import (  # type: ignore[import-untyped]
    AUTHENTICATION_ERROR,
    BOT_ERROR_RESPONSE,
    BOT_HELP_RESPONSE,
    BOT_START_RESPONSE,
    CONNECTION_ERROR,
    ERROR_API_RESULT_DATA,
    INVALID_ENV_VARS,
    INVALID_SESSION_STRING,
    MINI_APP_API_ENDPOINTS,
    MINI_APP_HTML_CONTENT,
    MISSING_ENV_VARS,
    NETWORK_ERROR,
    PERFORMANCE_TEST_DATA,
    TIMEOUT_API_RESULT_DATA,
    TIMEOUT_ERROR,
    UNKNOWN_ERROR,
    VALID_ENV_VARS,
    VALID_SESSION_STRING,
    VALIDATION_ERROR,
)

# Module-level constants for dynamic factories
# These are defined at module level so dynamic factories can reference them directly
VALID_CONFIG_DATA = {
    "base_url": "https://example.com",
    "timeout": 30,
    "retry_count": 3,
    "retry_delay": 1.0,
    "log_level": "INFO",
    "browser_headless": True,
    "browser_timeout": 30000,
}

VALID_USER_INFO_DATA = {
    "id": 123456789,
    "first_name": "Test User",
    "username": "test_user",
    "last_name": "Test",
    "phone": "+1234567890",
    "is_bot": False,
    "is_verified": True,
    "is_premium": False,
}

VALID_CHAT_INFO_DATA = {
    "id": 987654321,
    "title": "Test Chat",
    "type": "group",
    "username": "test_chat",
    "is_bot": False,
    "is_verified": False,
}

VALID_MESSAGE_INFO_DATA = {
    "id": 111222333,
    "chat": None,  # Will be set in fixtures
    "date": "2023-10-20T10:00:00Z",
    "text": "Test message",
    "from_user": None,  # Will be set in fixtures
    "reply_to": None,
    "media": None,
}

VALID_MINI_APP_INFO_DATA = {
    "url": "https://example.com/mini-app",
    "start_param": "test_param",
    "theme_params": {"bg_color": "#ffffff", "text_color": "#000000"},
    "platform": "web",
}

VALID_API_RESULT_DATA = {
    "endpoint": "/api/status",
    "method": "GET",
    "status_code": 200,
    "response_time": 0.5,
    "success": True,
    "redirect": False,
    "client_error": False,
    "server_error": False,
    "informational": False,
    "headers": {"content-type": "application/json"},
    "body": b'{"status": "ok"}',
    "content_type": "application/json",
    "reason": "OK",
    "error_message": None,
}


# User info fixtures
@pytest.fixture
def valid_user_info_data() -> dict[str, int | str | bool]:
    """
    Valid user info data.

    Returns:
        dict[str, int | str | bool]: Valid user info data.
    """
    return {
        "id": 123456789,
        "first_name": "Test User",
        "username": "test_user",
        "last_name": "Test",
        "phone": "+1234567890",
        "is_bot": False,
        "is_verified": True,
        "is_premium": False,
    }


@pytest.fixture
def bot_user_info_data() -> dict[str, int | str | bool]:
    """
    Bot user info data.

    Returns:
        dict[str, int | str | bool]: Bot user info data.
    """
    return {
        "id": 987654321,
        "first_name": "Test Bot",
        "username": "test_bot",
        "last_name": None,
        "phone": None,
        "is_bot": True,
        "is_verified": False,
        "is_premium": False,
    }


@pytest.fixture
def minimal_user_info_data() -> dict[str, int | str | bool]:
    """
    Minimal user info data.

    Returns:
        dict[str, int | str | bool]: Minimal user info data.
    """
    return {
        "id": 111222333,
        "first_name": "Minimal User",
        "username": None,
        "last_name": None,
        "phone": None,
        "is_bot": False,
        "is_verified": False,
        "is_premium": False,
    }


@pytest.fixture
def edge_case_user_info_data():
    """Edge case user info data."""
    return {
        "id": 0,  # Edge case: minimum ID
        "first_name": "",  # Edge case: empty first name
        "username": "a" * 100,  # Edge case: very long username
        "last_name": "b" * 100,  # Edge case: very long last name
        "phone": "+12345678901234567890",  # Edge case: very long phone
        "is_bot": False,
        "is_verified": False,
        "is_premium": False,
    }


@pytest.fixture
def unicode_user_info_data():
    """Unicode user info data."""
    return {
        "id": 123456789,
        "first_name": "Тест Пользователь",  # Cyrillic
        "username": "test_用户",  # Mixed Latin and Chinese
        "last_name": "テスト",  # Japanese
        "phone": "+1234567890",
        "is_bot": False,
        "is_verified": True,
        "is_premium": False,
    }


# User info object fixtures (returning dicts since UserInfo class doesn't exist)
@pytest.fixture
def valid_user_info(valid_user_info_data) -> dict:
    """
    Valid user info data (as dict).

    Returns:
        dict: Valid user info data.
    """
    return valid_user_info_data.copy()


@pytest.fixture
def unicode_user_info(unicode_user_info_data) -> dict:
    """
    Unicode user info data (as dict).

    Returns:
        dict: Unicode user info data.
    """
    return unicode_user_info_data.copy()


# Chat info fixtures
@pytest.fixture
def valid_chat_info_data() -> dict[str, int | str | bool]:
    """
    Valid chat info data.

    Returns:
        dict[str, int | str | bool]: Valid chat info data.
    """
    return {
        "id": 987654321,
        "title": "Test Chat",
        "type": "group",
        "username": "test_chat",
        "is_bot": False,
        "is_verified": False,
    }


@pytest.fixture
def private_chat_info_data() -> dict[str, int | str | bool]:
    """
    Private chat info data.

    Returns:
        dict[str, int | str | bool]: Private chat info data.
    """
    return {
        "id": 111222333,
        "title": "Private Chat",
        "type": "private",
        "username": None,
        "is_bot": False,
        "is_verified": False,
    }


@pytest.fixture
def channel_chat_info_data() -> dict[str, int | str | bool]:
    """
    Channel chat info data.

    Returns:
        dict[str, int | str | bool]: Channel chat info data.
    """
    return {
        "id": 444555666,
        "title": "Test Channel",
        "type": "channel",
        "username": "test_channel",
        "is_bot": False,
        "is_verified": True,
    }


# Chat info object fixtures (returning dicts since ChatInfo class doesn't exist)
@pytest.fixture
def valid_chat_info(valid_chat_info_data) -> dict:
    """
    Valid chat info data (as dict).

    Returns:
        dict: Valid chat info data.
    """
    return valid_chat_info_data.copy()


# Message info fixtures
@pytest.fixture
def valid_message_info_data(valid_chat_info_data, valid_user_info_data):
    """Valid message info data with chat and user."""
    data = {
        "id": 111222333,
        "chat": None,  # Will be set below
        "date": "2023-10-20T10:00:00Z",
        "text": "Test message",
        "from_user": None,  # Will be set below
        "reply_to": None,
        "media": None,
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = valid_user_info_data
    return data


@pytest.fixture
def reply_message_info_data(valid_chat_info_data, valid_user_info_data):
    """Reply message info data with chat and user."""
    data = {
        "id": 222333444,
        "chat": None,  # Will be set below
        "date": "2023-10-20T10:01:00Z",
        "text": "Reply message",
        "from_user": None,  # Will be set below
        "reply_to": 111222333,
        "media": None,
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = valid_user_info_data
    return data


@pytest.fixture
def media_message_info_data(valid_chat_info_data, valid_user_info_data):
    """Media message info data with chat and user."""
    data = {
        "id": 333444555,
        "chat": None,  # Will be set below
        "date": "2023-10-20T10:02:00Z",
        "text": "Message with media",
        "from_user": None,  # Will be set below
        "reply_to": None,
        "media": {
            "type": "photo",
            "url": "https://example.com/photo.jpg",
            "size": 1024,
        },
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = valid_user_info_data
    return data


@pytest.fixture
def edge_case_message_info_data(valid_chat_info_data, valid_user_info_data):
    """Edge case message info data with chat and user."""
    data = {
        "id": 0,  # Edge case: minimum ID
        "chat": None,  # Will be set below
        "date": "1970-01-01T00:00:00Z",  # Edge case: epoch time
        "text": "a" * 10000,  # Edge case: very long text
        "from_user": None,  # Will be set below
        "reply_to": None,
        "media": None,
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = valid_user_info_data
    return data


@pytest.fixture
def unicode_message_info_data(valid_chat_info_data, unicode_user_info_data):
    """Unicode message info data with chat and user."""
    data = {
        "id": 111222333,
        "chat": None,  # Will be set below
        "date": "2023-10-20T10:00:00Z",
        "text": "Hello 世界! Привет мир! こんにちは世界!",  # Mixed languages
        "from_user": None,  # Will be set below
        "reply_to": None,
        "media": None,
    }
    data["chat"] = valid_chat_info_data
    data["from_user"] = unicode_user_info_data
    return data


@pytest.fixture
def valid_message_info(valid_chat_info, valid_user_info):
    """Valid message info data (as dict)."""
    data = {
        "id": 111222333,
        "chat": valid_chat_info,
        "date": "2023-10-20T10:00:00Z",
        "text": "Test message",
        "from_user": valid_user_info,
        "reply_to": None,
        "media": None,
    }
    return data


@pytest.fixture
def reply_message_info(valid_chat_info, valid_user_info):
    """Reply message info data (as dict)."""
    data = {
        "id": 222333444,
        "chat": valid_chat_info,
        "date": "2023-10-20T10:01:00Z",
        "text": "Reply message",
        "from_user": valid_user_info,
        "reply_to": 111222333,
        "media": None,
    }
    return data


@pytest.fixture
def media_message_info(valid_chat_info, valid_user_info):
    """Media message info data (as dict)."""
    data = {
        "id": 333444555,
        "chat": valid_chat_info,
        "date": "2023-10-20T10:02:00Z",
        "text": "Message with media",
        "from_user": valid_user_info,
        "reply_to": None,
        "media": {
            "type": "photo",
            "url": "https://example.com/photo.jpg",
            "size": 1024,
        },
    }
    return data


@pytest.fixture
def edge_case_message_info(valid_chat_info, valid_user_info):
    """Edge case message info data (as dict)."""
    data = {
        "id": 0,  # Edge case: minimum ID
        "chat": valid_chat_info,
        "date": "1970-01-01T00:00:00Z",  # Edge case: epoch time
        "text": "a" * 10000,  # Edge case: very long text
        "from_user": valid_user_info,
        "reply_to": None,
        "media": None,
    }
    return data


@pytest.fixture
def unicode_message_info(valid_chat_info, unicode_user_info):
    """Unicode message info data (as dict)."""
    data = {
        "id": 111222333,
        "chat": valid_chat_info,
        "date": "2023-10-20T10:00:00Z",
        "text": "Hello 世界! Привет мир! こんにちは世界!",  # Mixed languages
        "from_user": unicode_user_info,
        "reply_to": None,
        "media": None,
    }
    return data


# Mini App info fixtures
@pytest.fixture
def valid_mini_app_info_data():
    """Valid mini app info data."""
    return {
        "url": "https://example.com/mini-app",
        "title": "Test Mini App",
        "description": "Test Mini App Description",
        "platform": "web",
    }


@pytest.fixture
def mobile_mini_app_info_data():
    """Mobile mini app info data."""
    return {
        "url": "https://example.com/mobile-mini-app",
        "title": "Mobile Mini App",
        "description": "Mobile Mini App Description",
        "platform": "mobile",
    }


@pytest.fixture
def valid_mini_app_info(valid_mini_app_info_data):
    """Valid mini app info data (as dict)."""
    return valid_mini_app_info_data.copy()


@pytest.fixture
def mobile_mini_app_info(mobile_mini_app_info_data):
    """Mobile mini app info data (as dict)."""
    return mobile_mini_app_info_data.copy()


# API result fixtures
@pytest.fixture
def valid_api_result_data():
    """Valid API result data."""
    return VALID_API_RESULT_DATA.copy()


@pytest.fixture
def error_api_result_data():
    """Error API result data."""
    return ERROR_API_RESULT_DATA.copy()


@pytest.fixture
def timeout_api_result_data():
    """Timeout API result data."""
    return TIMEOUT_API_RESULT_DATA.copy()


@pytest.fixture
def valid_api_result(valid_api_result_data):
    """Valid ApiResult instance."""
    return ApiResult(**valid_api_result_data)


@pytest.fixture
def error_api_result(error_api_result_data):
    """Error ApiResult instance."""
    return ApiResult(**error_api_result_data)


@pytest.fixture
def timeout_api_result(timeout_api_result_data):
    """Timeout ApiResult instance."""
    return ApiResult(**timeout_api_result_data)


# Config fixtures
@pytest.fixture
def valid_config_data() -> dict:
    """
    Valid config data.

    Returns:
        dict: Valid config data.
    """
    return VALID_CONFIG_DATA.copy()


@pytest.fixture
def valid_config(valid_config_data) -> Config:
    """
    Valid Config instance.

    Returns:
        Config: Valid Config object.
    """
    return Config(**valid_config_data)


# Environment variables fixtures
@pytest.fixture
def valid_env_vars():
    """Valid environment variables."""
    return VALID_ENV_VARS.copy()


@pytest.fixture
def invalid_env_vars():
    """Invalid environment variables."""
    return INVALID_ENV_VARS.copy()


@pytest.fixture
def missing_env_vars():
    """Missing environment variables."""
    return MISSING_ENV_VARS.copy()


# Session fixtures
@pytest.fixture
def valid_session_string():
    """Valid session string."""
    return VALID_SESSION_STRING


@pytest.fixture
def invalid_session_string():
    """Invalid session string."""
    return INVALID_SESSION_STRING


# Bot interaction fixtures
@pytest.fixture
def bot_start_response():
    """Bot start response data."""
    return BOT_START_RESPONSE.copy()


@pytest.fixture
def bot_help_response():
    """Bot help response data."""
    return BOT_HELP_RESPONSE.copy()


@pytest.fixture
def bot_error_response():
    """Bot error response data."""
    return BOT_ERROR_RESPONSE.copy()


# Mini App fixtures
@pytest.fixture
def mini_app_html_content():
    """Mini App HTML content."""
    return MINI_APP_HTML_CONTENT


@pytest.fixture
def mini_app_api_endpoints():
    """Mini App API endpoints data."""
    return MINI_APP_API_ENDPOINTS.copy()


# Error fixtures
@pytest.fixture
def connection_error():
    """Connection error message."""
    return CONNECTION_ERROR


@pytest.fixture
def timeout_error():
    """Timeout error message."""
    return TIMEOUT_ERROR


@pytest.fixture
def authentication_error():
    """Authentication error message."""
    return AUTHENTICATION_ERROR


@pytest.fixture
def validation_error():
    """Validation error message."""
    return VALIDATION_ERROR


@pytest.fixture
def network_error():
    """Network error message."""
    return NETWORK_ERROR


@pytest.fixture
def unknown_error():
    """Unknown error message."""
    return UNKNOWN_ERROR


# Performance fixtures
@pytest.fixture
def performance_test_data():
    """Performance test data."""
    return PERFORMANCE_TEST_DATA.copy()


# Collection fixtures
@pytest.fixture
def user_info_list(valid_user_info):
    """List of UserInfo instances."""
    users = []
    for i in range(5):
        user_data = VALID_USER_INFO_DATA.copy()
        user_data.update(
            {
                "id": 123456789 + i,
                "username": f"test_user_{i}",
                "first_name": f"Test User {i}",
            }
        )
        users.append(user_data)
    return users


@pytest.fixture
def chat_info_list(valid_chat_info):
    """List of ChatInfo instances."""
    chats = []
    for i in range(3):
        chat_data = VALID_CHAT_INFO_DATA.copy()
        chat_data.update(
            {
                "id": 987654321 + i,
                "title": f"Test Chat {i}",
                "username": f"test_chat_{i}",
            }
        )
        chats.append(chat_data)
    return chats


@pytest.fixture
def message_info_list(valid_message_info):
    """List of MessageInfo instances."""
    messages = []
    for i in range(5):
        message_data = VALID_MESSAGE_INFO_DATA.copy()
        message_data.update(
            {
                "id": 111222333 + i,
                "text": f"Test message {i}",
                "date": f"2023-10-20T10:0{i}:00Z",
            }
        )
        # Create chat and user for each message
        chat_data = VALID_CHAT_INFO_DATA.copy()
        chat_data["id"] = 987654321 + i

        user_data = VALID_USER_INFO_DATA.copy()
        user_data["id"] = 123456789 + i

        message_data["chat"] = chat_data
        message_data["from_user"] = user_data
        messages.append(message_data)
    return messages


@pytest.fixture
def api_result_list(valid_api_result):
    """List of ApiResult instances."""
    results = []
    for i in range(5):
        result_data = VALID_API_RESULT_DATA.copy()
        result_data.update(
            {
                "data": {"test": f"data_{i}", "value": i},
                "response_time": 0.1 + (i * 0.1),
            }
        )
        results.append(ApiResult(**result_data))
    return results


# JSON fixtures
@pytest.fixture
def json_test_data(
    valid_user_info_data,
    valid_chat_info_data,
    valid_message_info_data,
    valid_mini_app_info_data,
    valid_api_result_data,
    valid_config_data,
):
    """JSON test data for serialization testing."""
    return {
        "user": valid_user_info_data,
        "chat": valid_chat_info_data,
        "message": valid_message_info_data,
        "mini_app": valid_mini_app_info_data,
        "api_result": valid_api_result_data,
        "config": valid_config_data,
    }


@pytest.fixture
def large_json_test_data(
    valid_user_info_data,
    valid_chat_info_data,
    valid_message_info_data,
    valid_config_data,
):
    """Large JSON test data for performance testing."""
    return {
        "users": [valid_user_info_data for _ in range(100)],
        "chats": [valid_chat_info_data for _ in range(50)],
        "messages": [valid_message_info_data for _ in range(1000)],
        "config": valid_config_data,
    }


# Parametrized fixtures
@pytest.fixture(params=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def valid_log_level(request):
    """Valid log level."""
    return request.param


@pytest.fixture(params=["private", "group", "supergroup", "channel"])
def valid_chat_type(request):
    """Valid chat type."""
    return request.param


@pytest.fixture(params=["web", "mobile", "desktop", "tv"])
def valid_platform(request):
    """Valid platform."""
    return request.param


@pytest.fixture(params=[200, 201, 400, 401, 403, 404, 500, 502, 503])
def valid_status_code(request):
    """Valid HTTP status code."""
    return request.param


# Dynamic fixtures
@pytest.fixture
def config_with_custom_values():
    """Config with custom values."""

    def _create_config(**kwargs):
        base_data = VALID_CONFIG_DATA.copy()
        base_data.update(kwargs)
        return Config(**base_data)

    return _create_config


@pytest.fixture
def user_info_with_custom_values():
    """UserInfo with custom values."""

    def _create_user(**kwargs):
        base_data = VALID_USER_INFO_DATA.copy()
        base_data.update(kwargs)
        return base_data

    return _create_user


@pytest.fixture
def chat_info_with_custom_values():
    """ChatInfo with custom values."""

    def _create_chat(**kwargs):
        base_data = VALID_CHAT_INFO_DATA.copy()
        base_data.update(kwargs)
        return base_data

    return _create_chat


@pytest.fixture
def message_info_with_custom_values(valid_chat_info, valid_user_info):
    """MessageInfo with custom values."""

    def _create_message(**kwargs):
        base_data = VALID_MESSAGE_INFO_DATA.copy()
        base_data.update(kwargs)
        # Convert dict chat/user to objects if needed
        if base_data.get("chat") is None:
            base_data["chat"] = valid_chat_info
        if base_data.get("from_user") is None:
            base_data["from_user"] = valid_user_info
        return base_data

    return _create_message


@pytest.fixture
def app_info_with_custom_values():
    """App info with custom values."""

    def _create_app(**kwargs):
        base_data = VALID_MINI_APP_INFO_DATA.copy()
        base_data.update(kwargs)
        return base_data

    return _create_app


@pytest.fixture
def api_result_with_custom_values():
    """ApiResult with custom values."""

    def _create_api_result(**kwargs):
        base_data = VALID_API_RESULT_DATA.copy()
        base_data.update(kwargs)
        return ApiResult(**base_data)

    return _create_api_result

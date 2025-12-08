# Python imports
import os
from os import environ
from pathlib import Path
from pytest import fixture
from pytest_mock import MockerFixture
from yaml import SafeLoader, load  # type: ignore[import-untyped]


@fixture
def valid_config_data() -> dict[str, int | str | float | bool]:
    """
    Valid configuration data.

    Returns:
        dict[str, int | str | float | bool]: Valid configuration data.
    """
    return {
        "base_url": "https://example.com",
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "log_level": "INFO",
        "browser_headless": True,
        "browser_timeout": 30000,
    }


@fixture
def valid_config_data_minimal() -> dict[str, int | str | float | bool]:
    """
    Valid configuration data minimal.

    Returns:
        dict[str, int | str | float | bool]: Valid configuration data minimal.
    """
    return {
        "timeout": 1,
        "retry_count": 0,
        "retry_delay": 0.1,
    }


@fixture
def valid_config_data_maximal() -> dict[str, int | str | float | bool]:
    """
    Valid configuration data maximal.

    Returns:
        dict[str, int | str | float | bool]: Valid configuration data maximal.
    """
    return {
        "base_url": "https://example.com",
        "timeout": 300,
        "retry_count": 10,
        "retry_delay": 10.0,
        "log_level": "DEBUG",
        "browser_headless": False,
        "browser_timeout": 60000,
    }


@fixture
def valid_config_with_file_data() -> dict[str, int | str | float | bool]:
    """
    Valid configuration data (no session file in new Config).

    Returns:
        dict[str, int | str | float | bool]: Valid configuration data.
    """
    return {
        "base_url": "https://example.com",
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "log_level": "DEBUG",
        "browser_headless": True,
        "browser_timeout": 30000,
    }


@fixture
def invalid_config_data_api_id() -> dict[str, int | str | float]:
    """
    Invalid configuration data (deprecated - no longer used).

    Returns:
        dict[str, int | str | float]: Empty dict (this fixture is deprecated).
    """
    return {}  # This fixture is no longer needed, but kept for backward compatibility


@fixture
def invalid_config_data_timeout() -> dict[str, int | str | float]:
    """
    Invalid configuration data with timeout 0.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with timeout 0.
    """
    return {
        "timeout": 0,  # Invalid: must be >= 1
    }


@fixture
def invalid_config_data_minimal_retry_count() -> dict[str, int | str | float]:
    """
    Invalid configuration data with minimal retry count.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with minimal retry count.
    """
    return {
        "retry_count": -1,  # Invalid: must be >= 0
    }


@fixture
def invalid_config_data_maximal_retry_count() -> dict[str, int | str | float]:
    """
    Invalid configuration data with maximal retry count.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with maximal retry count.
    """
    return {
        "retry_count": 11,  # Invalid: must be <= 10
    }


@fixture
def invalid_config_data_minimal_retry_delay() -> dict[str, int | str | float]:
    """
    Invalid configuration data with minimal retry delay.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with minimal retry delay.
    """
    return {
        "retry_delay": 0.0,  # Invalid: must be >= 0.1
    }


@fixture
def invalid_config_data_maximal_retry_delay() -> dict[str, int | str | float]:
    """
    Invalid configuration data with maximal retry delay.

    Returns:
        dict[str, int | str | float]: Invalid configuration data with maximal retry delay.
    """
    return {
        "retry_delay": 10.1,  # Invalid: must be <= 10.0
    }


@fixture
def invalid_config_data_without_api_id() -> dict[str, str]:
    """
    Configuration data (deprecated - no longer used).

    Returns:
        dict[str, str]: Empty dict (this fixture is deprecated).
    """
    return {}  # This fixture is no longer needed, but kept for backward compatibility


@fixture
def invalid_config_data_without_api_hash() -> dict[str, int | str]:
    """
    Configuration data (deprecated - no longer used).

    Returns:
        dict[str, int | str]: Empty dict (this fixture is deprecated).
    """
    return {}  # This fixture is no longer needed, but kept for backward compatibility


@fixture
def config_data_for_default_values() -> dict[str, int | str | float | bool | None]:
    """
    Configuration data for testing default values.

    Returns:
        dict[str, int | str | float | bool | None]: Configuration data for default values test.
    """
    return {
        "base_url": None,
        "timeout": 30,
        "retry_count": 3,
        "retry_delay": 1.0,
        "log_level": "INFO",
        "browser_headless": True,
        "browser_timeout": 30000,
    }


@fixture
def config_data_for_missing_session() -> dict[str, int | str]:
    """
    Configuration data (deprecated - no longer used).

    Returns:
        dict[str, int | str]: Empty dict (this fixture is deprecated).
    """
    return {}  # This fixture is no longer needed, but kept for backward compatibility


@fixture
def config_data_for_invalid_log_level() -> dict[str, int | str]:
    """
    Configuration data for testing invalid log level validation.

    Returns:
        dict[str, int | str]: Configuration data with invalid log level.
    """
    return {
        "log_level": "INVALID",  # Invalid: must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
    }


@fixture
def config_data_for_invalid_retry_count() -> dict[str, int | str]:
    """
    Configuration data for testing invalid retry count validation.

    Returns:
        dict[str, int | str]: Configuration data with invalid retry count.
    """
    return {
        "retry_count": -1,  # Invalid: must be >= 0
    }


@fixture
def config_data_for_invalid_retry_delay() -> dict[str, int | str | float]:
    """
    Configuration data for testing invalid retry delay validation.

    Returns:
        dict[str, int | str | float]: Configuration data with invalid retry delay.
    """
    return {
        "retry_delay": 0.05,  # Invalid: must be >= 0.1
    }


@fixture
def config_data_for_empty_strings() -> dict[str, int | str]:
    """
    Configuration data (deprecated - no longer used).

    Returns:
        dict[str, int | str]: Empty dict (this fixture is deprecated).
    """
    return {}  # This fixture is no longer needed, but kept for backward compatibility


@fixture
def config_data_for_whitespace_strings() -> dict[str, int | str]:
    """
    Configuration data (deprecated - no longer used).

    Returns:
        dict[str, int | str]: Empty dict (this fixture is deprecated).
    """
    return {}  # This fixture is no longer needed, but kept for backward compatibility


@fixture
def config_data_for_very_long_strings() -> dict[str, int | str]:
    """
    Configuration data for testing very long strings.

    Returns:
        dict[str, int | str]: Configuration data with very long base_url.
    """
    long_string = "https://" + "a" * 10000 + ".com"
    return {
        "base_url": long_string,
    }


@fixture
def config_data_for_special_characters() -> dict[str, int | str]:
    """
    Configuration data for testing special characters.

    Returns:
        dict[str, int | str]: Configuration data with special characters in base_url.
    """
    special_string = "https://example.com/path!@#$%^&*()_+-=[]{}|;':\",./<>?"
    return {
        "base_url": special_string,
    }


@fixture
def config_data_for_unicode_characters() -> dict[str, int | str]:
    """
    Configuration data for testing unicode characters.

    Returns:
        dict[str, int | str]: Configuration data with unicode characters in base_url.
    """
    unicode_string = "https://example.com/тест_用户_テスト"
    return {
        "base_url": unicode_string,
    }


@fixture
def config_data_for_none_values() -> dict[str, int | str | None]:
    """
    Configuration data for testing None values.

    Returns:
        dict[str, int | str | None]: Configuration data with None base_url.
    """
    return {
        "base_url": None,  # None is valid for base_url
    }


@fixture
def config_data_for_both_session_methods() -> dict[str, int | str]:
    """
    Configuration data (deprecated - no longer used).

    Returns:
        dict[str, int | str]: Empty dict (this fixture is deprecated).
    """
    return {}  # This fixture is no longer needed, but kept for backward compatibility


@fixture
def config_data_for_log_level_debug() -> dict[str, int | str]:
    """
    Configuration data for testing log level debug.

    Returns:
        dict[str, int | str]: Configuration data for log level debug testing.
    """
    return {
        "log_level": "DEBUG",
    }


@fixture
def config_data_for_log_level_info() -> dict[str, int | str]:
    """
    Configuration data for testing log level info.

    Returns:
        dict[str, int | str]: Configuration data for log level info testing.
    """
    return {
        "log_level": "INFO",
    }


@fixture
def config_data_for_log_level_warning() -> dict[str, int | str]:
    """
    Configuration data for testing log level warning.

    Returns:
        dict[str, int | str]: Configuration data for log level warning testing.
    """
    return {
        "log_level": "WARNING",
    }


@fixture
def config_data_for_log_level_error() -> dict[str, int | str]:
    """
    Configuration data for testing log level error.

    Returns:
        dict[str, int | str]: Configuration data for log level error testing.
    """
    return {
        "log_level": "ERROR",
    }


@fixture
def config_data_for_log_level_critical() -> dict[str, int | str]:
    """
    Configuration data for testing log level critical.

    Returns:
        dict[str, int | str]: Configuration data for log level critical testing.
    """
    return {
        "log_level": "CRITICAL",
    }


@fixture
def config_data_for_log_level_case_sensitivity() -> dict[str, int | str]:
    """
    Configuration data for testing log level case sensitivity.

    Returns:
        dict[str, int | str]: Configuration data with lowercase log level (invalid).
    """
    return {
        "log_level": "debug",  # Invalid: must be uppercase
    }


@fixture
def config_data_for_float_precision() -> dict[str, int | str | float]:
    """
    Configuration data for testing float precision.

    Returns:
        dict[str, int | str | float]: Configuration data with precise float.
    """
    return {
        "retry_delay": 0.123456789,
    }


@fixture
def config_data_for_large_numbers() -> dict[str, int | str | float]:
    """
    Configuration data for testing large numbers.

    Returns:
        dict[str, int | str | float]: Configuration data with large numbers.
    """
    return {
        "timeout": 300,  # Max valid timeout
        "retry_count": 10,  # Max valid retry_count
        "retry_delay": 10.0,  # Max valid retry_delay
        "browser_timeout": 60000,  # Large browser timeout
    }


@fixture
def mock_environment(mocker: MockerFixture) -> dict[str, str]:
    """
    Mock environment variables for testing.

    Returns:
        dict[str, str]: Environment variables.
    """
    env_vars = {
        "WA_BASE_URL": "https://example.com",
        "WA_TIMEOUT": "30",
        "WA_RETRY_COUNT": "3",
        "WA_RETRY_DELAY": "1.0",
        "WA_LOG_LEVEL": "DEBUG",
        "WA_BROWSER_HEADLESS": "true",
        "WA_BROWSER_TIMEOUT": "30000",
    }
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_invalid_api_id(mocker: MockerFixture) -> dict[str, str]:
    """
    Mock environment variables with invalid WA_TIMEOUT for testing.

    Returns:
        dict[str, str]: Environment variables with invalid WA_TIMEOUT.
    """
    env_vars = {
        "WA_TIMEOUT": "invalid",  # Invalid: must be a number
    }
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_default_values(mocker: MockerFixture) -> dict[str, str]:
    """
    Mock environment variables with default values for testing.

    Returns:
        dict[str, str]: Environment variables with default values.
    """
    env_vars = {
        "WA_BASE_URL": "https://example.com",
        "WA_TIMEOUT": "30",
        "WA_RETRY_COUNT": "3",
        "WA_RETRY_DELAY": "1.0",
        "WA_LOG_LEVEL": "INFO",
    }
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_override_defaults(mocker: MockerFixture) -> dict[str, str]:
    """
    Mock environment variables with overridden default values for testing.

    Returns:
        dict[str, str]: Environment variables with overridden defaults.
    """
    env_vars = {
        "WA_BASE_URL": "https://example.com",
        "WA_TIMEOUT": "60",
        "WA_RETRY_COUNT": "5",
        "WA_RETRY_DELAY": "2.0",
        "WA_LOG_LEVEL": "WARNING",
    }
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def mock_environment_optional_variables(mocker: MockerFixture) -> dict[str, str]:
    """
    Mock environment variables with optional variables for testing.

    Returns:
        dict[str, str]: Environment variables with optional variables.
    """
    env_vars = {
        "WA_BASE_URL": "https://example.com",
        "WA_BROWSER_HEADLESS": "false",
        "WA_BROWSER_TIMEOUT": "60000",
    }
    mocker.patch.dict(os.environ, env_vars, clear=True)
    yield env_vars


@fixture
def yaml_config_file_valid() -> str:
    """
    Return path to valid YAML config file for testing.

    Returns:
        str: Path to the YAML file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "data", "valid_yaml.yaml")


@fixture
def yaml_config_file_minimal() -> str:
    """
    Return path to minimal YAML config file for testing.

    Returns:
        str: Path to the YAML file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "data", "minimal_config.yaml")


@fixture
def yaml_config_file_with_file_session() -> str:
    """
    Return path to YAML config file with session_file for testing.

    Returns:
        str: Path to the YAML file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "data", "config_with_file.yaml")


@fixture
def yaml_config_file_invalid() -> str:
    """
    Return path to invalid YAML config file for testing.

    Returns:
        str: Path to the YAML file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "data", "invalid_config.yaml")


@fixture
def yaml_config_file_missing_session() -> str:
    """
    Return path to YAML config file missing session for testing.

    Returns:
        str: Path to the YAML file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "data", "missing_session_config.yaml")


@fixture
def yaml_config_file_with_mini_app() -> str:
    """
    Return path to YAML config file with mini app settings for testing.

    Returns:
        str: Path to the YAML file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "data", "mini_app_config.yaml")


@fixture
def yaml_config_file_empty() -> str:
    """
    Return path to empty YAML config file for testing.

    Returns:
        str: Path to the YAML file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "data", "empty_config.yaml")


@fixture
def yaml_config_file_invalid_format() -> str:
    """
    Return path to YAML config file with invalid format for testing.

    Returns:
        str: Path to the YAML file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "data", "invalid_format_config.yaml")


# ============================================================================
# YAML config data fixtures (parsed YAML data)
# ============================================================================


def _load_yaml_data(file_name: str) -> dict[str, int | str | float | bool]:
    """
    Helper function to load YAML data from file.

    Configuration fields can be overridden by environment variables if they are set:
    - WA_BASE_URL overrides base_url
    - WA_TIMEOUT overrides timeout
    - WA_RETRY_COUNT overrides retry_count
    - WA_RETRY_DELAY overrides retry_delay
    - WA_LOG_LEVEL overrides log_level
    - WA_BROWSER_HEADLESS overrides browser_headless
    - WA_BROWSER_TIMEOUT overrides browser_timeout

    Args:
        file_name: Name of the YAML file in tests/data/.

    Returns:
        dict: Parsed YAML data with optional env var overrides.
    """
    file_path = Path(__file__).parent.parent / "data" / file_name
    with file_path.open() as f:
        config_data = load(f, Loader=SafeLoader)
    # Override fields with environment variables if present (WA_* prefix)
    if environ.get("WA_BASE_URL"):
        config_data["base_url"] = environ.get("WA_BASE_URL")
    if environ.get("WA_TIMEOUT"):
        config_data["timeout"] = int(environ.get("WA_TIMEOUT", "30"))
    if environ.get("WA_RETRY_COUNT"):
        config_data["retry_count"] = int(environ.get("WA_RETRY_COUNT", "3"))
    if environ.get("WA_RETRY_DELAY"):
        config_data["retry_delay"] = float(environ.get("WA_RETRY_DELAY", "1.0"))
    if environ.get("WA_LOG_LEVEL"):
        config_data["log_level"] = environ.get("WA_LOG_LEVEL")
    if environ.get("WA_BROWSER_HEADLESS"):
        config_data["browser_headless"] = environ.get("WA_BROWSER_HEADLESS", "true").lower() in ("true", "1", "yes")
    if environ.get("WA_BROWSER_TIMEOUT"):
        config_data["browser_timeout"] = int(environ.get("WA_BROWSER_TIMEOUT", "30000"))
    return config_data


@fixture
def yaml_config_data_valid() -> dict[str, int | str | float | bool]:
    """
    Return parsed YAML config data for valid config.

    Returns:
        dict: Parsed YAML config data.
    """
    return _load_yaml_data("valid_yaml.yaml")


@fixture
def yaml_config_data_minimal() -> dict[str, int | str | float | bool]:
    """
    Return parsed YAML config data for minimal config.

    Returns:
        dict: Parsed YAML config data.
    """
    return _load_yaml_data("minimal_config.yaml")

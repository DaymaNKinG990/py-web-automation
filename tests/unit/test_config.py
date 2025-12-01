"""
Unit tests for Web Automation Framework configuration.
"""

import builtins
import os
import sys
import tempfile
from unittest.mock import patch

import allure
import pytest
from loguru import logger
from msgspec import convert, to_builtins
from pytest import mark, raises

# Local imports
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


# ============================================================================
# I. Инициализация и валидация
# ============================================================================


class TestConfigInit:
    """Test Config initialization and validation."""

    @mark.unit
    @allure.title("TC-CONFIG-001: Create valid configuration")
    @allure.description("TC-CONFIG-001: Test creating a valid configuration.")
    def test_valid_config_creation(self, valid_config_data: dict[str, int | str | float]) -> None:
        """
        Test creating a valid configuration.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create Config from valid data"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Verify base_url matches"):
            assert config.base_url == valid_config_data.get("base_url"), "Base URL does not match"
        with allure.step("Verify timeout matches"):
            assert config.timeout == valid_config_data.get("timeout"), "Timeout does not match"
        with allure.step("Verify retry_count matches"):
            assert config.retry_count == valid_config_data.get("retry_count"), "Retry count does not match"
        with allure.step("Verify retry_delay matches"):
            assert config.retry_delay == valid_config_data.get("retry_delay"), "Retry delay does not match"
        with allure.step("Verify log_level matches"):
            assert config.log_level == valid_config_data.get("log_level"), "Log level does not match"
        with allure.step("Verify browser_headless matches"):
            assert config.browser_headless == valid_config_data.get("browser_headless"), (
                "Browser headless does not match"
            )
        with allure.step("Verify browser_timeout matches"):
            assert config.browser_timeout == valid_config_data.get("browser_timeout"), "Browser timeout does not match"

    @mark.unit
    @allure.title("TC-CONFIG-004: Create valid configuration")
    @allure.description("TC-CONFIG-004: Test creating a valid configuration.")
    def test_valid_config_with_file(
        self,
        valid_config_with_file_data: dict[str, int | str | float],
    ) -> None:
        """
        Test creating a valid configuration.

        Args:
            valid_config_with_file_data: Valid configuration data.
        """
        with allure.step("Create Config"):
            config = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
        with allure.step("Verify base_url matches"):
            assert config.base_url == valid_config_with_file_data.get("base_url"), "Base URL does not match"
        with allure.step("Verify timeout matches"):
            assert config.timeout == valid_config_with_file_data.get("timeout"), "Timeout does not match"
        with allure.step("Verify log_level matches"):
            assert config.log_level == valid_config_with_file_data.get("log_level"), "Log level does not match"

    @mark.unit
    @allure.title("TC-CONFIG-002: Configuration default values")
    @allure.description("TC-CONFIG-002: Test configuration default values.")
    def test_config_default_values(
        self,
        config_data_for_default_values: dict[str, int | str],
    ) -> None:
        """Test configuration default values."""
        with allure.step("Create Config with default values"):
            config = Config(**config_data_for_default_values)  # type: ignore[arg-type]
        with allure.step("Verify timeout default value"):
            assert config.timeout == config_data_for_default_values.get("timeout"), "Timeout should be default 30"
        with allure.step("Verify retry_count default value"):
            assert config.retry_count == config_data_for_default_values.get("retry_count"), (
                "Retry count should be default 3"
            )
        with allure.step("Verify retry_delay default value"):
            assert config.retry_delay == config_data_for_default_values.get("retry_delay"), (
                "Retry delay should be default 1.0"
            )
        with allure.step("Verify log_level default value"):
            assert config.log_level == config_data_for_default_values.get("log_level"), (
                "Log level should be default INFO"
            )
        with allure.step("Verify browser_headless default value"):
            assert config.browser_headless == config_data_for_default_values.get("browser_headless", True), (
                "Browser headless should be default True"
            )
        with allure.step("Verify browser_timeout default value"):
            assert config.browser_timeout == config_data_for_default_values.get("browser_timeout", 30000), (
                "Browser timeout should be default 30000"
            )
        with allure.step("Verify base_url default value"):
            assert config.base_url is config_data_for_default_values.get("base_url"), (
                "Base URL should be None by default"
            )

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration validation success")
    @allure.description("TC-CONFIG-001: Test successful configuration validation.")
    def test_config_validation_success(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """
        Test successful configuration validation.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create Config from valid data"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Verify validation passes"):
            assert 1 <= config.timeout <= 300, "Timeout should be between 1 and 300"
            assert 0 <= config.retry_count <= 10, "Retry count should be between 0 and 10"
            assert 0.1 <= config.retry_delay <= 10.0, "Retry delay should be between 0.1 and 10.0"
            assert config.log_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), "Log level should be valid"

    @mark.unit
    @allure.title("TC-CONFIG-006: Configuration validation (deprecated test)")
    @allure.description("TC-CONFIG-006: Test configuration validation (deprecated - kept for compatibility).")
    def test_config_validation_missing_api_id(
        self,
        invalid_config_data_without_api_id: dict[str, str | int | float],
    ) -> None:
        """
        Test configuration validation (deprecated - kept for compatibility).

        Args:
            invalid_config_data_without_api_id: Configuration data (deprecated).
        """
        with allure.step("Create Config with empty data (should use defaults)"):
            config = Config(**invalid_config_data_without_api_id)  # type: ignore[arg-type]
            # Should create with default values
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-009: Configuration validation (deprecated test)")
    @allure.description("TC-CONFIG-009: Test configuration validation (deprecated - kept for compatibility).")
    def test_config_validation_missing_api_hash(
        self,
        invalid_config_data_without_api_hash: dict[str, int | str],
    ) -> None:
        """
        Test configuration validation (deprecated - kept for compatibility).

        Args:
            invalid_config_data_without_api_hash: Configuration data (deprecated).
        """
        with allure.step("Create Config with empty data (should use defaults)"):
            config = Config(**invalid_config_data_without_api_hash)  # type: ignore[arg-type]
            # Should create with default values
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-021: Configuration validation (deprecated test)")
    @allure.description("TC-CONFIG-021: Test configuration validation (deprecated - kept for compatibility).")
    def test_config_validation_missing_session(
        self,
        config_data_for_missing_session: dict[str, int | str],
    ) -> None:
        """
        Test configuration validation (deprecated - kept for compatibility).

        Args:
            config_data_for_missing_session: Configuration data (deprecated).
        """
        with allure.step("Create Config with empty data (should use defaults)"):
            config = Config(**config_data_for_missing_session)  # type: ignore[arg-type]
            # Should create with default values
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-023: Configuration validation with invalid log level")
    @allure.description("TC-CONFIG-023: Test configuration validation with invalid log level.")
    def test_config_validation_invalid_log_level(
        self,
        config_data_for_invalid_log_level: dict[str, int | str],
    ) -> None:
        """
        Test configuration validation with invalid log level.

        Args:
            config_data_for_invalid_log_level: Configuration data with invalid log level.
        """
        with allure.step("Attempt to create Config with invalid log level"):
            # __post_init__ will raise ValueError for invalid log_level
            with raises(ValueError, match="Invalid log level"):
                Config(**config_data_for_invalid_log_level)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-015: Configuration validation with invalid retry count")
    @allure.description("TC-CONFIG-015: Test configuration validation with invalid retry count.")
    def test_config_validation_invalid_retry_count(
        self,
        config_data_for_invalid_retry_count: dict[str, int | str],
    ) -> None:
        """
        Test configuration validation with invalid retry count.

        Args:
            config_data_for_invalid_retry_count: Configuration data with invalid retry count.
        """
        with allure.step("Attempt to create Config with invalid retry_count"):
            with raises(ValueError, match="retry_count must be between 0 and 10"):
                Config(**config_data_for_invalid_retry_count)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-018: Configuration validation with invalid retry delay")
    @allure.description("TC-CONFIG-018: Test configuration validation with invalid retry delay.")
    def test_config_validation_invalid_retry_delay(
        self,
        config_data_for_invalid_retry_delay: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid retry delay.

        Args:
            config_data_for_invalid_retry_delay: Configuration data with invalid retry delay.
        """
        with allure.step("Attempt to create Config with invalid retry_delay"):
            with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
                Config(**config_data_for_invalid_retry_delay)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-002: Configuration validation with minimal values")
    @allure.description("TC-CONFIG-002: Test configuration validation with minimal values.")
    def test_config_validation_minimal_values(
        self,
        valid_config_data_minimal: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with minimal values.

        Args:
            valid_config_data_minimal: Valid configuration data minimal.
        """
        with allure.step("Create Config with minimal values"):
            config = Config(**valid_config_data_minimal)  # type: ignore[arg-type]
        with allure.step("Verify all minimal values are set correctly"):
            assert config.timeout == valid_config_data_minimal.get("timeout"), "Timeout does not match"
            assert config.retry_count == valid_config_data_minimal.get("retry_count"), "Retry count does not match"
            assert config.retry_delay == valid_config_data_minimal.get("retry_delay"), "Retry delay does not match"

    @mark.unit
    @allure.title("TC-CONFIG-002: Configuration validation with maximal values")
    @allure.description("TC-CONFIG-002: Test configuration validation with maximal values.")
    def test_config_validation_maximal_values(
        self,
        valid_config_data_maximal: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with maximal values.

        Args:
            valid_config_data_maximal: Valid configuration data maximal.
        """
        with allure.step("Create Config with maximal values"):
            config = Config(**valid_config_data_maximal)  # type: ignore[arg-type]
        with allure.step("Verify all maximal values are set correctly"):
            assert config.base_url == valid_config_data_maximal.get("base_url"), "Base URL does not match"
            assert config.timeout == valid_config_data_maximal.get("timeout"), "Timeout does not match"
            assert config.retry_count == valid_config_data_maximal.get("retry_count"), "Retry count does not match"
            assert config.retry_delay == valid_config_data_maximal.get("retry_delay"), "Retry delay does not match"
            assert config.log_level == valid_config_data_maximal.get("log_level"), "Log level does not match"
            assert config.browser_headless == valid_config_data_maximal.get("browser_headless"), (
                "Browser headless does not match"
            )
            assert config.browser_timeout == valid_config_data_maximal.get("browser_timeout"), (
                "Browser timeout does not match"
            )

    @mark.unit
    @allure.title("TC-CONFIG-006: Configuration validation (deprecated test)")
    @allure.description("TC-CONFIG-006: Test configuration validation (deprecated - kept for compatibility).")
    def test_config_validation_invalid_api_id(
        self,
        invalid_config_data_api_id: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation (deprecated - kept for compatibility).

        Args:
            invalid_config_data_api_id: Configuration data (deprecated).
        """
        with allure.step("Create Config with empty data (should use defaults)"):
            # Should create with default values if data is empty
            config = Config(**invalid_config_data_api_id)  # type: ignore[arg-type]
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-015: Configuration validation with invalid minimal retry count")
    @allure.description("TC-CONFIG-015: Test configuration validation with invalid minimal retry count.")
    def test_config_validation_invalid_minimal_retry_count(
        self,
        invalid_config_data_minimal_retry_count: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid minimal retry count.

        Args:
            invalid_config_data_minimal_retry_count: Invalid configuration data with invalid minimal retry count.
        """
        with allure.step("Attempt to create Config with invalid minimal retry_count"):
            with raises(ValueError, match="retry_count must be between 0 and 10"):
                Config(**invalid_config_data_minimal_retry_count)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-018: Configuration validation with invalid minimal retry delay")
    @allure.description("TC-CONFIG-018: Test configuration validation with invalid minimal retry delay.")
    def test_config_validation_invalid_minimal_retry_delay(
        self,
        invalid_config_data_minimal_retry_delay: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid minimal retry delay.

        Args:
            invalid_config_data_minimal_retry_delay: Invalid configuration data with invalid minimal retry delay.
        """
        with allure.step("Attempt to create Config with invalid minimal retry_delay"):
            with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
                Config(**invalid_config_data_minimal_retry_delay)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-012: Configuration validation with invalid timeout")
    @allure.description("TC-CONFIG-012: Test configuration validation with invalid timeout.")
    def test_config_validation_invalid_timeout(
        self,
        invalid_config_data_timeout: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid timeout.

        Args:
            invalid_config_data_timeout: Invalid configuration data with invalid timeout.
        """
        with allure.step("Attempt to create Config with invalid timeout"):
            with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
                Config(**invalid_config_data_timeout)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-016: Configuration validation with invalid maximal retry count")
    @allure.description("TC-CONFIG-016: Test configuration validation with invalid maximal retry count.")
    def test_config_validation_invalid_maximal_retry_count(
        self,
        invalid_config_data_maximal_retry_count,
    ):
        """
        Test configuration validation with invalid maximal retry count.

        Args:
            invalid_config_data_maximal_retry_count: Invalid configuration data with invalid maximal retry count.
        """
        with allure.step("Attempt to create Config with invalid maximal retry_count"):
            with raises(ValueError, match="retry_count must be between 0 and 10"):
                Config(**invalid_config_data_maximal_retry_count)

    @mark.unit
    @allure.title("TC-CONFIG-019: Configuration validation with invalid maximal retry delay")
    @allure.description("TC-CONFIG-019: Test configuration validation with invalid maximal retry delay.")
    def test_config_validation_invalid_maximal_retry_delay(
        self,
        invalid_config_data_maximal_retry_delay: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration validation with invalid maximal retry delay.

        Args:
            invalid_config_data_maximal_retry_delay: Invalid configuration data with invalid maximal retry delay.
        """
        with allure.step("Attempt to create Config with invalid maximal retry_delay"):
            with raises(ValueError, match="retry_delay must be between 0.1 and 10.0"):
                Config(**invalid_config_data_maximal_retry_delay)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration serialization")
    @allure.description("TC-CONFIG-001: Test configuration serialization.")
    def test_config_serialization(self, valid_config_data: dict[str, int | str | float]) -> None:
        """
        Test configuration serialization.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create Config from valid data"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Serialize Config to dict"):
            config_dict = to_builtins(config)
        with allure.step("Verify serialized dict"):
            assert isinstance(config_dict, dict)
            assert config_dict.get("base_url") == valid_config_data.get("base_url")
            assert config_dict.get("timeout") == valid_config_data.get("timeout")
            assert config_dict.get("retry_count") == valid_config_data.get("retry_count")
            assert config_dict.get("retry_delay") == valid_config_data.get("retry_delay")
            assert config_dict.get("log_level") == valid_config_data.get("log_level")

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration deserialization")
    @allure.description("TC-CONFIG-001: Test configuration deserialization.")
    def test_config_deserialization(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration deserialization.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Prepare config dict"):
            config_dict = valid_config_data.copy()
        with allure.step("Deserialize dict to Config"):
            config = convert(config_dict, Config)
        with allure.step("Verify deserialized Config"):
            assert isinstance(config, Config)
            assert config.base_url == valid_config_data.get("base_url")
            assert config.timeout == valid_config_data.get("timeout")
            assert config.retry_count == valid_config_data.get("retry_count")
            assert config.retry_delay == valid_config_data.get("retry_delay")
            assert config.log_level == valid_config_data.get("log_level")

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration equality with same data")
    @allure.description("TC-CONFIG-001: Test configuration equality with same data.")
    def test_config_equality(self, valid_config_data: dict[str, int | str | float]) -> None:
        """
        Test configuration equality with same data.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create two Config instances with same data"):
            config1 = Config(**valid_config_data)  # type: ignore[arg-type]
            config2 = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Verify configurations are equal"):
            assert config1 == config2, "Configuration should be equal"

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration inequality with different data")
    @allure.description("TC-CONFIG-001: Test configuration inequality with different data.")
    def test_config_inequality(
        self,
        valid_config_data: dict[str, int | str | float],
        valid_config_with_file_data: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration inequality with different data.

        Args:
            valid_config_data: Valid configuration data.
            valid_config_with_file_data: Valid configuration data with file.
        """
        with allure.step("Create two Config instances with different data"):
            config1 = Config(**valid_config_data)  # type: ignore[arg-type]
            config2 = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
        with allure.step("Verify configurations are not equal"):
            assert config1 != config2, "Configuration should be different"

    @mark.unit
    @allure.title("TC-CONFIG-039: Configuration hash equality with same data")
    @allure.description("TC-CONFIG-039: Test configuration hash equality with same data.")
    def test_config_hash_equality(self, valid_config_data: dict[str, int | str | float]) -> None:
        """
        Test configuration hash equality with same data.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create two Config instances with same data"):
            config1 = Config(**valid_config_data)  # type: ignore[arg-type]
            config2 = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Verify configuration hashes are equal"):
            assert hash(config1) == hash(config2), "Configuration hashes should be equal"

    @mark.unit
    @allure.title("TC-CONFIG-039: Configuration hash inequality with different data")
    @allure.description("TC-CONFIG-039: Test configuration hash inequality with different data.")
    def test_config_hash_inequality(
        self,
        valid_config_data: dict[str, int | str | float],
        valid_config_with_file_data: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration hash inequality with different data.

        Args:
            valid_config_data: Valid configuration data.
            valid_config_with_file_data: Valid configuration data with file.
        """
        with allure.step("Create two Config instances with different data"):
            config1 = Config(**valid_config_data)  # type: ignore[arg-type]
            config2 = Config(**valid_config_with_file_data)  # type: ignore[arg-type]
        with allure.step("Verify configuration hashes are not equal"):
            assert hash(config1) != hash(config2), "Configuration hashes should be different"

    @mark.unit
    @allure.title("TC-CONFIG-001: Configuration string representation")
    @allure.description("TC-CONFIG-001: Test configuration string representation.")
    def test_config_repr(self, valid_config_data: dict[str, int | str | float]) -> None:
        """
        Test configuration string representation.

        Args:
            valid_config_data: Valid configuration data.
        """
        with allure.step("Create Config instance"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Get string representation"):
            repr_str = repr(config)
        with allure.step("Verify repr contains expected information"):
            assert "Config" in repr_str
            assert f"base_url='{valid_config_data.get('base_url')}'" in repr_str
            assert f"timeout={valid_config_data.get('timeout')}" in repr_str


# ============================================================================
# II. Config.from_env()
# ============================================================================


class TestConfigFromEnv:
    """Test Config.from_env() method."""

    @mark.unit
    @allure.title("TC-CONFIG-025: Create config from valid environment variables")
    @allure.description("TC-CONFIG-025: Test creating config from valid environment variables.")
    def test_from_env_valid_variables(self, mock_environment: dict[str, str]) -> None:
        """
        Test creating config from valid environment variables.

        Args:
            mock_environment: Mock environment variables (already patched by fixture).
        """
        # Environment is already patched by mock_environment fixture
        with allure.step("Create Config from environment variables"):
            config = Config.from_env()
        with allure.step("Verify all environment variables are loaded correctly"):
            assert config.base_url == mock_environment.get("WA_BASE_URL"), "Base URL does not match"
            assert config.timeout == int(mock_environment.get("WA_TIMEOUT") or "30"), "Timeout does not match"
            assert config.retry_count == int(mock_environment.get("WA_RETRY_COUNT") or "3"), (
                "Retry count does not match"
            )
            assert config.retry_delay == float(mock_environment.get("WA_RETRY_DELAY") or "1.0"), (
                "Retry delay does not match"
            )
            assert config.log_level == mock_environment.get("WA_LOG_LEVEL"), "Log level does not match"
            assert config.browser_headless is True, "Browser headless should be True"
            assert config.browser_timeout == int(mock_environment.get("WA_BROWSER_TIMEOUT") or "30000"), (
                "Browser timeout does not match"
            )

    @mark.unit
    @allure.title("TC-CONFIG-028: Create config with missing required environment variables")
    @allure.description("TC-CONFIG-028: Test creating config with missing required environment variables.")
    def test_from_env_missing_required_variables(
        self,
        mock_empty_environment: dict[str, str],
    ) -> None:
        """
        Test creating config with missing required environment variables.

        Args:
            mock_empty_environment: Mock empty environment variables (already patched by fixture).
        """
        # Environment is already patched by mock_empty_environment fixture
        with allure.step("Create Config from empty environment (should use defaults)"):
            config = Config.from_env()
            # Should create with default values
            assert config.timeout == 30
            assert config.retry_count == 3
            assert config.retry_delay == 1.0
            assert config.log_level == "INFO"

    @mark.unit
    @allure.title("TC-CONFIG-028: Create config (deprecated test)")
    @allure.description("TC-CONFIG-028: Test creating config (deprecated - kept for compatibility).")
    def test_from_env_missing_api_id(
        self,
        mock_environment_missing_api_id: dict[str, str],
    ) -> None:
        """
        Test creating config (deprecated - kept for compatibility).

        Args:
            mock_environment_missing_api_id: Mock environment variables (deprecated).
        """
        # Environment is already patched by mock_environment_missing_api_id fixture
        with allure.step("Create Config from environment (should use defaults)"):
            config = Config.from_env()
            # Should create with default values
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-029: Create config (deprecated test)")
    @allure.description("TC-CONFIG-029: Test creating config (deprecated - kept for compatibility).")
    def test_from_env_missing_api_hash(
        self,
        mock_environment_missing_api_hash: dict[str, str],
    ) -> None:
        """
        Test creating config (deprecated - kept for compatibility).

        Args:
            mock_environment_missing_api_hash: Mock environment variables (deprecated).
        """
        # Environment is already patched by mock_environment_missing_api_hash fixture
        with allure.step("Create Config from environment (should use defaults)"):
            config = Config.from_env()
            # Should create with default values
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-030: Create config with invalid TMA_API_ID")
    @allure.description("TC-CONFIG-030: Test creating config with invalid TMA_API_ID.")
    def test_from_env_invalid_api_id(
        self,
        mock_environment_invalid_api_id: dict[str, str],
    ) -> None:
        """
        Test creating config with invalid WA_TIMEOUT.

        Args:
            mock_environment_invalid_api_id: Mock environment variables with invalid WA_TIMEOUT (already patched by fixture).
        """
        # Environment is already patched by mock_environment_invalid_api_id fixture
        with allure.step("Attempt to create Config with invalid WA_TIMEOUT"):
            with raises(ValueError, match="WA_TIMEOUT must be a valid integer"):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-027: Create config with default values from environment")
    @allure.description("TC-CONFIG-027: Test creating config with default values from environment.")
    def test_from_env_default_values(
        self,
        mock_environment_default_values: dict[str, str],
    ) -> None:
        """
        Test creating config with default values from environment.

        Args:
            mock_environment_default_values: Mock environment variables with default values (already patched by fixture).
        """
        # Environment is already patched by mock_environment_default_values fixture
        with allure.step("Create Config from environment with default values"):
            config = Config.from_env()
        with allure.step("Verify default values are set correctly"):
            assert config.timeout == int(mock_environment_default_values.get("WA_TIMEOUT") or "30"), (
                "Timeout should be default 30"
            )
            assert config.retry_count == int(mock_environment_default_values.get("WA_RETRY_COUNT") or "3"), (
                "Retry count should be default 3"
            )
            assert config.retry_delay == float(mock_environment_default_values.get("WA_RETRY_DELAY") or "1.0"), (
                "Retry delay should be default 1.0"
            )
            assert config.log_level == mock_environment_default_values.get("WA_LOG_LEVEL"), (
                "Log level should be default INFO"
            )

    @mark.unit
    @allure.title("TC-CONFIG-026: Create config with overridden default values")
    @allure.description("TC-CONFIG-026: Test creating config with overridden default values.")
    def test_from_env_override_defaults(
        self,
        mock_environment_override_defaults: dict[str, str],
    ) -> None:
        """
        Test creating config with overridden default values.

        Args:
            mock_environment_override_defaults: Mock environment variables with overridden defaults (already patched by fixture).
        """
        # Environment is already patched by mock_environment_override_defaults fixture
        with allure.step("Create Config from environment with overridden defaults"):
            config = Config.from_env()
        with allure.step("Verify overridden values are set correctly"):
            assert config.timeout == int(mock_environment_override_defaults.get("WA_TIMEOUT") or "60"), (
                "Timeout should be overridden to 60"
            )
            assert config.retry_count == int(mock_environment_override_defaults.get("WA_RETRY_COUNT") or "5"), (
                "Retry count should be overridden to 5"
            )
            assert config.retry_delay == float(mock_environment_override_defaults.get("WA_RETRY_DELAY") or "2.0"), (
                "Retry delay should be overridden to 2.0"
            )
            assert config.log_level == mock_environment_override_defaults.get("WA_LOG_LEVEL"), (
                "Log level should be overridden to WARNING"
            )

    @mark.unit
    @allure.title("TC-CONFIG-005: Create config with optional environment variables")
    @allure.description("TC-CONFIG-005: Test creating config with optional environment variables.")
    def test_from_env_optional_variables(
        self,
        mock_environment_optional_variables: dict[str, str],
    ) -> None:
        """
        Test creating config with optional environment variables.

        Args:
            mock_environment_optional_variables: Mock environment variables with optional variables (already patched by fixture).
        """
        # Environment is already patched by mock_environment_optional_variables fixture
        with allure.step("Create Config from environment with optional variables"):
            config = Config.from_env()
        with allure.step("Verify optional values are set correctly"):
            assert config.base_url == mock_environment_optional_variables.get("WA_BASE_URL")
            assert config.browser_headless is False  # WA_BROWSER_HEADLESS="false"
            assert config.browser_timeout == int(mock_environment_optional_variables.get("WA_BROWSER_TIMEOUT", "60000"))

    @mark.unit
    @allure.title("TC-CONFIG-025: Type conversion in from_env method")
    @allure.description("TC-CONFIG-025: Test type conversion in from_env method.")
    def test_from_env_type_conversion(
        self,
        mock_environment_type_conversion: dict[str, str],
    ) -> None:
        """
        Test type conversion in from_env method.

        Args:
            mock_environment_type_conversion: Mock environment variables for type conversion testing (already patched by fixture).
        """
        # Environment is already patched by mock_environment_type_conversion fixture
        with allure.step("Create Config from environment"):
            config = Config.from_env()
        with allure.step("Verify type conversions"):
            assert isinstance(config.timeout, int), "Timeout should be int"
            assert isinstance(config.retry_count, int), "Retry count should be int"
            assert isinstance(config.retry_delay, float), "Retry delay should be float"
            assert isinstance(config.browser_timeout, int), "Browser timeout should be int"
            assert isinstance(config.browser_headless, bool), "Browser headless should be bool"

    @mark.unit
    @allure.title("TC-CONFIG-030: Invalid type conversion in from_env method")
    @allure.description("TC-CONFIG-030: Test invalid type conversion in from_env method.")
    def test_from_env_invalid_type_conversion(
        self,
        mock_environment_invalid_type_conversion: dict[str, str],
    ) -> None:
        """
        Test invalid type conversion in from_env method.

        Args:
            mock_environment_invalid_type_conversion: Mock environment variables with invalid type conversion.
        """
        # Environment is already set by fixture
        with allure.step("Attempt to create Config with invalid type conversion"):
            with raises(ValueError):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-031: from_env method with missing session string")
    @allure.description("TC-CONFIG-031: Test from_env method with missing session string.")
    def test_from_env_with_empty_strings(
        self, monkeypatch, mock_environment_missing_session_string: dict[str, str]
    ) -> None:
        """
        Test from_env method with missing session string.

        Args:
            mock_environment_missing_session_string: Mock environment variables missing TMA_SESSION_STRING.
        """
        # Environment is already set by fixture

        with allure.step("Create Config from environment (should use defaults)"):
            # Should create with default values if session is missing
            config = Config.from_env()
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-030: from_env method with invalid WA_TIMEOUT")
    @allure.description("TC-CONFIG-030: Test from_env method with invalid WA_TIMEOUT.")
    def test_from_env_with_invalid_api_id(self, monkeypatch, mock_environment_invalid_api_id: dict[str, str]) -> None:
        """
        Test from_env method with invalid WA_TIMEOUT.

        Args:
            mock_environment_invalid_api_id: Mock environment variables with invalid TMA_API_ID.
        """
        # Environment is already set by fixture
        # Invalid string "invalid" will cause ValueError when converting to int
        with allure.step("Attempt to create Config with invalid WA_TIMEOUT"):
            with raises(ValueError, match="WA_TIMEOUT must be a valid integer"):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-009: from_env method with invalid TMA_API_HASH length")
    @allure.description("TC-CONFIG-009: Test from_env method with invalid TMA_API_HASH length.")
    def test_from_env_with_invalid_api_hash_length(
        self, monkeypatch, mock_environment_invalid_api_hash_length: dict[str, str]
    ) -> None:
        """
        Test from_env method with invalid TMA_API_HASH length.

        Args:
            mock_environment_invalid_api_hash_length: Mock environment variables with invalid TMA_API_HASH length.
        """
        # Environment is already set by fixture
        with allure.step("Create Config from environment (should use defaults)"):
            # Should create with default values if api_hash is invalid
            config = Config.from_env()
            assert config.timeout == 30
            assert config.retry_count == 3


# ============================================================================
# III. Граничные случаи и дополнительные тесты инициализации
# ============================================================================


class TestConfigInitEdgeCases:
    """Test Config initialization edge cases."""

    @mark.unit
    @allure.title("TC-CONFIG-009: Configuration with empty strings")
    @allure.description("TC-CONFIG-009: Test configuration with empty strings.")
    def test_config_with_empty_strings(
        self,
        config_data_for_empty_strings: dict[str, int | str],
    ) -> None:
        """
        Test configuration with empty strings.

        Args:
            config_data_for_empty_strings: Configuration data with empty strings.
        """
        with allure.step("Create Config with empty strings (should use defaults)"):
            # Should create with default values if strings are empty
            config = Config(**config_data_for_empty_strings)  # type: ignore[arg-type]
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-022: Configuration with whitespace strings")
    @allure.description("TC-CONFIG-022: Test configuration with whitespace strings.")
    def test_config_with_whitespace_strings(
        self,
        config_data_for_whitespace_strings: dict[str, int | str],
    ) -> None:
        """
        Test configuration with whitespace strings.

        Args:
            config_data_for_whitespace_strings: Configuration data with whitespace strings.
        """
        with allure.step("Create Config with whitespace strings (should use defaults)"):
            # Should create with default values if strings are whitespace
            config = Config(**config_data_for_whitespace_strings)  # type: ignore[arg-type]
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-041: Configuration with very long strings")
    @allure.description("TC-CONFIG-041: Test configuration with very long strings.")
    def test_config_with_very_long_strings(
        self,
        config_data_for_very_long_strings: dict[str, int | str],
    ) -> None:
        """
        Test configuration with very long strings.

        Args:
            config_data_for_very_long_strings: Configuration data with very long strings.
        """
        with allure.step("Create Config with very long strings"):
            config = Config(**config_data_for_very_long_strings)  # type: ignore[arg-type]
        with allure.step("Verify very long base_url is handled"):
            assert config.base_url == config_data_for_very_long_strings.get("base_url")

    @mark.unit
    @allure.title("TC-CONFIG-042: Configuration with special characters")
    @allure.description("TC-CONFIG-042: Test configuration with special characters.")
    def test_config_with_special_characters(
        self,
        config_data_for_special_characters: dict[str, int | str],
    ) -> None:
        """
        Test configuration with special characters.

        Args:
            config_data_for_special_characters: Configuration data with special characters.
        """
        with allure.step("Create Config with special characters"):
            config = Config(**config_data_for_special_characters)  # type: ignore[arg-type]
        with allure.step("Verify special characters are handled correctly"):
            assert config.base_url == config_data_for_special_characters.get("base_url"), "Base URL should match"

    @mark.unit
    @allure.title("TC-CONFIG-042: Configuration with unicode characters")
    @allure.description("TC-CONFIG-042: Test configuration with unicode characters.")
    def test_config_with_unicode_characters(
        self,
        config_data_for_unicode_characters: dict[str, int | str],
    ) -> None:
        """
        Test configuration with unicode characters.

        Args:
            config_data_for_unicode_characters: Configuration data with unicode characters.
        """
        with allure.step("Create Config with unicode characters"):
            config = Config(**config_data_for_unicode_characters)  # type: ignore[arg-type]
        with allure.step("Verify unicode characters are handled correctly"):
            assert config.base_url == config_data_for_unicode_characters.get("base_url"), "Base URL should match"

    @mark.unit
    @allure.title("TC-CONFIG-043: Configuration with None values")
    @allure.description("TC-CONFIG-043: Test configuration with None values.")
    def test_config_with_none_values(
        self,
        config_data_for_none_values: dict[str, int | str | None],
    ) -> None:
        """
        Test configuration with None values.

        Args:
            config_data_for_none_values: Configuration data with None values.
        """
        with allure.step("Create Config with None values"):
            config = Config(**config_data_for_none_values)  # type: ignore[arg-type]
        with allure.step("Verify None values are handled correctly"):
            assert config.base_url is None, "Base URL should be None"

    @mark.unit
    @allure.title("TC-CONFIG-005: Configuration (deprecated test)")
    @allure.description("TC-CONFIG-005: Test configuration (deprecated - kept for compatibility).")
    def test_config_with_both_session_methods(
        self,
        config_data_for_both_session_methods: dict[str, int | str],
    ) -> None:
        """
        Test configuration (deprecated - kept for compatibility).

        Args:
            config_data_for_both_session_methods: Configuration data (deprecated).
        """
        with allure.step("Create Config with empty data (should use defaults)"):
            config = Config(**config_data_for_both_session_methods)  # type: ignore[arg-type]
            # Should create with default values
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-043: Configuration base_url with whitespace")
    @allure.description(
        "TC-CONFIG-043: Test that base_url with whitespace at beginning/end is preserved as-is (no strip)."
    )
    def test_config_mini_app_url_with_whitespace(self) -> None:
        """
        Test that base_url with whitespace at beginning/end is preserved as-is (no strip).

        This test verifies that optional fields like base_url preserve whitespace
        and are not automatically stripped, as per specification requirement.
        """
        with allure.step("Prepare URL with whitespace"):
            url_with_whitespace = "  https://example.com/app  "
        with allure.step("Create Config with URL containing whitespace"):
            config = Config(
                base_url=url_with_whitespace,
            )
        with allure.step("Verify whitespace is preserved"):
            assert config.base_url == url_with_whitespace, "base_url should preserve whitespace without strip"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level debug")
    @allure.description("TC-CONFIG-024: Test configuration log level debug.")
    def test_config_log_level_debug(
        self,
        config_data_for_log_level_debug: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level debug.

        Args:
            config_data_for_log_level_debug: Configuration data with log level debug.
        """
        with allure.step("Create Config with DEBUG log level"):
            config = Config(**config_data_for_log_level_debug)  # type: ignore[arg-type]
        with allure.step("Verify log level is DEBUG"):
            assert config.log_level == config_data_for_log_level_debug.get("log_level"), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level info")
    @allure.description("TC-CONFIG-024: Test configuration log level info.")
    def test_config_log_level_info(
        self,
        config_data_for_log_level_info: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level info.

        Args:
            config_data_for_log_level_info: Configuration data with log level info.
        """
        with allure.step("Create Config with INFO log level"):
            config = Config(**config_data_for_log_level_info)  # type: ignore[arg-type]
        with allure.step("Verify log level is INFO"):
            assert config.log_level == config_data_for_log_level_info.get("log_level"), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level warning")
    @allure.description("TC-CONFIG-024: Test configuration log level warning.")
    def test_config_log_level_warning(
        self,
        config_data_for_log_level_warning: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level warning.

        Args:
            config_data_for_log_level_warning: Configuration data with log level warning.
        """
        with allure.step("Create Config with WARNING log level"):
            config = Config(**config_data_for_log_level_warning)  # type: ignore[arg-type]
        with allure.step("Verify log level is WARNING"):
            assert config.log_level == config_data_for_log_level_warning.get("log_level"), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level error")
    @allure.description("TC-CONFIG-024: Test configuration log level error.")
    def test_config_log_level_error(
        self,
        config_data_for_log_level_error: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level error.

        Args:
            config_data_for_log_level_error: Configuration data with log level error.
        """
        with allure.step("Create Config with ERROR log level"):
            config = Config(**config_data_for_log_level_error)  # type: ignore[arg-type]
        with allure.step("Verify log level is ERROR"):
            assert config.log_level == config_data_for_log_level_error.get("log_level"), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-024: Configuration log level critical")
    @allure.description("TC-CONFIG-024: Test configuration log level critical.")
    def test_config_log_level_critical(
        self,
        config_data_for_log_level_critical: dict[str, int | str],
    ) -> None:
        """
        Test configuration log level critical.

        Args:
            config_data_for_log_level_critical: Configuration data with log level critical.
        """
        with allure.step("Create Config with CRITICAL log level"):
            config = Config(**config_data_for_log_level_critical)  # type: ignore[arg-type]
        with allure.step("Verify log level is CRITICAL"):
            assert config.log_level == config_data_for_log_level_critical.get("log_level"), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-023: Log level case sensitivity")
    @allure.description("TC-CONFIG-023: Test log level case sensitivity.")
    def test_config_log_level_case_sensitivity(
        self,
        config_data_for_log_level_case_sensitivity: dict[str, int | str],
    ) -> None:
        """
        Test log level case sensitivity.

        Args:
            config_data_for_log_level_case_sensitivity: Configuration data with log level case sensitivity.
        """
        with allure.step("Attempt to create Config with invalid case log level"):
            # __post_init__ will raise ValueError for invalid log_level
            with raises(ValueError, match="Invalid log level"):
                Config(**config_data_for_log_level_case_sensitivity)  # type: ignore[arg-type]

    @mark.unit
    @allure.title("TC-CONFIG-020: Float precision in retry_delay")
    @allure.description("TC-CONFIG-020: Test float precision in retry_delay.")
    def test_config_float_precision(
        self,
        config_data_for_float_precision: dict[str, int | str | float],
    ) -> None:
        """
        Test float precision in retry_delay.

        Args:
            config_data_for_float_precision: Configuration data with float precision.
        """
        with allure.step("Create Config with float precision"):
            config = Config(**config_data_for_float_precision)  # type: ignore[arg-type]
        with allure.step("Verify float precision is preserved"):
            assert config.retry_delay == config_data_for_float_precision.get("retry_delay"), "Retry delay should match"

    @mark.unit
    @allure.title("TC-CONFIG-040: Configuration with large numbers")
    @allure.description("TC-CONFIG-040: Test configuration with large numbers.")
    def test_config_large_numbers(
        self,
        config_data_for_large_numbers: dict[str, int | str | float],
    ) -> None:
        """
        Test configuration with large numbers.

        Args:
            config_data_for_large_numbers: Configuration data with large numbers.
        """
        with allure.step("Create Config with large numbers"):
            config = Config(**config_data_for_large_numbers)  # type: ignore[arg-type]
        with allure.step("Verify large numbers are handled correctly"):
            assert config.timeout == config_data_for_large_numbers.get("timeout"), "Timeout should match"
            assert config.retry_count == config_data_for_large_numbers.get("retry_count"), "Retry count should match"
            assert config.retry_delay == config_data_for_large_numbers.get("retry_delay"), "Retry delay should match"
            assert config.browser_timeout == config_data_for_large_numbers.get("browser_timeout", 30000), (
                "Browser timeout should match"
            )


# ============================================================================
# IV. Config.from_yaml()
# ============================================================================


class TestConfigFromYaml:
    """Test Config.from_yaml() method."""

    @mark.unit
    @allure.title("TC-CONFIG-032: Create config from valid YAML file")
    @allure.description("TC-CONFIG-032: Test creating config from valid YAML file.")
    def test_from_yaml_valid_file(self, yaml_config_file_valid: str, yaml_config_data_valid: dict) -> None:
        """
        Test creating config from valid YAML file.

        Args:
            yaml_config_file_valid: Path to valid YAML config file.
            yaml_config_data_valid: Parsed YAML config data.
        """
        with allure.step("Load Config from valid YAML file"):
            config = Config.from_yaml(yaml_config_file_valid)
        with allure.step("Verify all values from YAML are loaded correctly"):
            assert config.base_url == yaml_config_data_valid.get("base_url"), "Base URL should match"
            assert config.timeout == yaml_config_data_valid.get("timeout"), "Timeout should match"
            assert config.retry_count == yaml_config_data_valid.get("retry_count"), "Retry count should match"
            assert config.retry_delay == yaml_config_data_valid.get("retry_delay"), "Retry delay should match"
            assert config.log_level == yaml_config_data_valid.get("log_level"), "Log level should match"
            assert config.browser_headless == yaml_config_data_valid.get("browser_headless", True), (
                "Browser headless should match"
            )
            assert config.browser_timeout == yaml_config_data_valid.get("browser_timeout", 30000), (
                "Browser timeout should match"
            )

    @mark.unit
    @allure.title("TC-CONFIG-034: Create config from minimal YAML file")
    @allure.description("TC-CONFIG-034: Test creating config from minimal YAML file.")
    def test_from_yaml_minimal_file(self, yaml_config_file_minimal: str, yaml_config_data_minimal: dict) -> None:
        """
        Test creating config from minimal YAML file.

        Args:
            yaml_config_file_minimal: Path to minimal YAML config file.
            yaml_config_data_minimal: Parsed YAML config data.
        """
        with allure.step("Load Config from minimal YAML file"):
            config = Config.from_yaml(yaml_config_file_minimal)
        with allure.step("Verify all values from minimal YAML are loaded correctly"):
            assert config.base_url == yaml_config_data_minimal.get("base_url"), "Base URL should match or be None"
            assert config.timeout == yaml_config_data_minimal.get("timeout", 30), (
                "Timeout should match or be default 30"
            )
            assert config.retry_count == yaml_config_data_minimal.get("retry_count", 3), (
                "Retry count should match or be default 3"
            )
            assert config.retry_delay == yaml_config_data_minimal.get("retry_delay", 1.0), (
                "Retry delay should match or be default 1.0"
            )
            assert config.log_level == yaml_config_data_minimal.get("log_level", "INFO"), (
                "Log level should be default INFO"
            )

    @mark.unit
    @allure.title("TC-CONFIG-004: Create config from YAML file with session_file")
    @allure.description("TC-CONFIG-004: Test creating config from YAML file with session_file.")
    def test_from_yaml_with_file_session(
        self,
        yaml_config_file_with_file_session: str,
        yaml_config_data_with_file_session: dict,
    ) -> None:
        """
        Test creating config from YAML file with session_file.

        Args:
            yaml_config_file_with_file_session: Path to YAML config file with session_file.
            yaml_config_data_with_file_session: Parsed YAML config data.
        """
        with allure.step("Load Config from YAML file with session_file"):
            config = Config.from_yaml(yaml_config_file_with_file_session)
        with allure.step("Verify values are loaded correctly"):
            assert config.timeout == yaml_config_data_with_file_session.get("timeout"), "Timeout should match"
            assert config.retry_count == yaml_config_data_with_file_session.get("retry_count"), (
                "Retry count should match"
            )
            assert config.retry_delay == yaml_config_data_with_file_session.get("retry_delay"), (
                "Retry delay should match"
            )
            assert config.log_level == yaml_config_data_with_file_session.get("log_level"), "Log level should match"

    @mark.unit
    @allure.title("TC-CONFIG-033: Create config from YAML file with mini app settings")
    @allure.description("TC-CONFIG-033: Test creating config from YAML file with mini app settings.")
    def test_from_yaml_with_mini_app(
        self, yaml_config_file_with_mini_app: str, yaml_config_data_with_mini_app: dict
    ) -> None:
        """
        Test creating config from YAML file with mini app settings.

        Args:
            yaml_config_file_with_mini_app: Path to YAML config file with mini app settings.
            yaml_config_data_with_mini_app: Parsed YAML config data.
        """
        with allure.step("Load Config from YAML file with mini app settings"):
            config = Config.from_yaml(yaml_config_file_with_mini_app)
        with allure.step("Verify all values from YAML are loaded correctly"):
            assert config.base_url == yaml_config_data_with_mini_app.get("base_url"), "Base URL should match"
            assert config.timeout == yaml_config_data_with_mini_app.get("timeout"), "Timeout should match"
            assert config.retry_count == yaml_config_data_with_mini_app.get("retry_count"), "Retry count should match"
            assert config.retry_delay == yaml_config_data_with_mini_app.get("retry_delay"), "Retry delay should match"
            assert config.log_level == yaml_config_data_with_mini_app.get("log_level"), "Log level should match"
            assert config.browser_headless == yaml_config_data_with_mini_app.get("browser_headless", True), (
                "Browser headless should match"
            )
            assert config.browser_timeout == yaml_config_data_with_mini_app.get("browser_timeout", 30000), (
                "Browser timeout should match"
            )

    @mark.unit
    @allure.title("TC-CONFIG-037: Create config from invalid YAML file")
    @allure.description("TC-CONFIG-037: Test creating config from invalid YAML file.")
    @mark.unit
    @allure.title("TC-CONFIG-037: Create config from invalid YAML file")
    @allure.description("TC-CONFIG-037: Test creating config from invalid YAML file.")
    def test_from_yaml_invalid_file(self, yaml_config_file_invalid: str) -> None:
        """
        Test creating config from invalid YAML file.

        Args:
            yaml_config_file_invalid: Path to invalid YAML config file.
        """
        with allure.step("Attempt to load Config from invalid YAML file"):
            with raises(ValueError):
                Config.from_yaml(yaml_config_file_invalid)

    @mark.unit
    @allure.title("TC-CONFIG-031: Create config from YAML file missing session")
    @allure.description("TC-CONFIG-031: Test creating config from YAML file missing session.")
    def test_from_yaml_missing_session(self, yaml_config_file_missing_session: str) -> None:
        """
        Test creating config from YAML file missing session.

        Args:
            yaml_config_file_missing_session: Path to YAML config file missing session.
        """
        with allure.step("Load Config from YAML file (should use defaults if missing fields)"):
            # Config should load successfully with defaults if fields are missing
            config = Config.from_yaml(yaml_config_file_missing_session)
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @allure.title("TC-CONFIG-035: Create config from nonexistent YAML file")
    @allure.description("TC-CONFIG-035: Test creating config from nonexistent YAML file.")
    def test_from_yaml_nonexistent_file(self) -> None:
        """
        Test creating config from nonexistent YAML file.
        """
        with allure.step("Attempt to load Config from nonexistent file"):
            with raises(FileNotFoundError, match="Configuration file not found"):
                Config.from_yaml("nonexistent_config.yaml")

    @mark.unit
    @allure.title("TC-CONFIG-036: Create config from YAML file with invalid format")
    @allure.description("TC-CONFIG-036: Test creating config from YAML file with invalid format.")
    def test_from_yaml_invalid_yaml_format(self, yaml_config_file_invalid_format: str) -> None:
        """
        Test creating config from YAML file with invalid format.

        Args:
            yaml_config_file_invalid_format: Path to invalid YAML config file format.
        """
        with allure.step("Attempt to load Config from invalid YAML format"):
            with raises(ValueError, match="Failed to load configuration"):
                Config.from_yaml(yaml_config_file_invalid_format)

    @mark.unit
    @allure.title("TC-CONFIG-036: Create config from empty YAML file")
    @allure.description("TC-CONFIG-036: Test creating config from empty YAML file.")
    def test_from_yaml_empty_file(self, yaml_config_file_empty: str) -> None:
        """
        Test creating config from empty YAML file.

        Args:
            yaml_config_file_empty: Path to empty YAML config file.
        """
        with allure.step("Attempt to load Config from empty YAML file"):
            with raises(ValueError, match="YAML file must contain a dictionary"):
                Config.from_yaml(yaml_config_file_empty)


# ============================================================================
# V. Параметризованные тесты валидации
# ============================================================================


class TestConfigValidationParametrized:
    """Test Config validation with parametrized tests."""

    @mark.unit
    @mark.parametrize("timeout", [0, 301, -5])
    @allure.title("TC-CONFIG-006: Invalid timeout values")
    @allure.description("TC-CONFIG-006: Test invalid timeout values.")
    def test_config_invalid_api_id(self, timeout: int) -> None:
        """Test invalid timeout values."""
        with allure.step(f"Attempt to create Config with invalid timeout={timeout}"):
            with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
                Config(
                    base_url="https://example.com",
                    timeout=timeout,
                )

    @mark.unit
    @mark.parametrize("timeout", [30, 60, 120])
    @allure.title("TC-CONFIG-009: Valid timeout values")
    @allure.description("TC-CONFIG-009: Test valid timeout values.")
    def test_config_valid_api_hash_length(self, timeout: int) -> None:
        """Test valid timeout values."""
        with allure.step(f"Create Config with timeout={timeout}"):
            config = Config(
                base_url="https://example.com",
                timeout=timeout,
            )
        with allure.step("Verify timeout is correct"):
            assert config.timeout == timeout

    @mark.unit
    @mark.parametrize("timeout", [0, 301, -5])
    @allure.title("TC-CONFIG-009: Invalid timeout values")
    @allure.description("TC-CONFIG-009: Test invalid timeout values.")
    def test_config_invalid_api_hash_length(self, timeout: int) -> None:
        """Test invalid timeout values."""
        with allure.step(f"Attempt to create Config with invalid timeout={timeout}"):
            with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
                Config(base_url="https://example.com", timeout=timeout)

    @mark.unit
    @allure.title("TC-CONFIG-011: Configuration (deprecated test)")
    @allure.description("TC-CONFIG-011: Test configuration (deprecated - kept for compatibility).")
    def test_config_api_hash_none(self) -> None:
        """Test configuration (deprecated - kept for compatibility)."""
        with allure.step("Create Config with default values"):
            config = Config()
            # Should create with default values
            assert config.timeout == 30
            assert config.retry_count == 3

    @mark.unit
    @mark.parametrize("timeout", [1, 300])
    @allure.title("TC-CONFIG-014: Valid timeout values")
    @allure.description("TC-CONFIG-014: Test valid timeout values.")
    def test_config_valid_timeout(self, timeout: int) -> None:
        """Test valid timeout values."""
        with allure.step(f"Create Config with timeout={timeout}"):
            config = Config(
                base_url="https://example.com",
                timeout=timeout,
            )
        with allure.step("Verify timeout is set correctly"):
            assert config.timeout == timeout

    @mark.unit
    @mark.parametrize("timeout", [0, 301, -5])
    @allure.title("TC-CONFIG-012: Invalid timeout values")
    @allure.description("TC-CONFIG-012: Test invalid timeout values.")
    def test_config_invalid_timeout(self, timeout: int) -> None:
        """Test invalid timeout values."""
        with allure.step(f"Attempt to create Config with invalid timeout={timeout}"):
            with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
                Config(
                    base_url="https://example.com",
                    timeout=timeout,
                )

    @mark.unit
    @mark.parametrize("retry_count", [0, 5, 10])
    @allure.title("TC-CONFIG-017: Valid retry_count values")
    @allure.description("TC-CONFIG-017: Test valid retry_count values.")
    def test_config_valid_retry_count(self, retry_count: int) -> None:
        """Test valid retry_count values."""
        with allure.step(f"Create Config with retry_count={retry_count}"):
            config = Config(
                base_url="https://example.com",
                retry_count=retry_count,
            )
        with allure.step("Verify retry_count is set correctly"):
            assert config.retry_count == retry_count

    @mark.unit
    @mark.parametrize("retry_count", [-1, 11])
    @allure.title("TC-CONFIG-015: Invalid retry_count values")
    @allure.description("TC-CONFIG-015: Test invalid retry_count values.")
    def test_config_invalid_retry_count(self, retry_count: int) -> None:
        """Test invalid retry_count values."""
        with allure.step(f"Attempt to create Config with invalid retry_count={retry_count}"):
            with raises(ValueError, match="retry_count must be between 0 and 10"):
                Config(
                    base_url="https://example.com",
                    retry_count=retry_count,
                )

    @mark.unit
    @mark.parametrize("retry_delay", [0.1, 5.0, 10.0])
    @allure.title("TC-CONFIG-020: Valid retry_delay values")
    @allure.description("TC-CONFIG-020: Test valid retry_delay values.")
    def test_config_valid_retry_delay(self, retry_delay: float) -> None:
        """Test valid retry_delay values."""
        with allure.step(f"Create Config with retry_delay={retry_delay}"):
            config = Config(
                base_url="https://example.com",
                retry_delay=retry_delay,
            )
        with allure.step("Verify retry_delay is set correctly"):
            assert config.retry_delay == retry_delay

    @mark.unit
    @mark.parametrize("retry_delay", [0.09, 10.01])
    @allure.title("TC-CONFIG-018: Invalid retry_delay values")
    @allure.description("TC-CONFIG-018: Test invalid retry_delay values.")
    def test_config_invalid_retry_delay(self, retry_delay: float) -> None:
        """Test invalid retry_delay values."""
        with allure.step(f"Attempt to create Config with invalid retry_delay={retry_delay}"):
            with raises(ValueError, match="retry_delay must be between 0.1 and 10.0 seconds"):
                Config(
                    base_url="https://example.com",
                    retry_delay=retry_delay,
                )

    @mark.unit
    @mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    @allure.title("TC-CONFIG-024: Valid log_level values")
    @allure.description("TC-CONFIG-024: Test valid log_level values.")
    def test_config_valid_log_level(self, log_level: str) -> None:
        """Test valid log_level values."""
        with allure.step(f"Create Config with log_level={log_level}"):
            config = Config(
                base_url="https://example.com",
                log_level=log_level,
            )
        with allure.step("Verify log_level is set correctly"):
            assert config.log_level == log_level

    @mark.unit
    @mark.parametrize("log_level", ["debug", "Info", "TRACE", "INVALID", ""])
    @allure.title("TC-CONFIG-023: Invalid log_level values")
    @allure.description("TC-CONFIG-023: Test invalid log_level values.")
    def test_config_invalid_log_level(self, log_level: str) -> None:
        """Test invalid log_level values."""
        with allure.step(f"Attempt to create Config with invalid log_level={log_level}"):
            # __post_init__ will raise ValueError for invalid log_level
            with raises(ValueError, match="Invalid log level"):
                Config(
                    base_url="https://example.com",
                    log_level=log_level,  # type: ignore[arg-type]
                )

    @mark.unit
    @allure.title("TC-CONFIG-038: Frozen config raises AttributeError on attribute modification")
    @allure.description("TC-CONFIG-038: Test that frozen config raises AttributeError on attribute modification.")
    def test_config_frozen_attribute_error(self) -> None:
        """Test that frozen config raises AttributeError on attribute modification."""
        with allure.step("Create Config instance"):
            config = Config(
                base_url="https://example.com",
                timeout=30,
            )
        with allure.step("Attempt to modify frozen attribute"):
            with raises(AttributeError):
                config.timeout = 60  # type: ignore


# ============================================================================
# VI. Дополнительные тесты Config.from_env()
# ============================================================================


class TestConfigFromEnvAdditional:
    """Additional tests for Config.from_env() method."""

    @mark.unit
    @allure.title("TC-CONFIG-028: from_env with invalid WA_TIMEOUT")
    @allure.description("TC-CONFIG-028: Test from_env with invalid WA_TIMEOUT.")
    def test_from_env_invalid_timeout(self, monkeypatch) -> None:
        """Test from_env with invalid WA_TIMEOUT."""
        with allure.step("Clear all WA_ environment variables"):
            # Clear all WA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("WA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with invalid WA_TIMEOUT"):
            # Set env vars with invalid WA_TIMEOUT (non-numeric)
            monkeypatch.setenv("WA_TIMEOUT", "invalid")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(ValueError, match="WA_TIMEOUT must be a valid integer"):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-029: from_env with invalid WA_RETRY_COUNT")
    @allure.description("TC-CONFIG-029: Test from_env with invalid WA_RETRY_COUNT.")
    def test_from_env_invalid_retry_count(self, monkeypatch) -> None:
        """Test from_env with invalid WA_RETRY_COUNT."""
        with allure.step("Clear all WA_ environment variables"):
            # Clear all WA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("WA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with invalid WA_RETRY_COUNT"):
            # Set env vars with invalid WA_RETRY_COUNT (non-numeric)
            monkeypatch.setenv("WA_RETRY_COUNT", "invalid")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(ValueError, match="WA_RETRY_COUNT must be a valid integer"):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-030: from_env with non-numeric WA_TIMEOUT")
    @allure.description("TC-CONFIG-030: Test from_env with non-numeric WA_TIMEOUT.")
    def test_from_env_invalid_timeout_non_numeric(self, monkeypatch) -> None:
        """Test from_env with non-numeric WA_TIMEOUT."""
        with allure.step("Clear all WA_ environment variables"):
            # Clear all WA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("WA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with non-numeric WA_TIMEOUT"):
            # Set env vars with non-numeric WA_TIMEOUT
            monkeypatch.setenv("WA_TIMEOUT", "abc")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(ValueError, match="WA_TIMEOUT must be a valid integer"):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-030: from_env with non-numeric WA_RETRY_DELAY")
    @allure.description("TC-CONFIG-030: Test from_env with non-numeric WA_RETRY_DELAY.")
    def test_from_env_invalid_retry_delay_non_numeric(self, monkeypatch) -> None:
        """Test from_env with non-numeric WA_RETRY_DELAY."""
        with allure.step("Clear all WA_ environment variables"):
            # Clear all WA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("WA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with non-numeric WA_RETRY_DELAY"):
            # Set env vars with non-numeric WA_RETRY_DELAY
            monkeypatch.setenv("WA_RETRY_DELAY", "xyz")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(ValueError, match="WA_RETRY_DELAY must be a valid float"):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-022: from_env with invalid WA_LOG_LEVEL")
    @allure.description("TC-CONFIG-022: Test from_env with invalid WA_LOG_LEVEL.")
    def test_from_env_invalid_log_level(self, monkeypatch) -> None:
        """Test from_env with invalid WA_LOG_LEVEL."""
        with allure.step("Clear all WA_ environment variables"):
            # Clear all WA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("WA_"):
                    monkeypatch.delenv(key, raising=False)
        with allure.step("Set env vars with invalid WA_LOG_LEVEL"):
            # Set env vars with invalid WA_LOG_LEVEL
            monkeypatch.setenv("WA_LOG_LEVEL", "INVALID")

        with allure.step("Attempt to create Config.from_env()"):
            with raises(
                ValueError,
                match="Invalid log level",
            ):
                Config.from_env()

    @mark.unit
    @allure.title("TC-CONFIG-027: from_env uses default values when optional env vars are missing")
    @allure.description("TC-CONFIG-027: Test from_env uses default values when optional env vars are missing.")
    def test_from_env_default_values_when_missing(self, monkeypatch) -> None:
        """Test from_env uses default values when optional env vars are missing."""
        with allure.step("Clear all WA_ environment variables"):
            # Clear all WA_ env vars
            for key in list(os.environ.keys()):
                if key.startswith("WA_"):
                    monkeypatch.delenv(key, raising=False)

        with allure.step("Create Config.from_env()"):
            config = Config.from_env()
        with allure.step("Verify default values are used"):
            assert config.timeout == 30, "Default timeout should be 30"
            assert config.retry_count == 3, "Default retry_count should be 3"
            assert config.retry_delay == 1.0, "Default retry_delay should be 1.0"
            assert config.log_level == "INFO", "Default log_level should be INFO"


# ============================================================================
# VII. Дополнительные тесты Config.from_yaml()
# ============================================================================


class TestConfigFromYamlAdditional:
    """Additional tests for Config.from_yaml() method."""

    @mark.unit
    @allure.title("TC-CONFIG-043: from_yaml with null optional fields in YAML")
    @allure.description("TC-CONFIG-043: Test from_yaml with null optional fields in YAML.")
    def test_from_yaml_with_null_optional_fields(self, yaml_config_file_valid: str) -> None:
        """Test from_yaml with null optional fields in YAML."""
        with allure.step("Load Config from YAML file"):
            # This test verifies that None values in YAML are handled correctly
            config = Config.from_yaml(yaml_config_file_valid)
        with allure.step("Verify optional fields can be None"):
            # Config should be created successfully with null optional fields
            assert config is not None
            assert isinstance(config, Config)

    @mark.unit
    @allure.title("TC-CONFIG-014: from_yaml with minimum boundary values")
    @allure.description("TC-CONFIG-014: Test from_yaml with minimum boundary values.")
    def test_from_yaml_boundary_values_min(self) -> None:
        """Test from_yaml with minimum boundary values."""

        with allure.step("Create temporary YAML file with minimum values"):
            yaml_content = """base_url: "https://example.com"
timeout: 1
retry_count: 0
retry_delay: 0.1
log_level: "DEBUG"
browser_headless: false
browser_timeout: 1000
"""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Load Config from YAML with minimum values"):
                config = Config.from_yaml(temp_path)
            with allure.step("Verify minimum boundary values"):
                assert config.timeout == 1
                assert config.retry_count == 0
                assert config.retry_delay == 0.1
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-014: from_yaml with maximum boundary values")
    @allure.description("TC-CONFIG-014: Test from_yaml with maximum boundary values.")
    def test_from_yaml_boundary_values_max(self) -> None:
        """Test from_yaml with maximum boundary values."""

        with allure.step("Create temporary YAML file with maximum values"):
            yaml_content = """base_url: "https://example.com"
timeout: 300
retry_count: 10
retry_delay: 10.0
log_level: "CRITICAL"
browser_headless: false
browser_timeout: 300000
"""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Load Config from YAML with maximum values"):
                config = Config.from_yaml(temp_path)
            with allure.step("Verify maximum boundary values"):
                assert config.timeout == 300
                assert config.retry_count == 10
                assert config.retry_delay == 10.0
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-037: from_yaml with minimal valid YAML")
    @allure.description("TC-CONFIG-037: Test from_yaml with minimal valid YAML.")
    def test_from_yaml_minimal_valid(self) -> None:
        """Test from_yaml with minimal valid YAML."""

        with allure.step("Create temporary YAML file with minimal config"):
            yaml_content = """base_url: "https://example.com"
timeout: 30
"""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Load Config from minimal YAML"):
                config = Config.from_yaml(temp_path)
                assert config.base_url == "https://example.com"
                assert config.timeout == 30
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-006: from_yaml with invalid timeout = 0 in YAML")
    @allure.description("TC-CONFIG-006: Test from_yaml with invalid timeout = 0 in YAML.")
    def test_from_yaml_invalid_timeout_zero(self) -> None:
        """Test from_yaml with invalid timeout = 0 in YAML."""

        with allure.step("Create temporary YAML file with timeout=0"):
            yaml_content = """base_url: "https://example.com"
timeout: 0
"""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Attempt to load Config from YAML with invalid timeout"):
                with raises(ValueError, match="timeout must be between 1 and 300 seconds"):
                    Config.from_yaml(temp_path)
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-023: from_yaml with lowercase log_level in YAML")
    @allure.description("TC-CONFIG-023: Test from_yaml with lowercase log_level in YAML.")
    def test_from_yaml_invalid_log_level_lowercase(self) -> None:
        """Test from_yaml with lowercase log_level in YAML."""

        with allure.step("Create temporary YAML file with invalid log_level"):
            yaml_content = """base_url: "https://example.com"
log_level: "debug"
"""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Attempt to load Config from YAML with invalid log_level"):
                # __post_init__ will raise ValueError for invalid log_level
                with raises(ValueError, match="Invalid log level"):
                    Config.from_yaml(temp_path)
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-044: from_yaml overrides timeout with WA_TIMEOUT env variable")
    @allure.description("TC-CONFIG-044: Test from_yaml overrides timeout with WA_TIMEOUT env variable.")
    def test_from_yaml_override_timeout_from_env(self, monkeypatch) -> None:
        """Test from_yaml overrides timeout with WA_TIMEOUT env variable. TC-CONFIG-044"""

        with allure.step("Create temporary YAML file with timeout"):
            yaml_content = """base_url: "https://example.com"
timeout: 30
"""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Set WA_TIMEOUT environment variable"):
                # Set environment variable
                monkeypatch.setenv("WA_TIMEOUT", "60")

            with allure.step("Load Config from YAML"):
                # Note: from_yaml doesn't override with env vars, it uses YAML values
                config = Config.from_yaml(temp_path)

            with allure.step("Verify timeout is from YAML"):
                # YAML values take precedence
                assert config.timeout == 30
        finally:
            os.unlink(temp_path)

    @mark.unit
    @allure.title("TC-CONFIG-045: from_yaml uses YAML values (env vars don't override YAML)")
    @allure.description("TC-CONFIG-045: Test from_yaml uses YAML values (env vars don't override YAML).")
    def test_from_yaml_uses_yaml_values(self, monkeypatch) -> None:
        """Test from_yaml uses YAML values (env vars don't override YAML). TC-CONFIG-045"""

        with allure.step("Create temporary YAML file with timeout"):
            yaml_content = """base_url: "https://example.com"
timeout: 30
"""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                temp_path = f.name

        try:
            with allure.step("Set WA_TIMEOUT environment variable"):
                # Set environment variable
                monkeypatch.setenv("WA_TIMEOUT", "60")

            with allure.step("Load Config from YAML"):
                config = Config.from_yaml(temp_path)

            with allure.step("Verify timeout is from YAML (env vars don't override YAML)"):
                # YAML values take precedence over env vars
                assert config.timeout == 30
                assert config.timeout != 60
        finally:
            os.unlink(temp_path)


# ============================================================================
# VIII. Дополнительные свойства класса
# ============================================================================


class TestConfigAdditional:
    """Test additional Config class properties."""

    @mark.unit
    @allure.title("TC-CONFIG-001: Config serialization using msgspec.to_builtins")
    @allure.description("TC-CONFIG-001: Test serialization using msgspec.to_builtins.")
    def test_config_serialization_to_builtins(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """Test serialization using msgspec.to_builtins."""
        with allure.step("Create Config instance"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Serialize Config to dict"):
            config_dict = to_builtins(config)
        with allure.step("Verify serialized dict contains all expected fields"):
            assert isinstance(config_dict, dict)
            assert config_dict.get("base_url") == valid_config_data.get("base_url")
            assert config_dict.get("timeout") == valid_config_data.get("timeout")
            assert config_dict.get("retry_count") == valid_config_data.get("retry_count")
            assert config_dict.get("retry_delay") == valid_config_data.get("retry_delay")
            assert config_dict.get("log_level") == valid_config_data.get("log_level")
            assert config_dict.get("browser_headless") == valid_config_data.get("browser_headless")
            assert config_dict.get("browser_timeout") == valid_config_data.get("browser_timeout")

    @mark.unit
    @allure.title("TC-CONFIG-001: Config deserialization from dict using msgspec.convert")
    @allure.description("TC-CONFIG-001: Test deserialization using msgspec.convert.")
    def test_config_deserialization_from_dict(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """Test deserialization using msgspec.convert."""
        with allure.step("Deserialize dict to Config"):
            config = convert(valid_config_data, Config)
        with allure.step("Verify deserialized Config contains all expected fields"):
            assert isinstance(config, Config)
            assert config.base_url == valid_config_data.get("base_url")
            assert config.timeout == valid_config_data.get("timeout")
            assert config.retry_count == valid_config_data.get("retry_count")
            assert config.retry_delay == valid_config_data.get("retry_delay")
            assert config.log_level == valid_config_data.get("log_level")
            assert config.browser_headless == valid_config_data.get("browser_headless")
            assert config.browser_timeout == valid_config_data.get("browser_timeout")

    @mark.unit
    @allure.title("TC-CONFIG-001: Config repr contains class name")
    @allure.description("TC-CONFIG-001: Test that Config repr contains class name.")
    def test_config_repr_contains_class_name(
        self,
        valid_config_data: dict[str, int | str | float],
    ) -> None:
        """Test that repr(config) contains class name."""
        with allure.step("Create Config instance"):
            config = Config(**valid_config_data)  # type: ignore[arg-type]
        with allure.step("Get repr string"):
            repr_str = repr(config)
        with allure.step("Verify repr contains class name"):
            assert "Config" in repr_str


# ============================================================================
# IX. Fallback logging and error handling tests
# ============================================================================


class TestConfigFallbackLogging:
    """Test fallback logging configuration in Config.__post_init__."""

    @mark.unit
    @allure.title("TC-CONFIG-LOGGING-001: Fallback logging configuration with AttributeError")
    @allure.description("TC-CONFIG-LOGGING-001: Test fallback logging configuration when AttributeError occurs.")
    def test_config_fallback_logging_attribute_error(self, monkeypatch) -> None:
        """
        Test fallback logging configuration when AttributeError occurs.

        This test verifies that when accessing logger._core.handlers raises
        AttributeError, the fallback logging path is executed.
        """
        with allure.step("Mock logger._core.handlers to raise AttributeError"):
            # Create a property that raises AttributeError when accessed
            class AttributeErrorProperty:
                def __len__(self):
                    raise AttributeError("No handlers attribute")

            # Patch logger._core.handlers to raise AttributeError
            monkeypatch.setattr(logger._core, "handlers", AttributeErrorProperty())

            with patch.object(logger, "remove") as mock_remove:
                with patch.object(logger, "add") as mock_add:
                    with allure.step("Create Config instance"):
                        Config(
                            base_url="https://example.com",
                            timeout=30,
                            log_level="INFO",
                        )
                    with allure.step("Verify fallback logging was called"):
                        # Fallback path should call remove() and add()
                        mock_remove.assert_called_once()
                        mock_add.assert_called_once()

    @mark.unit
    @allure.title("TC-CONFIG-LOGGING-002: Fallback logging configuration with TypeError")
    @allure.description("TC-CONFIG-LOGGING-002: Test fallback logging configuration when TypeError occurs.")
    def test_config_fallback_logging_type_error(self, monkeypatch) -> None:
        """
        Test fallback logging configuration when TypeError occurs.

        This test verifies that when accessing logger._core.handlers raises
        TypeError, the fallback logging path is executed.
        """
        with allure.step("Mock logger._core.handlers to raise TypeError"):
            # Create a property that raises TypeError when len() is called
            class TypeErrorProperty:
                def __len__(self):
                    raise TypeError("Type error")

            # Patch logger._core.handlers to raise TypeError
            monkeypatch.setattr(logger._core, "handlers", TypeErrorProperty())

            with patch.object(logger, "remove") as mock_remove:
                with patch.object(logger, "add") as mock_add:
                    with allure.step("Create Config instance"):
                        Config(
                            base_url="https://example.com",
                            timeout=30,
                            log_level="INFO",
                        )
                    with allure.step("Verify fallback logging was called"):
                        # Fallback path should call remove() and add()
                        mock_remove.assert_called_once()
                        mock_add.assert_called_once()


class TestConfigFromYamlErrorHandling:
    """Test error handling in Config.from_yaml()."""

    @mark.unit
    @allure.title("TC-CONFIG-YAML-001: Reject from_yaml() with missing PyYAML")
    @allure.description("TC-CONFIG-YAML-001: Test that from_yaml() raises ImportError when PyYAML is not installed.")
    def test_config_from_yaml_missing_pyyaml(self, monkeypatch, tmp_path) -> None:
        """
        Test that from_yaml() raises ImportError when PyYAML is not installed.

        This test verifies that when the yaml module cannot be imported,
        from_yaml() raises an ImportError with an appropriate message.
        """
        with allure.step("Create a temporary YAML file"):
            yaml_file = tmp_path / "config.yaml"
            yaml_file.write_text("base_url: https://example.com\ntimeout: 30\n")

        with allure.step("Mock yaml import to raise ImportError"):
            # Remove yaml from sys.modules if it exists
            yaml_module = sys.modules.pop("yaml", None)
            try:
                # Patch builtins.__import__ to raise ImportError for 'yaml'
                original_import = builtins.__import__

                def mock_import(name, *args, **kwargs):
                    if name == "yaml":
                        raise ImportError("No module named 'yaml'")
                    return original_import(name, *args, **kwargs)

                with patch("builtins.__import__", side_effect=mock_import):
                    with allure.step("Attempt to call Config.from_yaml()"):
                        with raises(ImportError, match="YAML support requires 'pyyaml' library"):
                            Config.from_yaml(str(yaml_file))
            finally:
                # Restore yaml module if it was there
                if yaml_module:
                    sys.modules["yaml"] = yaml_module

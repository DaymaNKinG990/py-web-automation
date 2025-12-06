"""
Configuration management for web automation testing framework.

This module provides the Config class for managing framework configuration
with validation, environment variable support, and YAML file loading.
"""

# Python imports
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from msgspec import Struct, ValidationError
from yaml import SafeLoader, load


class Config(Struct, frozen=True):
    """
    Configuration class for web automation testing framework.

    Provides type-safe configuration management with validation,
    environment variable support, and YAML file loading capabilities.

    Attributes:
        base_url: Base URL for the application under test (optional)
        timeout: Request timeout in seconds (default: 30, range: 1-300)
        retry_count: Number of retry attempts (default: 3, range: 0-10)
        retry_delay: Delay between retries in seconds (default: 1.0, range: 0.1-10.0)
        log_level: Logging level (default: "INFO", valid: DEBUG, INFO, WARNING, ERROR, CRITICAL)
        browser_headless: Run browser in headless mode (default: True)
        browser_timeout: Browser operation timeout in milliseconds (default: 30000)

    Raises:
        ValueError: If validation fails
        TypeError: If required arguments are missing

    Example:
        >>> # Create from parameters
        >>> config = Config(timeout=60, retry_count=5)
        >>> # Create from environment variables
        >>> config = Config.from_env()
        >>> # Create from YAML file
        >>> config = Config.from_yaml("config.yaml")
    """

    # Optional configuration fields with defaults
    base_url: str | None = None
    timeout: int = 30
    retry_count: int = 3
    retry_delay: float = 1.0
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    browser_headless: bool = True
    browser_timeout: int = 30000

    def __post_init__(self) -> None:
        """
        Validate configuration after initialization.

        Performs comprehensive validation of all configuration fields
        to ensure they meet the required constraints.

        Raises:
            ValueError: If any validation fails
        """
        # Validate timeout
        if not (1 <= self.timeout <= 300):
            raise ValueError("timeout must be between 1 and 300 seconds")
        # Validate retry_count
        if not (0 <= self.retry_count <= 10):
            raise ValueError("retry_count must be between 0 and 10")
        # Validate retry_delay
        if not (0.1 <= self.retry_delay <= 10.0):
            raise ValueError("retry_delay must be between 0.1 and 10.0 seconds")
        # Validate browser_timeout
        if not (1000 <= self.browser_timeout <= 300000):
            raise ValueError("browser_timeout must be between 1000 and 300000 milliseconds")
        # Validate log_level (msgspec validates Literal, but we add explicit check for safety)
        if self.log_level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            raise ValueError(
                f"Invalid log level: {self.log_level}. "
                "Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )

    @classmethod
    def from_env(cls) -> Config:
        """
        Create Config instance from environment variables.

        Reads configuration from environment variables with the following prefixes:
        - WA_BASE_URL: Base URL for the application
        - WA_TIMEOUT: Request timeout in seconds (default: 30)
        - WA_RETRY_COUNT: Number of retry attempts (default: 3)
        - WA_RETRY_DELAY: Delay between retries in seconds (default: 1.0)
        - WA_LOG_LEVEL: Logging level (default: "INFO")
        - WA_BROWSER_HEADLESS: Run browser in headless mode (default: "true")
        - WA_BROWSER_TIMEOUT: Browser operation timeout in milliseconds (default: 30000)

        Returns:
            Config: Configuration instance created from environment variables

        Raises:
            ValueError: If environment variables are invalid
            TypeError: If type conversion fails

        Example:
            >>> import os
            >>> os.environ["WA_BASE_URL"] = "https://example.com"
            >>> os.environ["WA_TIMEOUT"] = "60"
            >>> config = Config.from_env()
        """
        env = os.environ
        # Optional fields
        base_url = env.get("WA_BASE_URL")
        browser_headless_str = env.get("WA_BROWSER_HEADLESS", "true").lower()
        browser_headless = browser_headless_str in ("true", "1", "yes")
        # Optional configuration fields
        timeout_str = env.get("WA_TIMEOUT", "30")
        try:
            timeout = int(timeout_str)
        except ValueError as e:
            raise ValueError(f"WA_TIMEOUT must be a valid integer: {e}") from e
        retry_count_str = env.get("WA_RETRY_COUNT", "3")
        try:
            retry_count = int(retry_count_str)
        except ValueError as e:
            raise ValueError(f"WA_RETRY_COUNT must be a valid integer: {e}") from e

        retry_delay_str = env.get("WA_RETRY_DELAY", "1.0")
        try:
            retry_delay = float(retry_delay_str)
        except ValueError as e:
            raise ValueError(f"WA_RETRY_DELAY must be a valid float: {e}") from e
        browser_timeout_str = env.get("WA_BROWSER_TIMEOUT", "30000")
        try:
            browser_timeout = int(browser_timeout_str)
        except ValueError as e:
            raise ValueError(f"WA_BROWSER_TIMEOUT must be a valid integer: {e}") from e
        log_level = env.get("WA_LOG_LEVEL", "INFO").upper()
        if log_level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            raise ValueError(
                f"Invalid log level: {log_level}. "
                "Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )
        return cls(
            base_url=base_url,
            timeout=timeout,
            retry_count=retry_count,
            retry_delay=retry_delay,
            log_level=log_level,  # type: ignore[arg-type]
            browser_headless=browser_headless,
            browser_timeout=browser_timeout,
        )

    @classmethod
    def from_yaml(cls, file_path: str) -> Config:
        """
        Create Config instance from YAML file.

        Loads configuration from a YAML file.

        Args:
            file_path: Path to YAML configuration file

        Returns:
            Config: Configuration instance created from YAML file

        Raises:
            FileNotFoundError: If the YAML file does not exist
            ValueError: If the YAML file is invalid or validation fails
            yaml.YAMLError: If YAML parsing fails

        Example:
            >>> config = Config.from_yaml("config.yaml")
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        try:
            with path.open(encoding="utf-8") as f:
                data = load(f, Loader=SafeLoader)
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {e}") from e
        if not isinstance(data, dict):
            raise ValueError(f"YAML file must contain a dictionary, got {type(data)}")
        # Convert to Config instance
        try:
            return cls(**data)
        except (TypeError, ValidationError) as e:
            raise ValueError(f"Invalid configuration data: {e}") from e

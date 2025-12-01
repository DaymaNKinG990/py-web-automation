"""
Fixtures for BaseClient testing.
"""

from pytest import fixture

from py_web_automation.clients.base_client import BaseClient
from py_web_automation.config import Config


def _get_base_config_data() -> dict:
    """Get base config data for creating Config instances."""
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
def valid_config() -> Config:
    """Create a valid Config instance."""
    return Config(**_get_base_config_data())


@fixture
def base_client_urls():
    """Valid URLs for BaseClient testing."""
    return [
        "https://example.com/app",
        "https://api.example.com/v1",
        "http://localhost:8080",
        "https://test.example.com",
    ]


@fixture
def invalid_urls():
    """Invalid URLs for BaseClient testing."""
    return [
        None,  # TypeError expected
        123,  # TypeError expected
        [],  # TypeError expected
    ]


@fixture
def base_client_with_config(valid_config):
    """Create BaseClient with valid config."""
    return BaseClient("https://example.com/app", valid_config)


@fixture
def base_client_without_config():
    """Create BaseClient without config (will use default Config)."""
    # Note: Config() now has defaults for all fields, so this will work
    return BaseClient("https://example.com/app", None)

"""
Fixtures for Metrics testing with automatic cleanup.
"""

# Python imports
from pytest import fixture

# Local imports
from py_web_automation.clients.api_clients.http_client.metrics import Metrics


@fixture
def metrics() -> Metrics:
    """Create Metrics instance with automatic cleanup."""
    metrics_instance = Metrics()
    yield metrics_instance
    metrics_instance.reset()


"""
Fixtures for Middleware testing with automatic cleanup.
"""

# Python imports
from pytest import fixture

# Local imports
from py_web_automation.clients.api_clients.http_client.middleware import MiddlewareChain
from py_web_automation.clients.api_clients.http_client.middleware.context import (
    _HttpRequestContext as RequestContext,
    _HttpResponseContext as ResponseContext,
)
from py_web_automation.clients.api_clients.http_client.metrics import Metrics
from py_web_automation.clients.api_clients.http_client import HttpResult


@fixture
def middleware_chain() -> MiddlewareChain:
    """Create MiddlewareChain instance with automatic cleanup."""
    chain = MiddlewareChain()
    yield chain
    chain._middleware.clear()


@fixture
def metrics_for_middleware() -> Metrics:
    """Create Metrics instance for middleware testing with automatic cleanup."""
    metrics_instance = Metrics()
    yield metrics_instance
    metrics_instance.reset()


@fixture
def request_context() -> RequestContext:
    """Create RequestContext with automatic metadata cleanup."""
    context = RequestContext(method="GET", url="/test")
    yield context
    context.metadata.clear()


@fixture
def response_context() -> ResponseContext:
    """Create ResponseContext with automatic metadata cleanup."""
    result = HttpResult(
        endpoint="/test",
        method="GET",
        status_code=200,
        response_time=0.5,
        success=True,
        redirect=False,
        client_error=False,
        server_error=False,
        informational=False,
    )
    context = ResponseContext(result)
    yield context
    context.metadata.clear()

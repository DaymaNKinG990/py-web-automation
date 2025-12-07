"""
Middleware usage example.

This example demonstrates how to use middleware for request/response
interception, logging, metrics, and authentication.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.api_clients.http_client.metrics import Metrics
from py_web_automation.clients.api_clients.http_client.middleware import (
    AuthMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
    Middleware,
    MiddlewareChain,
)
from py_web_automation.clients.api_clients.http_client.middleware.context import (
    _HttpRequestContext,
    _HttpResponseContext,
)


async def main():
    """Main function demonstrating middleware usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Middleware Examples ===\n")

        # Example 1: Using Built-in Middleware
        print("1. Using built-in middleware...")
        metrics = Metrics()
        chain = MiddlewareChain()
        chain.add(LoggingMiddleware())
        chain.add(MetricsMiddleware(metrics))

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/users", method="GET")
            print(f"   Status: {result.status_code}")
            print(f"   Metrics - Requests: {metrics.request_count}")

        # Example 2: Custom Middleware
        print("\n2. Creating custom middleware...")

        class CustomHeaderMiddleware(Middleware):
            """Add custom header to all requests."""

            async def process_request(self, context: _HttpRequestContext) -> None:
                context.headers["X-Custom-Middleware"] = "enabled"
                print(f"   Added custom header to {context.method} {context.url}")

            async def process_response(self, context: _HttpResponseContext) -> None:
                print(f"   Response status: {context.result.status_code}")

        chain = MiddlewareChain()
        chain.add(CustomHeaderMiddleware())
        chain.add(LoggingMiddleware())

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/data", method="GET")
            print(f"   Status: {result.status_code}")

        # Example 3: Authentication Middleware
        print("\n3. Using authentication middleware...")
        auth_middleware = AuthMiddleware(token="your-token", token_type="Bearer")
        chain = MiddlewareChain()
        chain.add(auth_middleware)
        chain.add(LoggingMiddleware())

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/protected", method="GET")
            print(f"   Status: {result.status_code}")

        # Example 4: Metrics Middleware
        print("\n4. Using metrics middleware...")
        metrics = Metrics()
        chain = MiddlewareChain()
        chain.add(MetricsMiddleware(metrics))
        chain.add(LoggingMiddleware())

        async with HttpClient(base_url, config, middleware=chain) as api:
            for i in range(3):
                await api.make_request(f"/api/endpoint-{i}", method="GET")

            print(f"   Total requests: {metrics.request_count}")
            print(f"   Successful requests: {metrics.success_count}")
            print(f"   Failed requests: {metrics.error_count}")
            if metrics.request_count > 0:
                print(f"   Average latency: {metrics.average_latency:.3f}s")

        # Example 5: Request Modification Middleware
        print("\n5. Modifying requests with middleware...")

        class RequestModifierMiddleware(Middleware):
            """Modify request parameters."""

            async def process_request(self, context: _HttpRequestContext) -> None:
                # Add query parameter
                context.params["timestamp"] = "1234567890"
                # Modify header
                context.headers["X-Request-ID"] = "custom-id-123"
                print(f"   Modified request: {context.method} {context.url}")

            async def process_response(self, context: _HttpResponseContext) -> None:
                pass

        chain = MiddlewareChain()
        chain.add(RequestModifierMiddleware())
        chain.add(LoggingMiddleware())

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/data", method="GET")
            print(f"   Status: {result.status_code}")

        # Example 6: Response Modification Middleware
        print("\n6. Modifying responses with middleware...")

        class ResponseModifierMiddleware(Middleware):
            """Add metadata to responses."""

            async def process_request(self, context: _HttpRequestContext) -> None:
                pass

            async def process_response(self, context: _HttpResponseContext) -> None:
                # Add custom metadata
                context.metadata_context["processed_by"] = "ResponseModifierMiddleware"
                context.metadata_context["timestamp"] = "1234567890"
                print(f"   Added metadata to response: {context.result.status_code}")

        chain = MiddlewareChain()
        chain.add(ResponseModifierMiddleware())
        chain.add(LoggingMiddleware())

        async with HttpClient(base_url, config, middleware=chain) as api:
            result = await api.make_request("/api/data", method="GET")
            print(f"   Status: {result.status_code}")

        print("\n=== Middleware Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

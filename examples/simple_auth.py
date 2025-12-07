"""
Simple authentication example for Web Automation Framework.

This example demonstrates basic authentication using API tokens with AuthMiddleware.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.api_clients.http_client.middleware import (
    AuthMiddleware,
    MiddlewareChain,
)


async def main():
    """Simple example showing token-based authentication."""

    # Create configuration
    config = Config(
        timeout=30,
        retry_count=3,
        retry_delay=1.0,
        log_level="INFO",
    )

    base_url = "https://api.example.com"
    auth_token = "your-api-token-here"

    try:
        print("=== Simple Authentication Example ===")

        # Setup authentication middleware
        auth_middleware = AuthMiddleware(token=auth_token, token_type="Bearer")
        middleware_chain = MiddlewareChain()
        middleware_chain.add(auth_middleware)

        async with HttpClient(base_url, config, middleware=middleware_chain) as api:
            print("✅ Authentication middleware configured")

            # Make authenticated request
            result = await api.make_request("/api/protected", method="GET")
            print(f"Protected endpoint: {'✅ OK' if result.success else '❌ FAILED'}")
            print(f"Status Code: {result.status_code}")

            if result.success:
                print("✅ Successfully authenticated!")
                data = result.json()
                print(f"Response data: {data}")

            # Clear authentication token
            auth_middleware.clear_token()
            print("✅ Authentication token cleared")

            # Try request without authentication
            result = await api.make_request("/api/protected", method="GET")
            if not result.success:
                print("✅ Unauthenticated request correctly rejected")
            else:
                print("⚠️ Unauthenticated request was accepted (unexpected)")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Web Automation Framework - Simple Authentication Example")
    print("=" * 60)

    asyncio.run(main())

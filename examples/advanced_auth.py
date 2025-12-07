"""
Advanced authentication example for Web Automation Framework.

Demonstrates various authentication patterns including token management,
dynamic token updates, and error handling using AuthMiddleware.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.api_clients.http_client.middleware import (
    AuthMiddleware,
    MiddlewareChain,
)
from py_web_automation.exceptions import (
    AuthenticationError,
    ConnectionError,
    WebAutomationError,
)


async def token_based_auth():
    """Token-based authentication example."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"
    token = "your-bearer-token-here"

    print("=== Token-Based Authentication ===")

    # Setup authentication middleware
    auth_middleware = AuthMiddleware(token=token, token_type="Bearer")
    middleware_chain = MiddlewareChain()
    middleware_chain.add(auth_middleware)

    async with HttpClient(base_url, config, middleware=middleware_chain) as api:
        print("✅ Bearer token set via AuthMiddleware")

        # Make authenticated request
        result = await api.make_request("/api/user/profile", method="GET")
        print(f"Profile request: {'✅ OK' if result.success else '❌ FAILED'}")
        print(f"Status: {result.status_code}")

        # Clear token
        auth_middleware.clear_token()
        print("✅ Token cleared")


async def request_builder_auth():
    """Authentication using RequestBuilder with AuthMiddleware."""

    config = Config(timeout=30)
    base_url = "https://api.example.com"
    token = "your-api-token"

    print("\n=== Request Builder Authentication ===")

    # Setup authentication middleware
    auth_middleware = AuthMiddleware(token=token, token_type="Bearer")
    middleware_chain = MiddlewareChain()
    middleware_chain.add(auth_middleware)

    async with HttpClient(base_url, config, middleware=middleware_chain) as api:
        builder = api.build_request()

        # Build request with authentication (token added automatically by middleware)
        result = await builder.get("/api/data").execute()

        print(f"Request with auth middleware: {'✅ OK' if result.success else '❌ FAILED'}")

        # Alternative: Manual header (if needed for specific request)
        result = await builder.get("/api/data").header("Authorization", f"Bearer {token}").execute()

        print(f"Request with manual header: {'✅ OK' if result.success else '❌ FAILED'}")


async def error_handling_auth():
    """Error handling for authentication failures."""

    config = Config(timeout=30)
    base_url = "https://api.example.com"

    print("\n=== Authentication Error Handling ===")

    # Setup authentication middleware with invalid token
    auth_middleware = AuthMiddleware(token="invalid-token", token_type="Bearer")
    middleware_chain = MiddlewareChain()
    middleware_chain.add(auth_middleware)

    async with HttpClient(base_url, config, middleware=middleware_chain) as api:
        try:
            result = await api.make_request("/api/protected", method="GET")

            if result.status_code == 401:
                print("✅ Correctly detected 401 Unauthorized")
            elif result.status_code == 403:
                print("✅ Correctly detected 403 Forbidden")
            else:
                print(f"⚠️ Unexpected status: {result.status_code}")

        except AuthenticationError as e:
            print(f"✅ Authentication error caught: {e}")
        except ConnectionError as e:
            print(f"❌ Connection error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


async def multiple_auth_methods():
    """Demonstrate multiple authentication methods."""

    config = Config(timeout=30)
    base_url = "https://api.example.com"

    print("\n=== Multiple Authentication Methods ===")

    # Method 1: Bearer token via AuthMiddleware
    auth_middleware = AuthMiddleware(token="bearer-token", token_type="Bearer")
    middleware_chain = MiddlewareChain()
    middleware_chain.add(auth_middleware)

    async with HttpClient(base_url, config, middleware=middleware_chain) as api:
        result1 = await api.make_request("/api/endpoint1", method="GET")
        print(f"Bearer token via middleware: {'✅ OK' if result1.success else '❌ FAILED'}")

    # Method 2: Custom header (no middleware needed)
    async with HttpClient(base_url, config) as api:
        result2 = await api.make_request(
            "/api/endpoint2",
            method="GET",
            headers={"X-API-Key": "custom-api-key"},
        )
        print(f"Custom header: {'✅ OK' if result2.success else '❌ FAILED'}")

    # Method 3: Request builder with manual header
    async with HttpClient(base_url, config) as api:
        builder = api.build_request()
        result3 = await builder.get("/api/endpoint3").header("Authorization", "Token token-value").execute()
        print(f"Request builder with manual header: {'✅ OK' if result3.success else '❌ FAILED'}")

    # Method 4: Dynamic token update
    auth_middleware2 = AuthMiddleware(token="initial-token", token_type="Bearer")
    middleware_chain2 = MiddlewareChain()
    middleware_chain2.add(auth_middleware2)

    async with HttpClient(base_url, config, middleware=middleware_chain2) as api:
        # Update token dynamically
        auth_middleware2.update_token("refreshed-token")
        result4 = await api.make_request("/api/endpoint4", method="GET")
        print(f"Dynamic token update: {'✅ OK' if result4.success else '❌ FAILED'}")


async def main():
    """Run all authentication examples."""

    print("Web Automation Framework - Advanced Authentication Examples")
    print("=" * 60)

    try:
        await token_based_auth()
        await request_builder_auth()
        await error_handling_auth()
        await multiple_auth_methods()

        print("\n" + "=" * 60)
        print("✅ All authentication examples completed!")

    except WebAutomationError as e:
        print(f"\n❌ Framework error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

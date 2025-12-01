"""
Advanced authentication example for Web Automation Framework.

Demonstrates various authentication patterns including token management,
request builder with auth, and error handling.
"""

import asyncio

from py_web_automation import ApiClient, Config, RequestBuilder
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

    async with ApiClient(base_url, config) as api:
        # Set token
        api.set_auth_token(token, token_type="Bearer")
        print("✅ Bearer token set")

        # Make authenticated request
        result = await api.make_request("/api/user/profile", method="GET")
        print(f"Profile request: {'✅ OK' if result.success else '❌ FAILED'}")
        print(f"Status: {result.status_code}")

        # Clear token
        api.clear_auth_token()
        print("✅ Token cleared")


async def request_builder_auth():
    """Authentication using RequestBuilder."""

    config = Config(timeout=30)
    base_url = "https://api.example.com"
    token = "your-api-token"

    print("\n=== Request Builder Authentication ===")

    async with ApiClient(base_url, config) as api:
        builder = RequestBuilder(api)

        # Build request with authentication
        result = await builder.get("/api/data").header("Authorization", f"Bearer {token}").execute()

        print(f"Request with auth header: {'✅ OK' if result.success else '❌ FAILED'}")

        # Alternative: Use auth method
        result = await builder.get("/api/data").auth(token).execute()

        print(f"Request with auth method: {'✅ OK' if result.success else '❌ FAILED'}")


async def error_handling_auth():
    """Error handling for authentication failures."""

    config = Config(timeout=30)
    base_url = "https://api.example.com"

    print("\n=== Authentication Error Handling ===")

    async with ApiClient(base_url, config) as api:
        # Test with invalid token
        api.set_auth_token("invalid-token", token_type="Bearer")

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

    async with ApiClient(base_url, config) as api:
        # Method 1: Bearer token
        api.set_auth_token("bearer-token", token_type="Bearer")
        result1 = await api.make_request("/api/endpoint1", method="GET")
        print(f"Bearer token: {'✅ OK' if result1.success else '❌ FAILED'}")
        api.clear_auth_token()

        # Method 2: Custom header
        result2 = await api.make_request(
            "/api/endpoint2",
            method="GET",
            headers={"X-API-Key": "custom-api-key"},
        )
        print(f"Custom header: {'✅ OK' if result2.success else '❌ FAILED'}")

        # Method 3: Request builder with auth
        builder = RequestBuilder(api)
        result3 = await builder.get("/api/endpoint3").header("Authorization", "Token token-value").execute()
        print(f"Request builder: {'✅ OK' if result3.success else '❌ FAILED'}")


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

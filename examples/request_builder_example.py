"""
RequestBuilder usage example.

This example demonstrates how to use RequestBuilder for constructing
complex HTTP requests with a fluent API.
"""

import asyncio

from py_web_automation import ApiClient, Config, RequestBuilder


async def main():
    """Main function demonstrating RequestBuilder usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== RequestBuilder Examples ===\n")

        async with ApiClient(base_url, config) as api:
            builder = RequestBuilder(api)

            # Example 1: Simple GET Request
            print("1. Simple GET request...")
            result = await builder.get("/api/users").execute()
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

            # Example 2: GET with Query Parameters
            print("\n2. GET request with query parameters...")
            result = await builder.get("/api/users").params(page=1, limit=10, sort="name").execute()
            print(f"   Status: {result.status_code}")
            print("   URL would include: ?page=1&limit=10&sort=name")

            # Example 3: POST with JSON Body
            print("\n3. POST request with JSON body...")
            result = await builder.post("/api/users").body({"name": "John Doe", "email": "john@example.com"}).execute()
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

            # Example 4: PUT with Headers
            print("\n4. PUT request with custom headers...")
            result = await (
                builder.put("/api/users/1")
                .body({"name": "Jane Doe", "email": "jane@example.com"})
                .header("X-Custom-Header", "value")
                .header("Content-Type", "application/json")
                .execute()
            )
            print(f"   Status: {result.status_code}")

            # Example 5: DELETE Request
            print("\n5. DELETE request...")
            result = await builder.delete("/api/users/1").execute()
            print(f"   Status: {result.status_code}")

            # Example 6: PATCH Request
            print("\n6. PATCH request...")
            result = await builder.patch("/api/users/1").body({"email": "newemail@example.com"}).execute()
            print(f"   Status: {result.status_code}")

            # Example 7: Request with Authentication
            print("\n7. Request with authentication...")
            result = await builder.get("/api/protected").auth("your-token-here").execute()
            print(f"   Status: {result.status_code}")

            # Example 8: Complex Request with All Options
            print("\n8. Complex request with all options...")
            result = await (
                builder.post("/api/users")
                .params(validate=True)
                .body(
                    {
                        "name": "Complex User",
                        "email": "complex@example.com",
                        "metadata": {"source": "api", "version": "1.0"},
                    }
                )
                .header("X-Request-ID", "12345")
                .header("X-Client-Version", "2.0")
                .auth("bearer-token", token_type="Bearer")
                .execute()
            )
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

            # Example 9: Method Chaining
            print("\n9. Method chaining example...")
            result = await (
                builder.reset()
                .get("/api/data")
                .param("filter", "active")
                .param("sort", "date")
                .header("Accept", "application/json")
                .execute()
            )
            print(f"   Status: {result.status_code}")

            # Example 10: Reset Builder
            print("\n10. Resetting builder...")
            builder.reset()
            result = await builder.get("/api/status").execute()
            print(f"   Status: {result.status_code}")

        print("\n=== RequestBuilder Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

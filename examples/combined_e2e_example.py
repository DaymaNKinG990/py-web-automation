"""
End-to-end example combining multiple framework features.

This example demonstrates a comprehensive workflow using
multiple clients, middleware, retry, and other framework features together.
"""

import asyncio

import msgspec

from py_web_automation import Config
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.api_clients.http_client.metrics import Metrics
from py_web_automation.clients.api_clients.http_client.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    MiddlewareChain,
)
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient
from py_web_automation.clients.ui_clients import AsyncUiClient


class UserResponse(msgspec.Struct):
    """User response schema."""

    id: int
    name: str
    email: str
    active: bool = True


async def main():
    """Main function demonstrating combined E2E workflow."""

    config = Config(
        timeout=30,
        retry_count=3,
        retry_delay=1.0,
        log_level="INFO",
        browser_headless=True,
    )

    api_url = "https://api.example.com"
    web_url = "https://example.com"

    try:
        print("=== Combined E2E Example ===\n")

        # Setup shared components
        metrics = Metrics()

        # Setup middleware chain
        middleware_chain = MiddlewareChain()
        middleware_chain.add(LoggingMiddleware())
        middleware_chain.add(MetricsMiddleware(metrics))

        # Example 1: API Testing with All Features
        print("1. API testing with middleware...")
        async with HttpClient(api_url, config, middleware=middleware_chain) as api:
            result = await api.make_request("/api/users", method="GET")
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

        # Example 2: GraphQL with Validation
        print("\n2. GraphQL query with response validation...")
        async with GraphQLClient(api_url, config) as gql:
            query = """
            query {
                users {
                    id
                    name
                    email
                }
            }
            """
            result = await gql.query(query)

            if result.success:
                try:
                    # Validate response structure
                    data = result.json()
                    if data and "data" in data and "users" in data["data"]:
                        print(f"   Found {len(data['data']['users'])} users")
                except Exception as e:
                    print(f"   Validation error: {e}")

        # Example 3: Request Builder with Features
        print("\n3. Request builder with authentication...")
        async with HttpClient(api_url, config, middleware=middleware_chain) as api:
            builder = api.build_request()
            result = (
                await builder.get("/api/user/1")
                .header("Authorization", "Bearer bearer-token")
                .header("X-Request-ID", "e2e-test-123")
                .execute()
            )

            if result.success:
                try:
                    data = result.json()
                    if data:
                        print(f"   User data retrieved")
                except Exception as e:
                    print(f"   Validation failed: {e}")

        # Example 4: Database Operations
        print("\n4. Database operations with query builder...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            # Create table
            await db.execute_command(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    active BOOLEAN DEFAULT 1
                )
                """
            )

            # Insert using query builder
            query, params = db.query().insert("users", name="E2E User", email="e2e@example.com")._build()
            await db.execute_command(query, params)

            # Query using query builder
            query, params = db.query().select("*").from_table("users").where("active", "=", True)._build()
            results = await db.execute_query(query, params)
            print(f"   Found {len(results)} active users")

        # Example 5: UI Testing
        print("\n5. UI testing...")
        async with AsyncUiClient(web_url, config) as ui:
            await ui.setup_browser()
            if ui.page:
                await ui.page.goto(web_url, wait_until="networkidle")
            print("   Navigated to web application")
            await ui.take_screenshot("e2e_test.png")

        # Example 6: Metrics Summary
        print("\n6. Metrics summary...")
        print(f"   Total requests: {metrics.request_count}")
        print(f"   Success rate: {metrics.success_rate:.1f}%")
        print(f"   Average latency: {metrics.avg_latency:.3f}s")
        print(f"   Requests per second: {metrics.requests_per_second:.2f}")

        print("\n=== Combined E2E Example Completed ===")
        print("\nThis example demonstrated:")
        print("  ✅ API client with middleware")
        print("  ✅ GraphQL client with validation")
        print("  ✅ Request builder with authentication")
        print("  ✅ Database operations with query builder")
        print("  ✅ UI testing")
        print("  ✅ Metrics collection and analysis")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

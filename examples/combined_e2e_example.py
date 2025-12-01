"""
End-to-end example combining multiple framework features.

This example demonstrates a comprehensive workflow using
multiple clients, middleware, caching, retry, circuit breaker,
and other framework features together.
"""

import asyncio

import msgspec

from py_web_automation import (
    ApiClient,
    Config,
    DBClient,
    GraphQLClient,
    RequestBuilder,
    UiClient,
)
from py_web_automation.cache import ResponseCache
from py_web_automation.circuit_breaker import CircuitBreaker
from py_web_automation.metrics import Metrics
from py_web_automation.middleware import LoggingMiddleware, MetricsMiddleware, MiddlewareChain
from py_web_automation.rate_limit import RateLimiter
from py_web_automation.retry import retry_on_connection_error
from py_web_automation.validators import validate_api_result


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
        cache = ResponseCache(default_ttl=300)
        rate_limiter = RateLimiter(max_requests=10, window=60)
        circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=30.0)

        # Setup middleware chain
        middleware_chain = MiddlewareChain()
        middleware_chain.add(LoggingMiddleware())
        middleware_chain.add(MetricsMiddleware(metrics))

        # Example 1: API Testing with All Features
        print("1. API testing with middleware, cache, rate limiting, and circuit breaker...")
        async with ApiClient(api_url, config) as api:
            api._middleware = middleware_chain
            api._cache = cache
            api._rate_limiter = rate_limiter

            @retry_on_connection_error(max_attempts=3, delay=1.0)
            async def make_request_with_features():
                return await circuit_breaker.call(api.make_request, "/api/users", method="GET")

            result = await make_request_with_features()
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
                    if "data" in data and "users" in data["data"]:
                        print(f"   Found {len(data['data']['users'])} users")
                except Exception as e:
                    print(f"   Validation error: {e}")

        # Example 3: Request Builder with Features
        print("\n3. Request builder with authentication and validation...")
        async with ApiClient(api_url, config) as api:
            api._middleware = middleware_chain

            builder = RequestBuilder(api)
            result = await (
                builder.get("/api/user/1").auth("bearer-token").header("X-Request-ID", "e2e-test-123").execute()
            )

            if result.success:
                try:
                    user = validate_api_result(result, UserResponse)
                    print(f"   Validated user: {user.name} ({user.email})")
                except Exception as e:
                    print(f"   Validation failed: {e}")

        # Example 4: Database Operations
        print("\n4. Database operations with query builder...")
        from py_web_automation.query_builder import QueryBuilder

        db_client = DBClient.create(
            "sqlite",
            "sqlite:///:memory:",
            config,
            connection_string="sqlite:///:memory:",
        )

        await db_client.connect()

        # Create table
        await db_client.execute_command(
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
        query, params = QueryBuilder().insert("users", name="E2E User", email="e2e@example.com").build()
        await db_client.execute_command(query, params)

        # Query using query builder
        query, params = QueryBuilder().select("*").from_table("users").where("active", "=", True).build()
        results = await db_client.execute_query(query, params)
        print(f"   Found {len(results)} active users")

        await db_client.disconnect()

        # Example 5: UI Testing with Page Objects
        print("\n5. UI testing with page objects...")
        # Note: In real usage, you would import your page objects from your project
        # from your_project.pages import LoginPage, DashboardPage

        async with UiClient(web_url, config) as ui:
            await ui.setup_browser()
            await ui.page.goto(web_url, wait_until="networkidle")
            print("   Navigated to web application")
            # In real usage, you would use your page objects here
            # login_page = LoginPage(ui)
            # await login_page.navigate()

        # Example 6: Metrics Summary
        print("\n6. Metrics summary...")
        print(f"   Total requests: {metrics.request_count}")
        print(f"   Success rate: {metrics.success_rate:.1f}%")
        print(f"   Average latency: {metrics.avg_latency:.3f}s")
        print(f"   Requests per second: {metrics.requests_per_second:.2f}")

        # Example 7: Cache Statistics
        print("\n7. Cache statistics...")
        print(f"   Cache entries: {len(cache._cache)}")
        print(f"   Default TTL: {cache.default_ttl}s")

        # Example 8: Circuit Breaker Status
        print("\n8. Circuit breaker status...")
        print(f"   State: {circuit_breaker.stats.state.value}")
        print(f"   Failures: {circuit_breaker.stats.failures}")
        print(f"   Successes: {circuit_breaker.stats.successes}")

        print("\n=== Combined E2E Example Completed ===")
        print("\nThis example demonstrated:")
        print("  ✅ API client with middleware, cache, rate limiting, circuit breaker")
        print("  ✅ GraphQL client with validation")
        print("  ✅ Request builder with authentication")
        print("  ✅ Database operations with query builder")
        print("  ✅ UI testing with page objects")
        print("  ✅ Metrics collection and analysis")
        print("  ✅ Retry mechanism")
        print("  ✅ Response validation")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

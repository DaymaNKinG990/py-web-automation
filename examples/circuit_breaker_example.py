"""
Circuit breaker usage example.

This example demonstrates how to use CircuitBreaker to prevent
cascading failures by stopping requests to failing services.
"""

import asyncio

from py_web_automation import ApiClient, Config
from py_web_automation.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
)
from py_web_automation.exceptions import ConnectionError


async def main():
    """Main function demonstrating circuit breaker usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Circuit Breaker Examples ===\n")

        # Example 1: Basic Circuit Breaker
        print("1. Basic circuit breaker...")
        breaker = CircuitBreaker(
            failure_threshold=3,
            timeout=10.0,
            success_threshold=2,
            expected_exception=ConnectionError,
        )

        async def make_request_with_breaker():
            async with ApiClient(base_url, config) as api:
                return await breaker.call(api.make_request, "/api/data", method="GET")

        try:
            result = await make_request_with_breaker()
            print(f"   Status: {result.status_code}")
            print(f"   Circuit state: {breaker.stats.state.value}")
        except CircuitBreakerOpenError:
            print("   Circuit is OPEN - service unavailable")
        except Exception as e:
            print(f"   Error: {e}")

        # Example 2: Circuit Breaker State Transitions
        print("\n2. Circuit breaker state transitions...")
        breaker = CircuitBreaker(
            failure_threshold=2,
            timeout=5.0,
            success_threshold=1,
        )

        async def failing_request():
            raise ConnectionError("Service unavailable")

        # Simulate failures to open circuit
        print("   Simulating failures...")
        for i in range(3):
            try:
                await breaker.call(failing_request)
            except CircuitBreakerOpenError:
                print(f"   Attempt {i + 1}: Circuit OPEN")
                break
            except Exception as e:
                print(f"   Attempt {i + 1}: {type(e).__name__}")

        print(f"   Final state: {breaker.stats.state.value}")
        print(f"   Failures: {breaker.stats.failures}")

        # Example 3: Circuit Breaker with Custom Config
        print("\n3. Circuit breaker with custom config...")
        cb_config = CircuitBreakerConfig(
            failure_threshold=5,
            timeout=30.0,
            success_threshold=3,
            expected_exception=ConnectionError,
        )
        breaker = CircuitBreaker(
            failure_threshold=cb_config.failure_threshold,
            timeout=cb_config.timeout,
            success_threshold=cb_config.success_threshold,
            expected_exception=cb_config.expected_exception,
        )

        print(f"   Failure threshold: {breaker.config.failure_threshold}")
        print(f"   Timeout: {breaker.config.timeout}s")
        print(f"   Success threshold: {breaker.config.success_threshold}")

        # Example 4: Circuit Breaker Statistics
        print("\n4. Circuit breaker statistics...")
        breaker = CircuitBreaker(failure_threshold=3, timeout=10.0)

        async def test_request():
            async with ApiClient(base_url, config) as api:
                return await api.make_request("/api/test", method="GET")

        for i in range(5):
            try:
                result = await breaker.call(test_request)
                print(f"   Request {i + 1}: Success - {result.status_code}")
            except CircuitBreakerOpenError:
                print(f"   Request {i + 1}: Circuit OPEN")
            except Exception as e:
                print(f"   Request {i + 1}: {type(e).__name__}")

        stats = breaker.stats
        print("\n   Statistics:")
        print(f"     State: {stats.state.value}")
        print(f"     Failures: {stats.failures}")
        print(f"     Successes: {stats.successes}")
        if stats.last_failure_time:
            print(f"     Last failure: {stats.last_failure_time}")
        if stats.last_success_time:
            print(f"     Last success: {stats.last_success_time}")

        # Example 5: Circuit Breaker with Recovery
        print("\n5. Circuit breaker recovery...")
        breaker = CircuitBreaker(
            failure_threshold=2,
            timeout=2.0,  # Short timeout for demo
            success_threshold=1,
        )

        async def unreliable_request(succeed: bool):
            if succeed:
                async with ApiClient(base_url, config) as api:
                    return await api.make_request("/api/data", method="GET")
            else:
                raise ConnectionError("Service unavailable")

        # Open circuit
        print("   Opening circuit...")
        for _i in range(2):
            try:
                await breaker.call(unreliable_request, False)
            except Exception:
                pass

        print(f"   Circuit state: {breaker.stats.state.value}")

        # Wait for timeout
        print("   Waiting for timeout...")
        await asyncio.sleep(3)

        # Try to recover
        print("   Attempting recovery...")
        try:
            result = await breaker.call(unreliable_request, True)
            print(f"   Recovery successful - Status: {result.status_code}")
            print(f"   Circuit state: {breaker.stats.state.value}")
        except Exception as e:
            print(f"   Recovery failed: {e}")

        print("\n=== Circuit Breaker Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

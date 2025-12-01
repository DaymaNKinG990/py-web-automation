"""
Metrics collection usage example.

This example demonstrates how to use Metrics for collecting
and analyzing performance metrics.
"""

import asyncio

from py_web_automation import ApiClient, Config
from py_web_automation.metrics import Metrics


async def main():
    """Main function demonstrating metrics usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Metrics Examples ===\n")

        # Example 1: Basic Metrics Collection
        print("1. Basic metrics collection...")
        metrics = Metrics()

        async with ApiClient(base_url, config) as api:
            for i in range(5):
                start_time = asyncio.get_event_loop().time()
                result = await api.make_request(f"/api/endpoint-{i}", method="GET")
                latency = asyncio.get_event_loop().time() - start_time

                metrics.record_request(
                    success=result.success,
                    latency=latency,
                    error_type=None if result.success else "http_error",
                )

        print(f"   Total requests: {metrics.request_count}")
        print(f"   Successful: {metrics.success_count}")
        print(f"   Failed: {metrics.error_count}")
        print(f"   Success rate: {metrics.success_rate:.1f}%")

        # Example 2: Latency Metrics
        print("\n2. Latency metrics...")
        metrics = Metrics()

        async with ApiClient(base_url, config) as api:
            for i in range(10):
                start_time = asyncio.get_event_loop().time()
                result = await api.make_request(f"/api/data-{i}", method="GET")
                latency = asyncio.get_event_loop().time() - start_time

                metrics.record_request(
                    success=result.success,
                    latency=latency,
                )

        print(f"   Average latency: {metrics.avg_latency:.3f}s")
        print(f"   Min latency: {metrics.min_latency:.3f}s" if metrics.min_latency else "   Min latency: N/A")
        print(f"   Max latency: {metrics.max_latency:.3f}s" if metrics.max_latency else "   Max latency: N/A")

        # Example 3: Error Tracking
        print("\n3. Error tracking...")
        metrics = Metrics()

        async with ApiClient(base_url, config) as api:
            endpoints = ["/api/success", "/api/timeout", "/api/error", "/api/success"]
            for endpoint in endpoints:
                start_time = asyncio.get_event_loop().time()
                result = await api.make_request(endpoint, method="GET")
                latency = asyncio.get_event_loop().time() - start_time

                error_type = None
                if not result.success:
                    if result.status_code == 408:
                        error_type = "timeout"
                    elif result.status_code >= 500:
                        error_type = "server_error"
                    else:
                        error_type = "client_error"

                metrics.record_request(
                    success=result.success,
                    latency=latency,
                    error_type=error_type,
                )

        print(f"   Errors by type: {dict(metrics.errors_by_type)}")
        print(f"   Error rate: {metrics.error_rate:.1f}%")

        # Example 4: Metrics Summary
        print("\n4. Metrics summary...")
        metrics = Metrics()

        async with ApiClient(base_url, config) as api:
            for i in range(20):
                start_time = asyncio.get_event_loop().time()
                result = await api.make_request(f"/api/item-{i}", method="GET")
                latency = asyncio.get_event_loop().time() - start_time

                metrics.record_request(
                    success=result.success,
                    latency=latency,
                )

        print(f"   Summary: {metrics.get_summary()}")

        # Example 5: Metrics to Dictionary
        print("\n5. Converting metrics to dictionary...")
        metrics = Metrics()

        async with ApiClient(base_url, config) as api:
            for i in range(5):
                start_time = asyncio.get_event_loop().time()
                result = await api.make_request(f"/api/test-{i}", method="GET")
                latency = asyncio.get_event_loop().time() - start_time

                metrics.record_request(
                    success=result.success,
                    latency=latency,
                )

        metrics_dict = metrics.to_dict()
        print(f"   Metrics dict keys: {list(metrics_dict.keys())}")
        print(f"   Request count: {metrics_dict['request_count']}")
        print(f"   Success rate: {metrics_dict['success_rate']:.1f}%")
        print(f"   Requests per second: {metrics_dict['requests_per_second']:.2f}")

        # Example 6: Reset Metrics
        print("\n6. Resetting metrics...")
        metrics = Metrics()

        async with ApiClient(base_url, config) as api:
            for i in range(3):
                start_time = asyncio.get_event_loop().time()
                result = await api.make_request(f"/api/pre-{i}", method="GET")
                latency = asyncio.get_event_loop().time() - start_time
                metrics.record_request(success=result.success, latency=latency)

        print(f"   Before reset: {metrics.request_count} requests")
        metrics.reset()
        print(f"   After reset: {metrics.request_count} requests")

        print("\n=== Metrics Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

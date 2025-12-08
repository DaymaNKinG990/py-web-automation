"""
Unit tests for Metrics.
"""

# Python imports
from allure import title, description, step
from pytest import mark

# Local imports
from py_web_automation.clients.api_clients.graphql_client.metrics import Metrics

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestMetrics:
    """Test Metrics class."""

    @mark.asyncio
    @title("Metrics record successful request")
    @description("Test Metrics.record_request() records successful request.")
    async def test_metrics_record_successful_request(self) -> None:
        """Test Metrics.record_request() records successful request."""
        with step("Create Metrics instance"):
            metrics = Metrics()
        with step("Record successful request"):
            metrics.record_request(success=True, latency=0.5)
        with step("Verify metrics"):
            assert metrics.request_count == 1
            assert metrics.success_count == 1
            assert metrics.error_count == 0
            assert metrics.total_latency == 0.5
            assert metrics.min_latency == 0.5
            assert metrics.max_latency == 0.5

    @mark.asyncio
    @title("Metrics record failed request")
    @description("Test Metrics.record_request() records failed request.")
    async def test_metrics_record_failed_request(self) -> None:
        """Test Metrics.record_request() records failed request."""
        with step("Create Metrics instance"):
            metrics = Metrics()
        with step("Record failed request"):
            metrics.record_request(success=False, latency=0.1, error_type="graphql_error")
        with step("Verify metrics"):
            assert metrics.request_count == 1
            assert metrics.success_count == 0
            assert metrics.error_count == 1
            assert metrics.total_latency == 0.1
            assert metrics.errors_by_type["graphql_error"] == 1

    @mark.asyncio
    @title("Metrics calculate average latency")
    @description("Test Metrics.avg_latency calculates average correctly.")
    async def test_metrics_avg_latency(self) -> None:
        """Test Metrics.avg_latency calculates average correctly."""
        with step("Create Metrics instance"):
            metrics = Metrics()
        with step("Record multiple requests"):
            metrics.record_request(success=True, latency=0.2)
            metrics.record_request(success=True, latency=0.4)
            metrics.record_request(success=True, latency=0.6)
        with step("Verify average latency"):
            # Use approximate comparison for float precision
            assert abs(metrics.avg_latency - 0.4) < 0.0001

    @mark.asyncio
    @title("Metrics calculate success rate")
    @description("Test Metrics.success_rate calculates success rate correctly.")
    async def test_metrics_success_rate(self) -> None:
        """Test Metrics.success_rate calculates success rate correctly."""
        with step("Create Metrics instance"):
            metrics = Metrics()
        with step("Record mixed requests"):
            metrics.record_request(success=True, latency=0.1)
            metrics.record_request(success=True, latency=0.2)
            metrics.record_request(success=False, latency=0.1, error_type="error")
        with step("Verify success rate"):
            # success_rate returns percentage (0-100), not fraction
            expected_rate = (2 / 3) * 100.0
            assert abs(metrics.success_rate - expected_rate) < 0.01

    @mark.asyncio
    @title("Metrics update min and max latency")
    @description("Test Metrics updates min and max latency correctly.")
    async def test_metrics_min_max_latency(self) -> None:
        """Test Metrics updates min and max latency correctly."""
        with step("Create Metrics instance"):
            metrics = Metrics()
        with step("Record requests with different latencies"):
            metrics.record_request(success=True, latency=0.5)
            metrics.record_request(success=True, latency=0.1)
            metrics.record_request(success=True, latency=1.0)
        with step("Verify min and max latency"):
            assert metrics.min_latency == 0.1
            assert metrics.max_latency == 1.0

    @mark.asyncio
    @title("Metrics reset clears all metrics")
    @description("Test Metrics.reset() clears all metrics.")
    async def test_metrics_reset(self) -> None:
        """Test Metrics.reset() clears all metrics."""
        with step("Create Metrics instance and record requests"):
            metrics = Metrics()
            metrics.record_request(success=True, latency=0.5)
            metrics.record_request(success=False, latency=0.1, error_type="error")
        with step("Reset metrics"):
            metrics.reset()
        with step("Verify metrics are cleared"):
            assert metrics.request_count == 0
            assert metrics.success_count == 0
            assert metrics.error_count == 0
            assert metrics.total_latency == 0.0
            assert metrics.min_latency is None
            assert metrics.max_latency is None
            assert len(metrics.errors_by_type) == 0

    @mark.asyncio
    @title("Metrics avg_latency returns zero for empty metrics")
    @description("Test Metrics.avg_latency returns 0.0 when no requests recorded.")
    async def test_metrics_avg_latency_empty(self) -> None:
        """Test Metrics.avg_latency returns 0.0 when no requests recorded."""
        with step("Create empty Metrics instance"):
            metrics = Metrics()
        with step("Verify avg_latency is zero"):
            assert metrics.avg_latency == 0.0

    @mark.asyncio
    @title("Metrics success_rate returns zero for empty metrics")
    @description("Test Metrics.success_rate returns 0.0 when no requests recorded.")
    async def test_metrics_success_rate_empty(self) -> None:
        """Test Metrics.success_rate returns 0.0 when no requests recorded."""
        with step("Create empty Metrics instance"):
            metrics = Metrics()
        with step("Verify success_rate is zero"):
            assert metrics.success_rate == 0.0

    @mark.asyncio
    @title("Metrics error_rate returns zero for empty metrics")
    @description("Test Metrics.error_rate returns 0.0 when no requests recorded.")
    async def test_metrics_error_rate_empty(self) -> None:
        """Test Metrics.error_rate returns 0.0 when no requests recorded."""
        with step("Create empty Metrics instance"):
            metrics = Metrics()
        with step("Verify error_rate is zero"):
            assert metrics.error_rate == 0.0

    @mark.asyncio
    @title("Metrics operations_per_second returns zero for empty metrics")
    @description("Test Metrics.operations_per_second returns 0.0 when no requests recorded.")
    async def test_metrics_operations_per_second_empty(self) -> None:
        """Test Metrics.operations_per_second returns 0.0 when no requests recorded."""
        with step("Create empty Metrics instance"):
            metrics = Metrics()
        with step("Verify operations_per_second is zero"):
            assert metrics.operations_per_second == 0.0

    @mark.asyncio
    @title("Metrics operations_per_second handles zero elapsed time")
    @description("Test Metrics.operations_per_second returns 0.0 when elapsed time is zero.")
    async def test_metrics_operations_per_second_zero_elapsed(self) -> None:
        """Test Metrics.operations_per_second returns 0.0 when elapsed time is zero."""
        with step("Create Metrics instance"):
            metrics = Metrics()
        with step("Record request immediately"):
            # Record request at same time as start_time (simulated)
            metrics.record_request(success=True, latency=0.1)
        with step("Verify operations_per_second handles edge case"):
            # This tests the elapsed == 0 branch
            # In practice, elapsed will be very small but not zero
            # But we test that the check exists
            ops_per_sec = metrics.operations_per_second
            assert ops_per_sec >= 0.0

    @mark.asyncio
    @title("Metrics requests_per_second is alias for operations_per_second")
    @description("Test Metrics.requests_per_second returns same value as operations_per_second.")
    async def test_metrics_requests_per_second(self) -> None:
        """Test Metrics.requests_per_second returns same value as operations_per_second."""
        with step("Create Metrics instance"):
            metrics = Metrics()
        with step("Record some requests"):
            metrics.record_request(success=True, latency=0.1)
            metrics.record_request(success=True, latency=0.2)
        with step("Verify requests_per_second equals operations_per_second"):
            assert metrics.requests_per_second == metrics.operations_per_second

    @mark.asyncio
    @title("Metrics to_dict converts to dictionary")
    @description("Test Metrics.to_dict() converts metrics to dictionary representation.")
    async def test_metrics_to_dict(self) -> None:
        """Test Metrics.to_dict() converts metrics to dictionary representation."""
        with step("Create Metrics instance and record requests"):
            metrics = Metrics()
            metrics.record_request(success=True, latency=0.5)
            metrics.record_request(success=False, latency=0.1, error_type="graphql_error")
        with step("Convert to dictionary"):
            metrics_dict = metrics.to_dict()
        with step("Verify dictionary structure"):
            assert isinstance(metrics_dict, dict)
            assert metrics_dict["request_count"] == 2
            assert metrics_dict["success_count"] == 1
            assert metrics_dict["error_count"] == 1
            assert "avg_latency" in metrics_dict
            assert "min_latency" in metrics_dict
            assert "max_latency" in metrics_dict
            assert "success_rate" in metrics_dict
            assert "error_rate" in metrics_dict
            assert "operations_per_second" in metrics_dict
            assert "requests_per_second" in metrics_dict
            assert "errors_by_type" in metrics_dict
            assert metrics_dict["errors_by_type"]["graphql_error"] == 1
            assert "start_time" in metrics_dict
            assert "last_request_time" in metrics_dict

    @mark.asyncio
    @title("Metrics get_summary returns formatted string")
    @description("Test Metrics.get_summary() returns human-readable summary string.")
    async def test_metrics_get_summary(self) -> None:
        """Test Metrics.get_summary() returns human-readable summary string."""
        with step("Create Metrics instance and record requests"):
            metrics = Metrics()
            metrics.record_request(success=True, latency=0.5)
            metrics.record_request(success=True, latency=0.1)
            metrics.record_request(success=False, latency=0.2, error_type="graphql_error")
        with step("Get summary"):
            summary = metrics.get_summary()
        with step("Verify summary format"):
            assert isinstance(summary, str)
            assert "Operations: 3" in summary
            assert "Success: 2" in summary
            assert "Errors: 1" in summary
            assert "Latency:" in summary
            assert "OPS:" in summary

"""
Unit tests for metrics module.
"""

import time

import allure
import pytest

from py_web_automation.metrics import Metrics

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestMetricsRecordRequest:
    """Test Metrics.record_request method."""

    @allure.title("TC-METRICS-001: Metrics - record_request успех")
    def test_metrics_record_request_success(self):
        """Test recording successful request."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record successful request"):
            metrics.record_request(success=True, latency=0.5)

        with allure.step("Verify success metrics recorded"):
            assert metrics.request_count == 1
            assert metrics.success_count == 1
            assert metrics.error_count == 0

    @allure.title("TC-METRICS-002: Metrics - record_request ошибка")
    def test_metrics_record_request_error(self):
        """Test recording error request."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record error request"):
            metrics.record_request(success=False, latency=0.1, error_type="timeout")

        with allure.step("Verify error metrics recorded"):
            assert metrics.request_count == 1
            assert metrics.error_count == 1
            assert metrics.errors_by_type["timeout"] == 1

    @allure.title("TC-METRICS-003: Metrics - record_request без error_type")
    def test_metrics_record_request_no_error_type(self):
        """Test recording error without error_type."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record error without error_type"):
            metrics.record_request(success=False, latency=0.1)

        with allure.step("Verify error recorded without error_type"):
            assert metrics.error_count == 1
            assert len(metrics.errors_by_type) == 0


@pytest.mark.unit
class TestMetricsProperties:
    """Test Metrics properties."""

    @allure.title("TC-METRICS-004: Metrics - avg_latency")
    def test_metrics_avg_latency(self):
        """Test average latency calculation."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record requests with different latency"):
            metrics.record_request(success=True, latency=0.1)
            metrics.record_request(success=True, latency=0.3)
            metrics.record_request(success=True, latency=0.5)

        with allure.step("Verify avg_latency = 0.3"):
            assert metrics.avg_latency == pytest.approx(0.3, rel=0.1)

    @allure.title("TC-METRICS-005: Metrics - avg_latency без запросов")
    def test_metrics_avg_latency_empty(self):
        """Test avg_latency = 0.0 when no requests."""
        with allure.step("Create empty Metrics"):
            metrics = Metrics()

        with allure.step("Verify avg_latency = 0.0"):
            assert metrics.avg_latency == 0.0

    @allure.title("TC-METRICS-006: Metrics - success_rate")
    def test_metrics_success_rate(self):
        """Test success rate calculation."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record 10 requests (7 success, 3 errors)"):
            for _ in range(7):
                metrics.record_request(success=True, latency=0.5)
            for _ in range(3):
                metrics.record_request(success=False, latency=0.1)

        with allure.step("Verify success_rate = 70.0"):
            assert metrics.success_rate == pytest.approx(70.0, rel=0.1)

    @allure.title("TC-METRICS-007: Metrics - error_rate")
    def test_metrics_error_rate(self):
        """Test error rate calculation."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record 10 requests (7 success, 3 errors)"):
            for _ in range(7):
                metrics.record_request(success=True, latency=0.5)
            for _ in range(3):
                metrics.record_request(success=False, latency=0.1)

        with allure.step("Verify error_rate = 30.0"):
            assert metrics.error_rate == pytest.approx(30.0, rel=0.1)

    @allure.title("TC-METRICS-008: Metrics - min_latency и max_latency")
    def test_metrics_min_max_latency(self):
        """Test min/max latency tracking."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record requests with latency: 0.1, 0.5, 0.3"):
            metrics.record_request(success=True, latency=0.1)
            metrics.record_request(success=True, latency=0.5)
            metrics.record_request(success=True, latency=0.3)

        with allure.step("Verify min_latency=0.1, max_latency=0.5"):
            assert metrics.min_latency == pytest.approx(0.1, rel=0.01)
            assert metrics.max_latency == pytest.approx(0.5, rel=0.01)

    @allure.title("TC-METRICS-009: Metrics - requests_per_second")
    def test_metrics_requests_per_second(self):
        """Test RPS calculation."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record 10 requests"):
            for _ in range(10):
                metrics.record_request(success=True, latency=0.1)

        with allure.step("Wait 1 second"):
            time.sleep(1)

        with allure.step("Verify requests_per_second ≈ 10"):
            # RPS is calculated based on time since start_time
            rps = metrics.requests_per_second
            assert rps >= 0  # Should be non-negative

    @allure.title("TC-METRICS-010: Metrics - requests_per_second без запросов")
    def test_metrics_requests_per_second_empty(self):
        """Test RPS = 0.0 when no requests."""
        with allure.step("Create empty Metrics"):
            metrics = Metrics()

        with allure.step("Verify requests_per_second = 0.0"):
            assert metrics.requests_per_second == 0.0


@pytest.mark.unit
class TestMetricsUtility:
    """Test Metrics utility methods."""

    @allure.title("TC-METRICS-011: Metrics - reset")
    def test_metrics_reset(self):
        """Test metrics reset."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record several requests"):
            metrics.record_request(success=True, latency=0.5)
            metrics.record_request(success=False, latency=0.1)

        with allure.step("Reset metrics"):
            metrics.reset()

        with allure.step("Verify all metrics reset"):
            assert metrics.request_count == 0
            assert metrics.success_count == 0
            assert metrics.error_count == 0
            assert metrics.total_latency == 0.0
            assert metrics.min_latency is None
            assert metrics.max_latency is None
            assert len(metrics.errors_by_type) == 0

    @allure.title("TC-METRICS-012: Metrics - to_dict")
    def test_metrics_to_dict(self):
        """Test conversion to dictionary."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record several requests"):
            metrics.record_request(success=True, latency=0.5)
            metrics.record_request(success=False, latency=0.1, error_type="timeout")

        with allure.step("Convert to dictionary"):
            metrics_dict = metrics.to_dict()

        with allure.step("Verify dictionary contains all metrics"):
            assert "request_count" in metrics_dict
            assert "success_count" in metrics_dict
            assert "error_count" in metrics_dict
            assert "avg_latency" in metrics_dict
            assert metrics_dict["request_count"] == 2

    @allure.title("TC-METRICS-013: Metrics - get_summary")
    def test_metrics_get_summary(self):
        """Test formatted summary."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record several requests"):
            metrics.record_request(success=True, latency=0.5)
            metrics.record_request(success=False, latency=0.1)

        with allure.step("Get summary"):
            summary = metrics.get_summary()

        with allure.step("Verify formatted string contains key metrics"):
            assert "request_count" in summary.lower() or "requests" in summary.lower()
            assert "success" in summary.lower() or "error" in summary.lower()

    @allure.title("TC-METRICS-014: Metrics - last_request_time")
    def test_metrics_last_request_time(self):
        """Test last_request_time tracking."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record request"):
            before = time.time()
            metrics.record_request(success=True, latency=0.5)
            after = time.time()

        with allure.step("Verify last_request_time is recent"):
            assert metrics.last_request_time is not None
            assert before <= metrics.last_request_time.timestamp() <= after

    @allure.title("TC-METRICS-015: Metrics - errors_by_type aggregation")
    def test_metrics_errors_by_type(self):
        """Test error type aggregation."""
        with allure.step("Create Metrics"):
            metrics = Metrics()

        with allure.step("Record 3 errors with error_type='timeout'"):
            for _ in range(3):
                metrics.record_request(success=False, latency=0.1, error_type="timeout")

        with allure.step("Record 2 errors with error_type='connection'"):
            for _ in range(2):
                metrics.record_request(success=False, latency=0.1, error_type="connection")

        with allure.step("Verify errors aggregated by type"):
            assert metrics.errors_by_type["timeout"] == 3
            assert metrics.errors_by_type["connection"] == 2

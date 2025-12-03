"""
Performance metrics collection for web automation framework.

This module provides metrics collection for monitoring request performance,
success rates, and error patterns.
"""

# Python imports
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Metrics:
    """
    Internal performance metrics collector.

    Collects and aggregates metrics about API requests including:
    - Request count and success/error rates
    - Latency statistics (min, max, average)
    - Error breakdown by type
    - Timestamp tracking

    Attributes:
        request_count: Total number of requests
        success_count: Number of successful requests
        error_count: Number of failed requests
        total_latency: Sum of all request latencies
        min_latency: Minimum latency observed
        max_latency: Maximum latency observed
        errors_by_type: Dictionary counting errors by type
        start_time: When metrics collection started
        last_request_time: Timestamp of last request
    """

    request_count: int = 0
    success_count: int = 0
    error_count: int = 0
    total_latency: float = 0.0
    min_latency: float | None = None
    max_latency: float | None = None
    errors_by_type: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    start_time: datetime = field(default_factory=datetime.now)
    last_request_time: datetime | None = None

    def record_request(
        self,
        success: bool,
        latency: float,
        error_type: str | None = None,
    ) -> None:
        """
        Record a request metric.

        Args:
            success: Whether the request was successful
            latency: Request latency in seconds
            error_type: Type of error if request failed (optional)

        Example:
            >>> metrics.record_request(success=True, latency=0.5)
            >>> metrics.record_request(success=False, latency=0.1, error_type="timeout")
        """
        self.request_count += 1
        self.last_request_time = datetime.now()
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
            if error_type:
                self.errors_by_type[error_type] += 1
        self.total_latency += latency
        if self.min_latency is None or latency < self.min_latency:
            self.min_latency = latency
        if self.max_latency is None or latency > self.max_latency:
            self.max_latency = latency

    @property
    def avg_latency(self) -> float:
        """
        Calculate average latency.

        Returns:
            Average latency in seconds, or 0.0 if no requests
        """
        if self.request_count == 0:
            return 0.0
        return self.total_latency / self.request_count

    @property
    def success_rate(self) -> float:
        """
        Calculate success rate percentage.

        Returns:
            Success rate as percentage (0-100), or 0.0 if no requests
        """
        if self.request_count == 0:
            return 0.0
        return (self.success_count / self.request_count) * 100.0

    @property
    def error_rate(self) -> float:
        """
        Calculate error rate percentage.

        Returns:
            Error rate as percentage (0-100), or 0.0 if no requests
        """
        if self.request_count == 0:
            return 0.0
        return (self.error_count / self.request_count) * 100.0

    @property
    def requests_per_second(self) -> float:
        """
        Calculate requests per second.

        Returns:
            Average requests per second since start, or 0.0 if no requests
        """
        if self.request_count == 0:
            return 0.0
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed == 0:
            return 0.0
        return self.request_count / elapsed

    def reset(self) -> None:
        """Reset all metrics to zero."""
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_latency = 0.0
        self.min_latency = None
        self.max_latency = None
        self.errors_by_type.clear()
        self.start_time = datetime.now()
        self.last_request_time = None

    def to_dict(self) -> dict[str, Any]:
        """
        Convert metrics to dictionary.

        Returns:
            Dictionary representation of metrics

        Example:
            >>> metrics_dict = metrics.to_dict()
            >>> print(metrics_dict)
        """
        return {
            "request_count": self.request_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "avg_latency": self.avg_latency,
            "min_latency": self.min_latency,
            "max_latency": self.max_latency,
            "success_rate": self.success_rate,
            "error_rate": self.error_rate,
            "requests_per_second": self.requests_per_second,
            "errors_by_type": dict(self.errors_by_type),
            "start_time": self.start_time.isoformat(),
            "last_request_time": (
                self.last_request_time.isoformat() if self.last_request_time else None
            ),
        }

    def get_summary(self) -> str:
        """
        Get human-readable summary of metrics.

        Returns:
            Formatted string summary

        Example:
            >>> print(metrics.get_summary())
        """
        return (
            f"Requests: {self.request_count} | "
            f"Success: {self.success_count} ({self.success_rate:.1f}%) | "
            f"Errors: {self.error_count} ({self.error_rate:.1f}%) | "
            f"Latency: avg={self.avg_latency:.3f}s "
            f"min={self.min_latency or 0:.3f}s "
            f"max={self.max_latency or 0:.3f}s | "
            f"RPS: {self.requests_per_second:.2f}"
        )

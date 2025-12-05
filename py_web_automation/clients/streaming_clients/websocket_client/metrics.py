"""
Performance metrics collection for WebSocket client.

This module provides metrics collection for monitoring WebSocket message performance,
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
    Performance metrics collector for WebSocket messages and connections.

    Collects and aggregates metrics about WebSocket messages including:
    - Message count and success/error rates
    - Connection lifetime statistics
    - Error breakdown by type
    - Timestamp tracking

    Attributes:
        request_count: Total number of messages
        success_count: Number of successful messages
        error_count: Number of failed messages
        total_latency: Sum of all message latencies (or connection lifetimes)
        min_latency: Minimum latency observed
        max_latency: Maximum latency observed
        errors_by_type: Dictionary counting errors by type
        start_time: When metrics collection started
        last_request_time: Timestamp of last message
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
        Record a WebSocket message or connection metric.

        Args:
            success: Whether the message/connection was successful
            latency: Message latency or connection lifetime in seconds
            error_type: Type of error if operation failed (optional)

        Example:
            >>> metrics.record_request(success=True, latency=0.5)
            >>> metrics.record_request(success=False, latency=0.1, error_type="ConnectionClosed")
        """
        self.request_count += 1
        self.last_request_time = datetime.now()

        if success:
            self._record_success(latency)
        else:
            self._record_error(latency, error_type)

        self._update_latency_stats(latency)

    def _record_success(self, latency: float) -> None:
        """Record successful message/connection metrics."""
        self.success_count += 1
        self.total_latency += latency

    def _record_error(self, latency: float, error_type: str | None) -> None:
        """Record error message/connection metrics."""
        self.error_count += 1
        self.total_latency += latency
        if error_type:
            self.errors_by_type[error_type] += 1

    def _update_latency_stats(self, latency: float) -> None:
        """Update min and max latency statistics."""
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
    def messages_per_second(self) -> float:
        """
        Calculate messages per second.

        Returns:
            Average messages per second since start, or 0.0 if no messages
        """
        if self.request_count == 0:
            return 0.0
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed == 0:
            return 0.0
        return self.request_count / elapsed

    @property
    def requests_per_second(self) -> float:
        """
        Calculate requests per second (alias for messages_per_second).

        Returns:
            Average messages per second since start, or 0.0 if no messages
        """
        return self.messages_per_second

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
            "messages_per_second": self.messages_per_second,
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
            f"Messages: {self.request_count} | "
            f"Success: {self.success_count} ({self.success_rate:.1f}%) | "
            f"Errors: {self.error_count} ({self.error_rate:.1f}%) | "
            f"Latency: avg={self.avg_latency:.3f}s "
            f"min={self.min_latency or 0:.3f}s "
            f"max={self.max_latency or 0:.3f}s | "
            f"MPS: {self.messages_per_second:.2f}"
        )

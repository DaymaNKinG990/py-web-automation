"""
Constitution compliance review tools.

This package provides tools for reviewing codebase compliance with the project constitution.
"""

# Import main function for CLI access
from .__main__ import main
from .base_checker import BaseChecker
from .config import ReviewConfig
from .file_discovery import FileDiscoveryService
from .models import (
    ComplianceReport,
    ComplianceViolation,
    PrincipleCheck,
    RemediationStep,
    StandardCheck,
)
from .review_orchestrator import ReviewOrchestrator
from .violation_collector import ViolationCollector

__all__ = [
    "BaseChecker",
    "ComplianceReport",
    "ComplianceViolation",
    "FileDiscoveryService",
    "PrincipleCheck",
    "RemediationStep",
    "ReviewConfig",
    "ReviewOrchestrator",
    "StandardCheck",
    "ViolationCollector",
    "main",
]

"""
Data models for constitution compliance review.

This module defines the core data structures used throughout the review process.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ComplianceViolation:
    """
    Represents a single instance where code does not comply with a constitution principle.

    Attributes:
        principle: Name of the violated principle (e.g., "Async-First", "Type Safety")
        standard: Name of the violated standard (e.g., "Code Style", "Testing Standards")
        file_path: Relative path to the file containing the violation
        line_number: Line number where violation occurs (0 if file-level)
        column_number: Column number where violation occurs (0 if not applicable)
        violation_type: Type of violation (e.g., "missing_type_annotation", "blocking_io")
        violation_description: Human-readable description of the violation
        severity: Severity level: "CRITICAL", "HIGH", "MEDIUM", "LOW"
        code_snippet: Relevant code snippet showing the violation (optional)
        remediation_suggestion: Suggested fix for the violation
    """

    principle: str | None = None
    standard: str | None = None
    file_path: str = ""
    line_number: int = 0
    column_number: int = 0
    violation_type: str = ""
    violation_description: str = ""
    severity: str = "MEDIUM"
    code_snippet: str | None = None
    remediation_suggestion: str = ""

    def __post_init__(self) -> None:
        """Validate violation data."""
        if not self.principle and not self.standard:
            raise ValueError("Either principle or standard must be provided")
        if self.file_path == "":
            raise ValueError("file_path must be provided")
        if self.line_number < 0:
            raise ValueError("line_number must be >= 0")
        if self.severity not in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            raise ValueError("severity must be one of: CRITICAL, HIGH, MEDIUM, LOW")


@dataclass
class PrincipleCheck:
    """
    Represents verification of a single constitution principle.

    Attributes:
        principle_name: Name of the principle being checked
        check_status: Status: "PASS", "FAIL", "PARTIAL"
        violations_found: Number of violations found
        files_checked: Number of files analyzed for this principle
        files_with_violations: Number of files containing violations
        compliance_percentage: Compliance percentage for this principle (0-100)
        check_duration_seconds: Time taken to perform the check
        violations: List of violations for this principle
    """

    principle_name: str
    check_status: str = "PASS"
    violations_found: int = 0
    files_checked: int = 0
    files_with_violations: int = 0
    compliance_percentage: float = 100.0
    check_duration_seconds: float = 0.0
    violations: list[ComplianceViolation] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate check data."""
        if self.check_status not in ("PASS", "FAIL", "PARTIAL"):
            raise ValueError("check_status must be one of: PASS, FAIL, PARTIAL")
        if not 0 <= self.compliance_percentage <= 100:
            raise ValueError("compliance_percentage must be between 0 and 100")
        if self.violations_found != len(self.violations):
            raise ValueError("violations_found must equal length of violations list")


@dataclass
class StandardCheck:
    """
    Represents verification of a single development standard.

    Attributes:
        standard_name: Name of the standard being checked
        check_status: Status: "PASS", "FAIL", "PARTIAL"
        violations_found: Number of violations found
        files_checked: Number of files analyzed for this standard
        files_with_violations: Number of files containing violations
        compliance_percentage: Compliance percentage for this standard (0-100)
        check_duration_seconds: Time taken to perform the check
        violations: List of violations for this standard
    """

    standard_name: str
    check_status: str = "PASS"
    violations_found: int = 0
    files_checked: int = 0
    files_with_violations: int = 0
    compliance_percentage: float = 100.0
    check_duration_seconds: float = 0.0
    violations: list[ComplianceViolation] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate check data."""
        if self.check_status not in ("PASS", "FAIL", "PARTIAL"):
            raise ValueError("check_status must be one of: PASS, FAIL, PARTIAL")
        if not 0 <= self.compliance_percentage <= 100:
            raise ValueError("compliance_percentage must be between 0 and 100")
        if self.violations_found != len(self.violations):
            raise ValueError("violations_found must equal length of violations list")


@dataclass
class ComplianceReport:
    """
    Aggregated results of the review process.

    Attributes:
        report_id: Unique identifier for the report (timestamp-based)
        generated_at: When the report was generated
        total_files_analyzed: Number of files analyzed
        total_violations: Total number of violations found
        violations_by_principle: Count of violations per principle
        violations_by_standard: Count of violations per standard
        violations_by_file: Count of violations per file
        violations_by_severity: Count of violations per severity level
        compliance_percentage: Overall compliance percentage (0-100)
        principle_compliance: Compliance percentage per principle
        standard_compliance: Compliance percentage per standard
        violations: List of all violations
        summary: Executive summary of findings
    """

    report_id: str = ""
    generated_at: datetime = field(default_factory=datetime.now)
    total_files_analyzed: int = 0
    total_violations: int = 0
    violations_by_principle: dict[str, int] = field(default_factory=dict)
    violations_by_standard: dict[str, int] = field(default_factory=dict)
    violations_by_file: dict[str, int] = field(default_factory=dict)
    violations_by_severity: dict[str, int] = field(default_factory=dict)
    compliance_percentage: float = 100.0
    principle_compliance: dict[str, float] = field(default_factory=dict)
    standard_compliance: dict[str, float] = field(default_factory=dict)
    violations: list[ComplianceViolation] = field(default_factory=list)
    summary: str = ""

    def __post_init__(self) -> None:
        """Validate report data."""
        if not 0 <= self.compliance_percentage <= 100:
            raise ValueError("compliance_percentage must be between 0 and 100")

        # Validate that total_violations matches the number of unique violations
        if self.total_violations != len(self.violations):
            raise ValueError(
                f"total_violations mismatch: provided {self.total_violations} "
                f"does not match number of violations in list {len(self.violations)}. "
                f"This indicates a data consistency issue."
            )

        # Validate that total_violations matches sum of severity counts
        # (each violation has exactly one severity, so these should match)
        total_by_severity = sum(self.violations_by_severity.values())
        if self.total_violations != total_by_severity:
            raise ValueError(
                f"total_violations mismatch: provided {self.total_violations} "
                f"does not match computed sum {total_by_severity} from "
                f"violations_by_severity. This indicates a data consistency issue."
            )

        # Note: violations_by_principle and violations_by_standard sums may exceed
        # total_violations because a single violation can belong to both a principle
        # and a standard. This is expected behavior and not a validation error.


@dataclass(frozen=True)
class RemediationStep:
    """
    Represents an actionable step to fix violations.

    Attributes:
        step_id: Unique identifier for the remediation step
        principle: Principle this step addresses
        standard: Standard this step addresses (optional)
        priority: Priority: "CRITICAL", "HIGH", "MEDIUM", "LOW"
        title: Short title describing the remediation
        description: Detailed description of what needs to be done
        affected_files: List of files that need changes
        estimated_effort: Estimated effort (e.g., "2 hours", "1 day")
        dependencies: IDs of other remediation steps that must be completed first
        violation_ids: IDs of violations this step addresses
    """

    step_id: str
    principle: str
    standard: str | None = None
    priority: str = "MEDIUM"
    title: str = ""
    description: str = ""
    affected_files: list[str] = field(default_factory=list)
    estimated_effort: str = ""
    dependencies: list[str] = field(default_factory=list)
    violation_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate remediation step data."""
        if self.priority not in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            raise ValueError("priority must be one of: CRITICAL, HIGH, MEDIUM, LOW")
        if not self.affected_files:
            raise ValueError("affected_files must not be empty")
        if not self.violation_ids:
            raise ValueError("violation_ids must not be empty")

# Quick Start: Constitution Compliance Review

**Date**: 2025-12-09  
**Feature**: Project Constitution Compliance Review

## Overview

This guide provides step-by-step instructions for conducting a comprehensive constitution compliance review of the py-web-automation project.

## Prerequisites

- Python 3.12+
- `uv` package manager installed
- Git installed and configured
- Project dependencies installed: `uv sync --all-groups`

## Quick Start Steps

### 1. Setup Review Environment

```bash
# Navigate to project root
cd /path/to/py-web-automation

# Ensure all dependencies are installed
uv sync --all-groups

# Navigate to review feature directory
cd specs/001-constitution-review
```

### 2. Run Complete Review

Run the complete compliance review using the CLI:

**Option 1: From project root (recommended)**
```bash
# Navigate to review directory first
cd specs/001-constitution-review

# Run full review
uv run python -m tools

# Run with verbose output
uv run python -m tools --verbose

# Run with custom output directory
uv run python -m tools --output-dir ./custom_reports
```

**Option 2: Using wrapper script**
```bash
# From project root
uv run python specs/001-constitution-review/run_review.py

# With options
uv run python specs/001-constitution-review/run_review.py --verbose
```

### 3. View Generated Reports

After running the review, reports will be generated in `specs/001-constitution-review/reports/`:

- **compliance_report.md**: Human-readable compliance report with executive summary
- **violations_by_principle.json**: Structured JSON data for programmatic analysis
- **remediation_plan.md**: Prioritized list of fixes with effort estimates

### 4. Review Generated Reports

1. **compliance_report.md**: Start here for executive summary and overview
2. **violations_by_principle.json**: Use for programmatic analysis or tooling
3. **remediation_plan.md**: Follow for prioritized fix recommendations

## Expected Output

After running the review, you should see:

- **Total files analyzed**: ~150+ files (source + tests)
- **Violations found**: Varies based on current compliance state
- **Compliance percentage**: Overall project compliance score
- **Report generation time**: < 30 minutes

## Next Steps

1. Review the compliance report to understand current state
2. Prioritize violations by severity (CRITICAL → HIGH → MEDIUM → LOW)
3. Follow remediation plan to address violations
4. Re-run review after fixes to verify improvements

## Troubleshooting

### Issue: Tool fails with import errors

**Solution**: Ensure all dependencies are installed:
```bash
uv sync --all-groups
```

### Issue: Report generation takes too long

**Solution**: Run individual checks in parallel or increase timeout limits

### Issue: False positives in violations

**Solution**: Review tool configuration and add exceptions for legitimate cases

## Additional Resources

- See [research.md](./research.md) for detailed tool selection rationale
- See [data-model.md](./data-model.md) for report structure details
- See [spec.md](./spec.md) for full requirements


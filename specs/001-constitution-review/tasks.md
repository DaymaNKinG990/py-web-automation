# Tasks: Project Constitution Compliance Review

**Input**: Design documents from `/specs/001-constitution-review/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are not requested for this review tooling feature - focus is on creating analysis tools.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Review tools**: `specs/001-constitution-review/tools/`
- **Reports**: `specs/001-constitution-review/reports/`
- **Data models**: `specs/001-constitution-review/tools/models.py`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for review tools

- [X] T001 Create tools directory structure in specs/001-constitution-review/tools/
- [X] T002 Create reports directory structure in specs/001-constitution-review/reports/
- [X] T003 [P] Create data models module in specs/001-constitution-review/tools/models.py with ComplianceViolation, ComplianceReport, PrincipleCheck, StandardCheck, RemediationStep classes
- [X] T004 [P] Create shared utilities module in specs/001-constitution-review/tools/utils.py with file discovery, AST parsing helpers, and common validation functions
- [X] T005 [P] Create configuration module in specs/001-constitution-review/tools/config.py for review settings and paths

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create base checker abstract class in specs/001-constitution-review/tools/base_checker.py with common interface for all principle/standard checkers
- [X] T007 [P] Implement file discovery service in specs/001-constitution-review/tools/file_discovery.py to find all Python files in py_web_automation/ and tests/ directories
- [X] T008 [P] Implement AST parser wrapper in specs/001-constitution-review/tools/ast_parser.py with helpers for analyzing Python code structure
- [X] T009 [P] Implement violation collector in specs/001-constitution-review/tools/violation_collector.py to aggregate violations from all checkers
- [X] T010 Create main review orchestrator in specs/001-constitution-review/tools/review_orchestrator.py to coordinate all checkers and generate reports

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Comprehensive Constitution Compliance Audit (Priority: P1) 🎯 MVP

**Goal**: Conduct a complete review of the py-web-automation project to identify all areas where the codebase does not comply with the project constitution and generate a comprehensive compliance report.

**Independent Test**: Can be fully tested by running the review orchestrator and verifying it analyzes all code files, identifies violations with file paths and line numbers, and generates a compliance report categorized by principle with actionable remediation steps.

### Implementation for User Story 1

- [X] T011 [US1] Implement report generator in specs/001-constitution-review/tools/generate_report.py with generate_report() method that creates ComplianceReport from all violations
- [X] T012 [US1] Implement JSON export in specs/001-constitution-review/tools/generate_report.py with export_json() method that converts ComplianceReport to JSON structure per contracts/report-api.md
- [X] T013 [US1] Implement Markdown export in specs/001-constitution-review/tools/generate_report.py with export_markdown() method that generates compliance_report.md per contracts/report-api.md structure
- [X] T014 [US1] Implement remediation plan generator in specs/001-constitution-review/tools/generate_report.py with generate_remediation_plan() method that creates prioritized RemediationStep list from violations
- [X] T015 [US1] Integrate report generation into review orchestrator in specs/001-constitution-review/tools/review_orchestrator.py to automatically generate all report formats after analysis
- [X] T016 [US1] Add command-line interface in specs/001-constitution-review/tools/__main__.py to run full review and generate reports

**Checkpoint**: At this point, User Story 1 should be fully functional - running the review should generate comprehensive compliance reports with all violations categorized and actionable remediation steps.

---

## Phase 4: User Story 2 - Core Principles Compliance Verification (Priority: P1)

**Goal**: Verify compliance with all 7 core principles (Async-First, Type Safety, Test-First, SOLID/Design Patterns, Performance, Package Management, Documentation) across all relevant code files.

**Independent Test**: Can be fully tested by running individual principle checkers and verifying each generates PrincipleCheck results with violations, compliance percentage, and file-level details.

### Implementation for User Story 2

- [X] T017 [P] [US2] Implement Async-First checker in specs/001-constitution-review/tools/check_async.py that uses AST to identify I/O operations and verifies async/await usage
- [X] T018 [P] [US2] Implement Type Safety checker in specs/001-constitution-review/tools/check_types.py that uses mypy and AST to verify complete type annotations on all public APIs
- [X] T019 [P] [US2] Implement Test-First checker in specs/001-constitution-review/tools/check_tests.py that verifies test cases exist in test_cases/ before corresponding test implementations
- [X] T020 [P] [US2] Implement SOLID principles checker in specs/001-constitution-review/tools/check_solid.py that uses solid-checker and AST to verify SOLID compliance and design pattern usage
- [X] T021 [P] [US2] Implement Performance checker in specs/001-constitution-review/tools/check_performance.py that analyzes imports and code to verify msgspec usage (not Pydantic) in performance-critical components
- [X] T022 [P] [US2] Implement Package Management checker in specs/001-constitution-review/tools/check_package_mgmt.py that analyzes project files and git history to verify uv-only usage (no pip/uv pip)
- [X] T023 [P] [US2] Implement Documentation checker in specs/001-constitution-review/tools/check_docs.py that verifies all documentation is in English and docstrings follow Google-style format
- [X] T024 [US2] Integrate all principle checkers into review orchestrator in specs/001-constitution-review/tools/review_orchestrator.py to run all principle checks and aggregate results

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - all 7 core principles can be checked and violations reported in the compliance report.

---

## Phase 5: User Story 3 - Development Standards Compliance Verification (Priority: P2)

**Goal**: Verify compliance with development standards (Code Style, Error Handling, Resource Management, Separation of Concerns, Testing Standards, Import Organization, Git Workflow) to ensure consistent code quality.

**Independent Test**: Can be fully tested by running individual standard checkers and verifying each generates StandardCheck results with violations categorized by standard type.

### Implementation for User Story 3

- [X] T025 [P] [US3] Implement Code Style checker in specs/001-constitution-review/tools/check_code_style.py that uses ruff to verify PEP 8 compliance, line length, and formatting
- [X] T026 [P] [US3] Implement Error Handling checker in specs/001-constitution-review/tools/check_error_handling.py that uses AST to verify WebAutomationError hierarchy usage and proper exception chaining
- [X] T027 [P] [US3] Implement Resource Management checker in specs/001-constitution-review/tools/check_resources.py that uses AST to verify all clients implement context managers
- [X] T028 [P] [US3] Implement Separation of Concerns checker in specs/001-constitution-review/tools/check_separation.py that analyzes module structure to verify proper separation of client types
- [X] T029 [P] [US3] Extend Testing Standards checker in specs/001-constitution-review/tools/check_tests.py to verify test decorators (allure.feature, allure.story, allure.title, allure.testcase, allure.severity, allure.description, pytest.mark), allure.step() usage, and parametrization
- [X] T030 [P] [US3] Implement Import Organization checker in specs/001-constitution-review/tools/check_imports.py that uses AST to verify imports are at top of files, organized correctly, and use TYPE_CHECKING for circular dependencies
- [X] T031 [P] [US3] Implement Git Workflow checker in specs/001-constitution-review/tools/check_git.py that analyzes git history and branches to verify branching strategy and commit frequency compliance
- [X] T032 [US3] Integrate all standard checkers into review orchestrator in specs/001-constitution-review/tools/review_orchestrator.py to run all standard checks and aggregate results

**Checkpoint**: All user stories should now be independently functional - complete review system can analyze all principles and standards, generate comprehensive reports, and provide actionable remediation steps.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and finalize the review system

- [X] T033 [P] Add error handling and logging to all checkers in specs/001-constitution-review/tools/ for graceful failure and debugging
- [X] T034 [P] Add performance optimization to review orchestrator in specs/001-constitution-review/tools/review_orchestrator.py to ensure review completes within 30 minutes
- [X] T035 [P] Update quickstart.md in specs/001-constitution-review/quickstart.md with actual command examples and troubleshooting based on implementation
- [X] T036 Add validation tests for report generation in specs/001-constitution-review/tools/test_report_generation.py to verify report structure and completeness
- [X] T037 Add command-line help and usage documentation in specs/001-constitution-review/tools/__main__.py
- [X] T038 [P] Create example compliance report in specs/001-constitution-review/reports/example_compliance_report.md to demonstrate expected output format
- [X] T039 Verify all tools follow constitution principles (async I/O where applicable, type annotations, proper error handling) in specs/001-constitution-review/tools/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories. Requires base checker and report generation infrastructure.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on US1. All principle checkers can be developed in parallel.
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on US1/US2. All standard checkers can be developed in parallel.

### Within Each User Story

- Data models before checkers (T003 must complete before checkers can use ComplianceViolation)
- Base checker before individual checkers (T006 must complete before T017-T032)
- Individual checkers can be developed in parallel (all marked [P])
- Report generation after checkers (T011-T015 depend on violations from checkers)
- Integration after individual components (T024, T032 depend on all checkers)

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005)
- All Foundational tasks marked [P] can run in parallel (T007, T008, T009)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All principle checkers for US2 marked [P] can run in parallel (T017-T023)
- All standard checkers for US3 marked [P] can run in parallel (T025-T031)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all principle checkers in parallel:
Task: "Implement Async-First checker in specs/001-constitution-review/tools/check_async.py"
Task: "Implement Type Safety checker in specs/001-constitution-review/tools/check_types.py"
Task: "Implement Test-First checker in specs/001-constitution-review/tools/check_tests.py"
Task: "Implement SOLID principles checker in specs/001-constitution-review/tools/check_solid.py"
Task: "Implement Performance checker in specs/001-constitution-review/tools/check_performance.py"
Task: "Implement Package Management checker in specs/001-constitution-review/tools/check_package_mgmt.py"
Task: "Implement Documentation checker in specs/001-constitution-review/tools/check_docs.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Report Generation)
4. **STOP and VALIDATE**: Test report generation with sample violations
5. Demo report format and structure

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Generate reports (MVP!)
3. Add User Story 2 → Check all core principles → Enhanced reports
4. Add User Story 3 → Check all standards → Complete review system
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Report Generation)
   - Developer B: User Story 2 (Core Principles - can work on multiple checkers in parallel)
   - Developer C: User Story 3 (Development Standards - can work on multiple checkers in parallel)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All checkers must follow base checker interface for consistency
- Report generation must handle empty violation lists gracefully
- All tools must have complete type annotations per constitution
- Tools should use async I/O where beneficial for file operations
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence


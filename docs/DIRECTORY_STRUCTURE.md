# Directory Structure & Layout Rationale

## Overview
This document provides a comprehensive breakdown of the directory organization established in the **SahkaarX Stage Portfolio** repository during the Week 02 restructuring initiative and expanded during Week 03 branching operations.

---

## Complete Repository Layout

```text
sahkaarx-stage-portfolio-d5b2372f/
├── .github/                             # GitHub automation and repository governance
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md                # Standardized issue template for bug reporting
│   │   └── feature_request.md           # Template for proposing new features
│   └── PULL_REQUEST_TEMPLATE.md         # Template standardizing code review checklists
├── docs/                                # Technical documentation & design guides
│   ├── ARCHITECTURE.md                  # High-level architecture & system design
│   ├── BRANCHING.md                     # Engineering branching strategy & merge protocol
│   ├── CONTRIBUTING.md                  # Development setup, branching model, and Git rules
│   └── DIRECTORY_STRUCTURE.md           # Directory structure reference & rationale
├── practice/                            # Weekly challenge deliverables & learning artifacts
│   ├── week-01-create-intentional-merge-conflicts-and-resolve/
│   │   ├── README.md                    # Detailed conflict creation & resolution walkthrough
│   │   ├── auth_service.py              # Multi-strategy resolved authentication module
│   │   ├── conflict_markers_example.md  # Raw conflict marker illustration & explanation
│   │   └── test_auth_service.py         # Unit tests validating resolved implementation
│   ├── week-02-practice-atomic-commits-and-clear-messaging/
│   │   ├── README.md                    # Atomic commits practice overview & verification
│   │   ├── ATOMIC_COMMITS_GUIDE.md      # Comprehensive guide on atomic commits & Conventional Commits
│   │   └── COMMIT_LOG_AUDIT.md          # Audit matrix of atomic commits & coherent narrative
│   ├── week-02-practice-basic-git-workflow-with-multiple-commit/
│   │   ├── README.md                    # Basic git workflow practice overview & quick start
│   │   ├── GIT_WORKFLOW_GUIDE.md        # Deep dive into Git three-tree model & command lifecycle
│   │   ├── COMMIT_HISTORY_AUDIT.md      # Command matrix, atomic commit audit, & commit graph
│   │   └── PULL_REQUEST.md              # Production-ready Pull Request ready for merge
│   ├── week-02-practice-gitignore-configuration-and-repository/
│   │   ├── README.md                    # Gitignore configuration & cleanliness deliverable
│   │   ├── EXCLUDED_PATTERNS.md         # Exhaustive reference of all excluded patterns
│   │   └── CLEAN_REPO_VERIFICATION.md   # Clean status logs & negative index verification
│   ├── week-02-restructure-portfolio-repo-with-professional-org/
│   │   ├── README.md                    # Restructure overview, deliverables, & validation
│   │   ├── DIRECTORY_LAYOUT.md          # Before-and-after structural comparison & benefits
│   │   └── GIT_WORKFLOW.md              # Demonstration of Git commands, branch & atomic commits
│   └── week-03-create-and-merge-feature-branches/
│       ├── README.md                    # Week 03 practice overview & deliverable index
│       ├── BRANCHING.md                 # Complete branching strategy & merge documentation
│       ├── PR_01_BRANCH_VALIDATOR.md    # Pull Request deliverable for Feature Branch 1
│       ├── PR_02_MERGE_ANALYZER.md      # Pull Request deliverable for Feature Branch 2
│       ├── PR_03_PR_LIFECYCLE_MANAGER.md# Pull Request deliverable for Feature Branch 3
│       └── MERGE_HISTORY_AUDIT.md       # Merge commit topology graph and hygiene audit
├── scripts/                             # Automation, maintenance, and verification tooling
│   ├── run_atomic_commits_practice.ps1  # Automated atomic commits practice runner & Git publisher
│   ├── run_basic_git_workflow_practice.ps1 # Automated basic git workflow runner & remote publisher
│   ├── run_conflict_resolution.ps1      # Automated conflict resolution workflow script
│   ├── run_feature_branches_practice.ps1# Automated feature branch creation, push & merge runner
│   ├── run_gitignore_practice.ps1       # Automated .gitignore workflow runner
│   ├── run_repo_restructure.ps1         # Automated repo restructure & atomic commit runner
│   ├── verify_basic_git_workflow.py     # Automated basic git workflow & sync auditor
│   ├── verify_commit_history.py         # Automated commit history & Conventional Commits validator
│   ├── verify_feature_branches.py       # Automated feature branches & clean merge history validator
│   ├── verify_gitignore.py              # Automated .gitignore pattern & clean repo validator
│   └── verify_structure.py              # Python structural validation & compliance checker
├── src/                                 # Reusable core library packages and utilities
│   ├── __init__.py                      # Package initialization marker
│   └── utils/                           # Shared utility modules
│       ├── __init__.py                  # Utility package exports
│       ├── branch_validator.py          # Automated branch naming convention & hygiene validator
│       ├── commit_validator.py          # Conventional Commits parser and validation engine
│       ├── env_helper.py                # Environment variable reader with type safety
│       ├── git_ops.py                   # Git operations, state inspection, and workflow tracker
│       ├── logger.py                    # Standardized structured console logger
│       ├── merge_analyzer.py            # Merge history analyzer & clean commit auditor
│       └── pr_lifecycle.py              # PR lifecycle state machine and checklist manager
├── tests/                               # Comprehensive automated test suites
│   ├── __init__.py                      # Test package marker
│   ├── test_branch_validator.py         # Unit tests for branch naming & hygiene rules
│   ├── test_commit_validator.py         # Unit tests for Conventional Commits rules
│   ├── test_git_ops.py                  # Unit tests for Git workflow tracker and state helpers
│   ├── test_gitignore_rules.py          # Unit tests for .gitignore pattern matching
│   ├── test_merge_analyzer.py           # Unit tests for merge commit analysis & hygiene
│   ├── test_pr_lifecycle.py             # Unit tests for PR lifecycle states & checklist gates
│   └── test_repo_structure.py           # Integrity tests for repository layout & utilities
├── .gitignore                           # Comprehensive multi-environment ignore rules
├── BRANCHING.md                         # Root branching strategy & merge protocol documentation
└── README.md                            # Main portfolio hub and navigation index
```

---

## Directory Rationale & Technical Benefits

| Directory / File | Responsibility & Purpose | Technical Benefit |
| :--- | :--- | :--- |
| **`.github/`** | Repository governance, issue forms, PR review template | Establishes automated consistency for team issues, PR submissions, and code reviews. |
| **`docs/`** | Technical architecture, guidelines, directory references | Centralizes system knowledge, speeding up developer onboarding and code review. |
| **`practice/`** | Weekly technical tasks and portfolio milestones | Encapsulates challenge deliverables without polluting production source packages. |
| **`scripts/`** | Shell and Python automation scripts | Eliminates manual, error-prone commands through one-click, reproducible scripts. |
| **`src/`** | Core reusable business logic and utility libraries | Follows Python packaging conventions, enabling modular import paths (`from src.utils.logger import ...`). |
| **`tests/`** | Automated unit, regression, and structural tests | Ensures code reliability, prevents regressions, and enables automated CI verification. |
| **`.gitignore`** | Multi-stack ignore rules (Python, Node, OS, IDE, Secrets) | Prevents accidental leak of sensitive credentials, large caches, and OS artifacts. |
| **`BRANCHING.md`** | Branching taxonomy, lifecycle & merge strategy guide | Ensures all team members and reviewers follow identical branching and merge protocols. |
| **`README.md`** | Root portfolio entry point & navigation hub | Provides an immediate high-impact overview of all projects, badges, and quick start guides. |

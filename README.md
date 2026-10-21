# SahkaarX Engineering Stage Portfolio

[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![Git](https://img.shields.io/badge/git-feature--branches-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()
[![Standard](https://img.shields.io/badge/commits-conventional-orange.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

Welcome to the **SahkaarX Engineering Stage Portfolio**. This repository is an enterprise-grade engineering workspace demonstrating professional software engineering workflows, clean modular repository architecture, continuous integration verification, and disciplined Git version control practices.

---

## 🏛️ Repository Architecture

The repository enforces a strict **Separation of Concerns** separating core business modules, test suites, automation tooling, documentation, and weekly engineering challenge deliverables:

```text
sahkaarx-stage-portfolio-d5b2372f/
├── .github/                             # Repository governance & review templates
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md                # Standardized bug reporting form
│   │   └── feature_request.md           # Standardized feature proposal form
│   └── PULL_REQUEST_TEMPLATE.md         # PR submission checklist
├── docs/                                # Central architecture & engineering guidelines
│   ├── ARCHITECTURE.md                  # System design & architectural principles
│   ├── CONTRIBUTING.md                  # Branching model & Conventional Commits guide
│   └── DIRECTORY_STRUCTURE.md           # Full directory layout reference & rationale
├── practice/                            # Milestone challenge deliverables
│   ├── week-01-create-intentional-merge-conflicts-and-resolve/
│   │   ├── README.md                    # Conflict simulation & multi-strategy resolution
│   │   ├── auth_service.py              # Harmonized JWT + OAuth2 authentication service
│   │   ├── conflict_markers_example.md  # Git conflict marker walkthrough
│   │   └── test_auth_service.py         # Unit tests validating resolved implementation
│   └── week-02-restructure-portfolio-repo-with-professional-org/
│       ├── README.md                    # Restructure overview & verification guide
│       ├── DIRECTORY_LAYOUT.md          # Before-and-after structural comparison matrix
│       └── GIT_WORKFLOW.md              # Demonstration of Git commands & atomic commits
├── scripts/                             # Automation, maintenance, and verification tooling
│   ├── run_conflict_resolution.ps1      # Automated conflict resolution workflow script
│   ├── run_repo_restructure.ps1         # Automated repo restructure & commit runner
│   └── verify_structure.py              # Structural compliance & integrity checker
├── src/                                 # Reusable core library packages
│   ├── __init__.py                      # Package initialization marker
│   └── utils/                           # Shared utility library
│       ├── __init__.py                  # Utility package exports
│       ├── env_helper.py                # Environment variable reader with type validation
│       └── logger.py                    # Standardized structured console logger
├── tests/                               # Comprehensive automated test suites
│   ├── __init__.py                      # Test package marker
│   └── test_repo_structure.py           # Unit tests for structure & core utilities
├── .gitignore                           # Comprehensive multi-environment ignore file
└── README.md                            # Main portfolio hub & navigation index
```

---

## 🚀 Weekly Practices & Engineering Milestones

### [Week 01: Create Intentional Merge Conflicts and Resolve](practice/week-01-create-intentional-merge-conflicts-and-resolve/README.md)
- **Focus**: Git branch divergence, simulation of real merge conflicts between `feature/jwt-auth` and `feature/oauth2-auth`, analyzing conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>>`), resolving code into a unified multi-strategy pattern, and pushing clean history to GitHub.
- **Key Artifacts**: [`auth_service.py`](practice/week-01-create-intentional-merge-conflicts-and-resolve/auth_service.py), [`conflict_markers_example.md`](practice/week-01-create-intentional-merge-conflicts-and-resolve/conflict_markers_example.md), [`run_conflict_resolution.ps1`](scripts/run_conflict_resolution.ps1).

### [Week 02 Practice: .gitignore Configuration and Repository Cleanliness](practice/week-02-practice-gitignore-configuration-and-repository/README.md)
- **Focus**: Establishing a production-grade multi-environment [`.gitignore`](.gitignore) protecting secrets, excluding Python build artifacts, virtual environments, and OS/IDE clutter; demonstrating 100% clean repository state and negative index verification on feature branch [`feature/gitignore-config`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/gitignore-config).
- **Key Artifacts**: [Excluded Patterns Reference](practice/week-02-practice-gitignore-configuration-and-repository/EXCLUDED_PATTERNS.md), [Clean Repo Verification Report](practice/week-02-practice-gitignore-configuration-and-repository/CLEAN_REPO_VERIFICATION.md), [`scripts/verify_gitignore.py`](scripts/verify_gitignore.py), [`tests/test_gitignore_rules.py`](tests/test_gitignore_rules.py).

### [Week 02: Restructure Portfolio Repo with Professional Organization](practice/week-02-restructure-portfolio-repo-with-professional-org/README.md)
- **Focus**: Reorganizing repository into an enterprise directory structure, building a multi-environment [`.gitignore`](.gitignore), establishing central documentation in [`docs/`](docs/), modularizing utilities in [`src/`](src/), adding unit tests in [`tests/`](tests/), automating verification in [`scripts/`](scripts/), and demonstrating atomic Git commits on feature branch [`feature/repo-restructure`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/repo-restructure).
- **Key Artifacts**: [Directory Layout Analysis](practice/week-02-restructure-portfolio-repo-with-professional-org/DIRECTORY_LAYOUT.md), [Git Workflow & Atomic Commits](practice/week-02-restructure-portfolio-repo-with-professional-org/GIT_WORKFLOW.md).

---

## 🛠️ Quick Start & Verification

### 1. Verify Repository Integrity & Structure
Run the automated validation script to verify directory presence, `.gitignore` rules, and branch status:
```bash
python scripts/verify_structure.py
```

### 2. Verify .gitignore Rules & Repository Cleanliness
Run the automated `.gitignore` compliance checker:
```bash
python scripts/verify_gitignore.py
```

### 3. Run Automated Test Suite
Execute unit tests validating core utilities, `.gitignore` rules, and structural contracts:
```bash
python -m unittest discover tests/
```

### 3. Run Week 01 Auth Service Tests
```bash
python practice/week-01-create-intentional-merge-conflicts-and-resolve/test_auth_service.py
```

---

## 📐 Engineering Guidelines
- **Architecture**: See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for design patterns and system flow.
- **Directory Details**: See [`docs/DIRECTORY_STRUCTURE.md`](docs/DIRECTORY_STRUCTURE.md) for rationale and benefits.
- **Contributing & Commits**: See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for the branching strategy and Conventional Commits format.

---

## 🔗 Repository Information
- **GitHub Repository**: [https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)
- **Primary Feature Branch**: [`feature/repo-restructure`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/repo-restructure)

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
│   ├── BRANCHING.md                     # Engineering branching strategy & merge protocol
│   ├── CONTRIBUTING.md                  # Branching model & Conventional Commits guide
│   └── DIRECTORY_STRUCTURE.md           # Full directory layout reference & rationale
├── practice/                            # Milestone challenge deliverables
│   ├── week-01-create-intentional-merge-conflicts-and-resolve/
│   ├── week-02-practice-atomic-commits-and-clear-messaging/
│   ├── week-02-practice-basic-git-workflow-with-multiple-commit/
│   ├── week-02-practice-gitignore-configuration-and-repository/
│   ├── week-02-restructure-portfolio-repo-with-professional-org/
│   ├── week-03-create-and-merge-feature-branches/
│   └── week-06-finalize-capstone-integrate-variables-data-types/
│       ├── README.md                    # Week 06 Capstone overview & verification
│       ├── PULL_REQUEST.md              # PR #4 deliverable & review resolution
│       ├── VARIABLES_AND_SCOPE_GUIDE.md # Deep-dive guide on variables, types & LEGB
│       └── CAPSTONE_FINALIZATION_REPORT.md # Comprehensive portfolio audit & certification
├── scripts/                             # Automation, maintenance, and verification tooling
│   ├── run_capstone_finalization.ps1    # Automated capstone branch, commits, PR merge & push runner
│   ├── verify_variables_data_types.py   # Automated capstone type conversion & scope engine validator
│   ├── run_feature_branches_practice.ps1# Automated feature branch creation, push & merge runner
│   ├── verify_feature_branches.py       # Automated feature branch & merge validator
│   ├── verify_structure.py              # Structural compliance & integrity checker
│   └── ...                              # Weekly runners and compliance validators
├── src/                                 # Reusable core library packages
│   ├── __init__.py                      # Package initialization marker & public exports
│   ├── variables_data_types.py          # Type conversion engine, LEGB scope manager & data protection
│   └── utils/                           # Shared utility library
│       ├── branch_validator.py          # Automated branch naming convention & hygiene validator
│       ├── merge_analyzer.py            # Merge history analyzer & clean commit auditor
│       ├── pr_lifecycle.py              # PR lifecycle state machine and checklist manager
│       ├── commit_validator.py          # Conventional Commits validator
│       ├── git_ops.py                   # Git operations & workflow tracker
│       ├── env_helper.py                # Environment variable reader
│       └── logger.py                    # Structured console logger
├── tests/                               # Comprehensive automated test suites
│   ├── test_variables_data_types.py     # Unit tests for type conversion, LEGB scope & closures
│   ├── test_branch_validator.py         # Unit tests for branch naming & hygiene rules
│   ├── test_merge_analyzer.py           # Unit tests for merge commit analysis
│   ├── test_pr_lifecycle.py             # Unit tests for PR lifecycle states & checklist gates
│   └── ...                              # Test suites for structure, gitignore, and commit rules
├── .gitignore                           # Comprehensive multi-environment ignore file
├── BRANCHING.md                         # Engineering branching strategy & merge protocol
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

### [Week 02 Practice: Atomic Commits and Clear Messaging](practice/week-02-practice-atomic-commits-and-clear-messaging/README.md)
- **Focus**: Structuring a clean linear Git history adhering strictly to [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), enforcing single-purpose commits, imperative mood commit messages, and automated verification of Git history on feature branch [`feature/atomic-commits-and-messaging`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/atomic-commits-and-messaging).
- **Key Artifacts**: [Atomic Commits Guide](practice/week-02-practice-atomic-commits-and-clear-messaging/ATOMIC_COMMITS_GUIDE.md), [Commit Log Audit](practice/week-02-practice-atomic-commits-and-clear-messaging/COMMIT_LOG_AUDIT.md), [`src/utils/commit_validator.py`](src/utils/commit_validator.py), [`tests/test_commit_validator.py`](tests/test_commit_validator.py), [`scripts/verify_commit_history.py`](scripts/verify_commit_history.py), [`scripts/run_atomic_commits_practice.ps1`](scripts/run_atomic_commits_practice.ps1).

### [Week 02 Practice: Basic Git Workflow with Multiple Commits](practice/week-02-practice-basic-git-workflow-with-multiple-commit/README.md)
- **Focus**: Demonstrating proficiency with core Git commands (`add`, `commit`, `pull`, `push`), executing 3+ atomic commits on dedicated feature branch [`feature/basic-git-workflow`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/basic-git-workflow), synchronizing with `main` via `pull`, and preparing a verified Pull Request ready for merge.
- **Key Artifacts**: [Git Workflow Guide](practice/week-02-practice-basic-git-workflow-with-multiple-commit/GIT_WORKFLOW_GUIDE.md), [Commit History Audit](practice/week-02-practice-basic-git-workflow-with-multiple-commit/COMMIT_HISTORY_AUDIT.md), [Pull Request Specification](practice/week-02-practice-basic-git-workflow-with-multiple-commit/PULL_REQUEST.md), [`src/utils/git_ops.py`](src/utils/git_ops.py), [`tests/test_git_ops.py`](tests/test_git_ops.py), [`scripts/verify_basic_git_workflow.py`](scripts/verify_basic_git_workflow.py), [`scripts/run_basic_git_workflow_practice.ps1`](scripts/run_basic_git_workflow_practice.ps1).

### [Week 03 Practice: Create and Merge Feature Branches](practice/week-03-create-and-merge-feature-branches/README.md)
- **Focus**: Establishing a formal branching strategy, implementing 3 feature branches following `<type>/<description>` naming conventions, making atomic Conventional Commits, publishing branches to GitHub, executing clean non-fast-forward (`--no-ff`) merges to `main` without unnecessary commits, and documenting PR deliverables and topology audit.
- **Key Artifacts**: [`BRANCHING.md`](BRANCHING.md), [`practice/week-03-create-and-merge-feature-branches/BRANCHING.md`](practice/week-03-create-and-merge-feature-branches/BRANCHING.md), [`PR_01_BRANCH_VALIDATOR.md`](practice/week-03-create-and-merge-feature-branches/PR_01_BRANCH_VALIDATOR.md), [`PR_02_MERGE_ANALYZER.md`](practice/week-03-create-and-merge-feature-branches/PR_02_MERGE_ANALYZER.md), [`PR_03_PR_LIFECYCLE_MANAGER.md`](practice/week-03-create-and-merge-feature-branches/PR_03_PR_LIFECYCLE_MANAGER.md), [`MERGE_HISTORY_AUDIT.md`](practice/week-03-create-and-merge-feature-branches/MERGE_HISTORY_AUDIT.md), [`src/utils/branch_validator.py`](src/utils/branch_validator.py), [`src/utils/merge_analyzer.py`](src/utils/merge_analyzer.py), [`src/utils/pr_lifecycle.py`](src/utils/pr_lifecycle.py), [`scripts/verify_feature_branches.py`](scripts/verify_feature_branches.py), [`scripts/run_feature_branches_practice.ps1`](scripts/run_feature_branches_practice.ps1).

### [Week 06 Capstone: Finalize Capstone — Integrate Variables & Data Types Module](practice/week-06-finalize-capstone-integrate-variables-data-types/README.md)
- **Focus**: Finalizing the engineering portfolio capstone with a production-grade Variables & Data Types module, implementing lossless explicit type conversions (primitives, Decimals, datetimes, collections), Python's LEGB (Local, Enclosing, Global, Built-in) variable scope resolution order, stateful closures with `nonlocal`, audited global state modification, comprehensive unit testing, and clean non-fast-forward (`--no-ff`) merge of PR #4 on [`feature/variables-data-types`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/variables-data-types).
- **Key Artifacts**: [`src/variables_data_types.py`](src/variables_data_types.py), [`tests/test_variables_data_types.py`](tests/test_variables_data_types.py), [Pull Request Specification](practice/week-06-finalize-capstone-integrate-variables-data-types/PULL_REQUEST.md), [Variables & Scope Engineering Guide](practice/week-06-finalize-capstone-integrate-variables-data-types/VARIABLES_AND_SCOPE_GUIDE.md), [Capstone Finalization Report](practice/week-06-finalize-capstone-integrate-variables-data-types/CAPSTONE_FINALIZATION_REPORT.md), [`scripts/verify_variables_data_types.py`](scripts/verify_variables_data_types.py), [`scripts/run_capstone_finalization.ps1`](scripts/run_capstone_finalization.ps1), [`execute_capstone_workflow.py`](execute_capstone_workflow.py).

---

## 🛠️ Quick Start & Verification

### 1. Verify Capstone Variables & Data Types (Week 06)
Validate deliverables, type conversion rules, variable scope resolution, and unit tests:
```bash
python scripts/verify_variables_data_types.py
```

### 2. Verify Feature Branches & Clean Merges (Week 03)
Validate the 3 feature branches, clean merge history, and unit tests:
```bash
python scripts/verify_feature_branches.py
```

### 3. Verify Repository Integrity & Structure
Run the automated validation script to verify directory presence, `.gitignore` rules, and branch status:
```bash
python scripts/verify_structure.py
```

### 4. Verify .gitignore Rules & Repository Cleanliness
Run the automated `.gitignore` compliance checker:
```bash
python scripts/verify_gitignore.py
```

### 5. Verify Atomic Commits & Git History Compliance
Validate that the feature branch contains 4+ atomic commits adhering to Conventional Commits:
```bash
python scripts/verify_commit_history.py
```

### 6. Verify Basic Git Workflow & Multiple Commits
Validate the feature branch, 3+ atomic commits, and command lifecycle:
```bash
python scripts/verify_basic_git_workflow.py
```

### 7. Run Automated Test Suite
Execute unit tests validating core utilities, Git operations, commit validation rules, `.gitignore` rules, and structural contracts:
```bash
python -m unittest discover tests/
```

### 8. Run Week 01 Auth Service Tests
```bash
python practice/week-01-create-intentional-merge-conflicts-and-resolve/test_auth_service.py
```

---

## 📐 Engineering Guidelines
- **Branching Strategy**: See [`BRANCHING.md`](BRANCHING.md) for full taxonomy, lifecycle, and merge protocols.
- **Architecture**: See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for design patterns and system flow.
- **Directory Details**: See [`docs/DIRECTORY_STRUCTURE.md`](docs/DIRECTORY_STRUCTURE.md) for rationale and benefits.
- **Contributing & Commits**: See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for Conventional Commits format.

---

## 🔗 Repository Information
- **GitHub Repository**: [https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)
- **Primary Feature Branches**:
  - [`feature/variables-data-types`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/variables-data-types) (Week 06 Capstone: Variables & Data Types Module)
  - [`feature/branch-strategy-validator`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/branch-strategy-validator) (Week 03 Branch Strategy Validator)
  - [`feature/merge-history-analyzer`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/merge-history-analyzer) (Week 03 Merge History Analyzer)
  - [`feature/pr-lifecycle-manager`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/pr-lifecycle-manager) (Week 03 PR Lifecycle Manager)
  - [`feature/basic-git-workflow`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/basic-git-workflow) (Week 02 Basic Git Workflow Practice)
  - [`feature/atomic-commits-and-messaging`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/atomic-commits-and-messaging) (Week 02 Atomic Commits Practice)
  - [`feature/gitignore-config`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/gitignore-config) (Week 02 .gitignore Practice)
  - [`feature/repo-restructure`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/repo-restructure) (Week 02 Restructure Practice)



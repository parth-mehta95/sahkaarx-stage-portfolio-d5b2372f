# SahkaarX Branching Strategy & Git Merge Protocol

> **Repository**: [parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)  
> **Standard**: Production GitHub Flow with Strict Conventional Commits & Clean Merge Topology  
> **Practice Milestone**: [Week 03: Create and Merge Feature Branches](../practice/week-03-create-and-merge-feature-branches/README.md)  
> **Status**: Verified & Active in Production  

---

## 📖 Executive Summary

In a modern high-velocity continuous integration and deployment (CI/CD) environment, software stability and team scalability depend on a clean, predictable, and traceable version control discipline.

This document defines the **SahkaarX Engineering Branching Strategy**, establishing:
1. **Standardized Branch Taxonomy & Naming Conventions** to immediately convey intent, scope, and ownership.
2. **End-to-End Branch Lifecycle** from checkout, atomic development, rebasing, and peer review to integration.
3. **Clean Merge Strategy** ensuring that integration into the `main` trunk preserves discrete feature context while eliminating redundant, messy, or unverified commits.
4. **Pull Request Protocol & Verification Gates** that every branch must satisfy prior to merge approval.

---

## 🌿 1. Core Branching Model: Enhanced GitHub Flow

Our repository utilizes an **Enhanced GitHub Flow** architecture. The `main` branch is protected, immutable without code review, and always represents releasable, production-ready code.

```text
main (production-ready trunk, CI protected)
 │
 ├── [Branch Out] ───────┐
 │                       ▼
 │             feature/branch-strategy-validator
 │             ├── feat(branch-validator): implement branch naming validator
 │             └── test(branch-validator): add unit tests
 │                       │
 │  ┌────────────────────┘ [PR #1: Verified & Approved]
 │  ▼
 * Merge pull request #1 from feature/branch-strategy-validator (--no-ff)
 │
 ├── [Branch Out] ───────┐
 │                       ▼
 │             feature/merge-history-analyzer
 │             ├── feat(merge-analyzer): implement commit history auditor
 │             └── test(merge-analyzer): add unit tests
 │                       │
 │  ┌────────────────────┘ [PR #2: Verified & Approved]
 │  ▼
 * Merge pull request #2 from feature/merge-history-analyzer (--no-ff)
 │
 ├── [Branch Out] ───────┐
 │                       ▼
 │             feature/pr-lifecycle-manager
 │             ├── feat(pr-lifecycle): implement PR lifecycle manager
 │             └── test(pr-lifecycle): add unit tests
 │                       │
 │  ┌────────────────────┘ [PR #3: Verified & Approved]
 │  ▼
 * Merge pull request #3 from feature/pr-lifecycle-manager (--no-ff)
 │
 ├── [Branch Out] ───────┐
 │                       ▼
 │             feature/variables-data-types
 │             ├── feat(variables-data-types): implement core type conversion and variable scope module
 │             ├── test(variables-data-types): add unit tests
 │             ├── docs(capstone): document variables data types guide, pr deliverable, and capstone finalization
 │             └── chore(portfolio): finalize capstone repository integration and verify production readiness
 │                       │
 │  ┌────────────────────┘ [PR #4: Verified & Approved - Capstone Finalization]
 │  ▼
 * Merge pull request #4 from feature/variables-data-types (--no-ff)
 │
 ▼ (Clean, linear integration graph with traceable feature histories)
```

---

## 🏷️ 2. Branch Taxonomy & Naming Conventions

All branch names must be lowercase, use hyphens (`kebab-case`) for words, and be prefixed with a recognized operational scope.

### Standard Branch Types

| Prefix | Intent / Scope | Lifecycle | Example |
| :--- | :--- | :--- | :--- |
| `feature/` | New business logic, capabilities, or architectural modules | Short-lived (1–5 days) | `feature/branch-strategy-validator` |
| `bugfix/` | Defect remediation, edge case handling, or regression fixes | Short-lived (1–3 days) | `bugfix/git-ops-divergence-handling` |
| `hotfix/` | Critical production patches bypassing normal staging cycles | Urgent (< 24 hours) | `hotfix/auth-token-validation-patch` |
| `docs/` | Pure documentation, architecture guides, and API specs | Short-lived | `docs/update-branching-guidelines` |
| `refactor/` | Internal restructuring without modifying external behavior | Short-lived (1–3 days) | `refactor/optimize-git-history-parser` |
| `chore/` | Tooling updates, CI pipelines, and dependency bumps | Short-lived | `chore/update-verification-scripts` |
| `test/` | Adding test suites, mock fixtures, or benchmark suites | Short-lived | `test/add-merge-analyzer-test-matrix` |

### Formal Naming Syntax

```text
<prefix>/[<TICKET-ID>-]<kebab-case-description>
```

---

## 🔀 3. Merge Strategies & Clean History Enforcement

A clean commit history makes bisecting regressions, generating automated release notes, and reviewing code effortless. We reject noisy, uncurated Git histories.

### Strategy Comparison Matrix

| Strategy | Command / GitHub Mode | When to Use | Advantages | Considerations |
| :--- | :--- | :--- | :--- | :--- |
| **Non-Fast-Forward Merge Commit (`--no-ff`)** | `git merge --no-ff <branch>` / "Create a merge commit" | Multi-commit features where logical sequence should be preserved | Clear feature boundary; easy single-commit rollback (`git revert -m 1 <hash>`) | Creates an explicit merge commit |
| **Squash and Merge** | `git merge --squash <branch>` / "Squash and merge" | Small tasks, bugfixes, or branches with messy intermediate WIP commits | Condenses entire branch into 1 atomic commit on `main`; completely linear history | Discards individual intermediate commit timestamps |
| **Rebase and Merge** | `git rebase main` + fast-forward / "Rebase and merge" | High-discipline teams where every single branch commit is clean and atomic | Completely linear history without merge commits | Feature grouping boundaries are not explicitly recorded |

---

## 🚀 4. Week 03 Implemented Feature Branches

In fulfillment of Week 03 deliverables, 3 dedicated feature branches were created, committed with Conventional Commits, pushed to GitHub, and cleanly merged into `main`:

1. `feature/branch-strategy-validator`: Automated branch naming convention and hygiene validator ([PR #1](../practice/week-03-create-and-merge-feature-branches/PR_01_BRANCH_VALIDATOR.md))
2. `feature/merge-history-analyzer`: Merge history analysis and commit graph auditor ([PR #2](../practice/week-03-create-and-merge-feature-branches/PR_02_MERGE_ANALYZER.md))
3. `feature/pr-lifecycle-manager`: Pull request lifecycle manager and checklist validator ([PR #3](../practice/week-03-create-and-merge-feature-branches/PR_03_PR_LIFECYCLE_MANAGER.md))

---

## 📋 5. Verification Commands

```bash
python -m unittest discover tests/
python scripts/verify_feature_branches.py
python scripts/verify_structure.py
```

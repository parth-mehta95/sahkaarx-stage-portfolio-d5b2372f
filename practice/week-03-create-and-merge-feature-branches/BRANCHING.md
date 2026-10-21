# SahkaarX Branching Strategy & Git Merge Protocol

> **Repository**: [parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)  
> **Standard**: Production GitHub Flow with Strict Conventional Commits & Clean Merge Topology  
> **Practice Milestone**: [Week 03: Create and Merge Feature Branches](README.md)  
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
 ▼ (Clean, linear integration graph with traceable feature histories)
```

### Architectural Principles:
1. **Single Source of Truth**: All deployable artifacts originate from `main`.
2. **Ephemeral Branches**: Feature and bugfix branches exist only for the duration of the feature delivery and are promptly deleted post-merge.
3. **Zero Direct Commits on `main`**: All code enters `main` exclusively through vetted Pull Requests.
4. **Continuous Synchronization**: Feature branches frequently sync with upstream `main` to catch and resolve divergence before opening or merging PRs.

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

- **Prefix**: Exactly one of `feature`, `bugfix`, `hotfix`, `docs`, `refactor`, `chore`, `test`.
- **Delimiter**: Exactly one forward slash (`/`).
- **Ticket ID (Optional)**: e.g. `PROJ-101-`, `ENG-404-`.
- **Descriptor**: 3 to 45 alphanumeric characters, lowercase, separated by single hyphens.

### Anti-Patterns to Reject

| Bad Branch Name | Why Rejected | Correct Alternative |
| :--- | :--- | :--- |
| `my-feature` | Missing scope prefix (`feature/`, `bugfix/`) | `feature/user-dashboard` |
| `feature/Add_Login` | Contains uppercase and underscores | `feature/add-login` |
| `temp_wip_test` | Vague, untracked, no prefix | `feature/prototype-cache-layer` |
| `parth-branch` | Named after developer instead of functional deliverable | `feature/merge-history-analyzer` |
| `feature/` | Missing descriptor | `feature/pr-lifecycle-manager` |
| `feature/update` | Generic, nondescript descriptor | `feature/audit-branch-naming` |

---

## 🔄 3. End-to-End Branch Lifecycle

```text
[1. Checkout] ──> [2. Atomic Commits] ──> [3. Local Tests] ──> [4. Sync Main] ──> [5. Push & PR] ──> [6. Clean Merge]
```

### Step 1: Branch Creation
Always start from an up-to-date `main` branch:
```bash
git checkout main
git pull origin main
git checkout -b feature/branch-strategy-validator
```

### Step 2: Atomic Commits with Conventional Commits
Make focused, single-purpose commits that compile and pass tests independently:
```bash
git add src/utils/branch_validator.py
git commit -m "feat(branch-validator): implement automated git branch naming convention validator"

git add tests/test_branch_validator.py
git commit -m "test(branch-validator): add comprehensive unit test suite for branch validator"
```

### Step 3: Local Verification & Linting
Run all automated test suites and repository verifications before pushing:
```bash
python -m unittest discover tests/
python scripts/verify_structure.py
```

### Step 4: Upstream Synchronization
Rebase or merge the latest `main` into your feature branch to prevent divergence:
```bash
git fetch origin
git merge origin/main --no-edit
```

### Step 5: Remote Delivery & Pull Request Creation
Push branch to GitHub with upstream tracking:
```bash
git push -u origin feature/branch-strategy-validator
```
Open a Pull Request on GitHub adhering to `.github/PULL_REQUEST_TEMPLATE.md`.

### Step 6: Code Review & Verification Gates
PR must satisfy all criteria:
- Minimum of 1 peer approval.
- Automated CI suites pass 100%.
- Branch naming convention validated.
- Zero extraneous files committed.

### Step 7: Clean Merge Execution
Execute non-fast-forward merge (`--no-ff`) or squash merge to preserve clean history.

### Step 8: Post-Merge Branch Pruning
Delete local and remote branches to keep the repository clean:
```bash
git checkout main
git pull origin main
git branch -d feature/branch-strategy-validator
git push origin --delete feature/branch-strategy-validator
```

---

## 🔀 4. Merge Strategies & Clean History Enforcement

A clean commit history makes bisecting regressions, generating automated release notes, and reviewing code effortless. We reject noisy, uncurated Git histories.

### Strategy Comparison Matrix

| Strategy | Command / GitHub Mode | When to Use | Advantages | Considerations |
| :--- | :--- | :--- | :--- | :--- |
| **Non-Fast-Forward Merge Commit (`--no-ff`)** | `git merge --no-ff <branch>` / "Create a merge commit" | Multi-commit features where logical sequence should be preserved | Clear feature boundary; easy single-commit rollback (`git revert -m 1 <hash>`) | Creates an explicit merge commit |
| **Squash and Merge** | `git merge --squash <branch>` / "Squash and merge" | Small tasks, bugfixes, or branches with messy intermediate WIP commits | Condenses entire branch into 1 atomic commit on `main`; completely linear history | Discards individual intermediate commit timestamps |
| **Rebase and Merge** | `git rebase main` + fast-forward / "Rebase and merge" | High-discipline teams where every single branch commit is clean and atomic | Completely linear history without merge commits | Feature grouping boundaries are not explicitly recorded |

### Preventing Unnecessary Commits

Our repository enforces the following rules to eliminate clutter:
1. **No WIP / Temporary Commits on `main`**: Commits like `"wip"`, `"temp"`, `"try again"`, or `"asdf"` are strictly blocked.
2. **No Pointless Micro-Fixes**: Commits like `"fix typo"` or `"oops"` must be squashed via `git rebase -i` into the parent commit before PR approval.
3. **No Back-Merge Clutter**: Avoid frequent `"Merge branch 'main' into feature"` commits. Use `git rebase main` on local feature branches.

---

## 🚀 5. Week 03 Implemented Feature Branches

In fulfillment of Week 03 deliverables, 3 dedicated feature branches were created, committed with Conventional Commits, pushed to GitHub, and cleanly merged into `main`:

### Feature Branch 1: `feature/branch-strategy-validator`
- **Scope**: Implements [`src/utils/branch_validator.py`](../../src/utils/branch_validator.py) and [`tests/test_branch_validator.py`](../../tests/test_branch_validator.py).
- **Capabilities**: Validates branch names against standard prefix conventions, detects trunk branches, enforces kebab-case syntax, and flags anti-patterns.
- **Commits**:
  1. `feat(branch-validator): implement automated git branch naming convention and hygiene validator`
  2. `test(branch-validator): add comprehensive unit test suite for branch validator`
- **PR Deliverable**: [`PR_01_BRANCH_VALIDATOR.md`](PR_01_BRANCH_VALIDATOR.md)
- **Merge Status**: ✅ Cleanly merged into `main` with `--no-ff`.

### Feature Branch 2: `feature/merge-history-analyzer`
- **Scope**: Implements [`src/utils/merge_analyzer.py`](../../src/utils/merge_analyzer.py) and [`tests/test_merge_analyzer.py`](../../tests/test_merge_analyzer.py).
- **Capabilities**: Analyzes Git commit graph, audits merge commits, detects PR numbers and source branches, and flags unhygienic commits (WIP, typo, temp).
- **Commits**:
  1. `feat(merge-analyzer): add merge history analysis and commit graph auditor`
  2. `test(merge-analyzer): add unit test coverage for merge commit history analysis`
- **PR Deliverable**: [`PR_02_MERGE_ANALYZER.md`](PR_02_MERGE_ANALYZER.md)
- **Merge Status**: ✅ Cleanly merged into `main` with `--no-ff`.

### Feature Branch 3: `feature/pr-lifecycle-manager`
- **Scope**: Implements [`src/utils/pr_lifecycle.py`](../../src/utils/pr_lifecycle.py) and [`tests/test_pr_lifecycle.py`](../../tests/test_pr_lifecycle.py).
- **Capabilities**: Models PR states (`OPEN`, `IN_REVIEW`, `APPROVED`, `MERGED`), verifies PR readiness checklists, and auto-generates markdown conforming to `.github/PULL_REQUEST_TEMPLATE.md`.
- **Commits**:
  1. `feat(pr-lifecycle): implement pull request lifecycle manager and checklist validator`
  2. `test(pr-lifecycle): add unit tests verifying pull request states and markdown generation`
- **PR Deliverable**: [`PR_03_PR_LIFECYCLE_MANAGER.md`](PR_03_PR_LIFECYCLE_MANAGER.md)
- **Merge Status**: ✅ Cleanly merged into `main` with `--no-ff`.

---

## 🛠️ 6. Verification and Automation Tooling

To ensure repeatable compliance, the repository provides automated verifiers and runners:

```bash
# 1. Run all unit tests
python -m unittest discover tests/

# 2. Verify Week 03 feature branches and merge history
python scripts/verify_feature_branches.py

# 3. Verify general repository structural integrity
python scripts/verify_structure.py
```

---

## 📋 7. Pull Request Review Checklist

Prior to requesting review or merging, each engineer must verify:
- [x] Branch name matches `<type>/<description>` convention.
- [x] All commits follow [Conventional Commits v1.0.0](https://www.conventionalcommits.org/).
- [x] Unit test suites pass with zero regressions (`python -m unittest discover tests/`).
- [x] Repository verification passes (`python scripts/verify_structure.py`).
- [x] No secrets, build artifacts, or IDE clutter committed.
- [x] Commit history is clean with zero unnecessary or WIP commits.
- [x] Merge into `main` performed with clean merge commit preserving history.

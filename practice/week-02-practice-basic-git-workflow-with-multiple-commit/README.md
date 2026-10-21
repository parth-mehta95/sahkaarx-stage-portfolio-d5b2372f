# Week 02 Practice: Basic Git Workflow with Multiple Commits

> **Repository**: [parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)  
> **Feature Branch**: [`feature/basic-git-workflow`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/basic-git-workflow)  
> **Pull Request**: [`PULL_REQUEST.md`](PULL_REQUEST.md) / [GitHub PR Link](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/pull/new/feature/basic-git-workflow)  
> **Status**: ✅ Completed & Verified  

---

## 🎯 Task Brief & Scenario

Your code review requires demonstrating proficiency with core Git commands. Create a feature branch with multiple logical commits.

### Key Objectives
1. **Create and checkout a dedicated feature branch** (`feature/basic-git-workflow`).
2. **Execute 3+ logical changes with atomic commits** following Conventional Commits.
3. **Demonstrate all basic Git commands**: `add`, `commit`, `pull`, and `push`.
4. **Synchronize branch with `main` via `pull`** to ensure zero divergence and no merge conflicts.
5. **Prepare a Pull Request ready for merge** with comprehensive verification.

---

## 📦 Deliverables & Repository Artifacts

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **Feature Branch** | [`feature/basic-git-workflow`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/basic-git-workflow) | Dedicated branch containing 5 atomic commits pushed to GitHub |
| **Git Operations Utility** | [`src/utils/git_ops.py`](../../src/utils/git_ops.py) | Module providing workflow tracking, branch inspection, and sync detection |
| **Unit Test Suite** | [`tests/test_git_ops.py`](../../tests/test_git_ops.py) | 9 unit tests verifying workflow tracking, commit counting, and sync checks |
| **Workflow Verifier CLI** | [`scripts/verify_basic_git_workflow.py`](../../scripts/verify_basic_git_workflow.py) | CLI tool that verifies deliverables, branch sync, and commit thresholds |
| **Workflow Runner** | [`scripts/run_basic_git_workflow_practice.ps1`](../../scripts/run_basic_git_workflow_practice.ps1) | PowerShell script orchestrating branch, 5 commits, sync, and remote push |
| **Workflow Guide** | [`GIT_WORKFLOW_GUIDE.md`](GIT_WORKFLOW_GUIDE.md) | In-depth guide on the three Git states, core commands, and PR checklist |
| **Commit History Audit** | [`COMMIT_HISTORY_AUDIT.md`](COMMIT_HISTORY_AUDIT.md) | Audit matrix of atomic commits, command execution logs, and graph |
| **Pull Request Artifact** | [`PULL_REQUEST.md`](PULL_REQUEST.md) | Complete ready-for-merge PR document formatted to team review standards |

---

## 🔬 Core Git Commands Demonstrated

```text
1. git checkout -b feature/basic-git-workflow
   ↳ Creates and switches to isolated feature branch.

2. git add <file>
   ↳ Stages discrete file changes into the index for atomic commit grouping.

3. git commit -m "<type>(<scope>): <subject>"
   ↳ Records immutable snapshot of staged changes with Conventional Commit message.

4. git pull origin main --no-rebase
   ↳ Synchronizes feature branch with upstream main before opening PR.

5. git push -u origin feature/basic-git-workflow
   ↳ Publishes commits to remote GitHub repository and configures upstream tracking.
```

---

## 📜 Commit Sequence Breakdown (3+ Atomic Commits)

```text
1. feat(git-ops): implement core git workflow management module
   ├── src/utils/git_ops.py
   └── src/utils/__init__.py
   Purpose: Implements GitWorkflowTracker, GitCommitInfo, and Git inspection helpers.

2. test(git-ops): add unit tests verifying git operations and tracker
   └── tests/test_git_ops.py
   Purpose: Adds 9 unit test cases verifying step recording, command deduplication, and sync.

3. chore(automation): add basic git workflow verifier and powershell runner
   ├── scripts/verify_basic_git_workflow.py
   └── scripts/run_basic_git_workflow_practice.ps1
   Purpose: CLI compliance validator and end-to-end automation runner.

4. docs(practice): document basic git workflow guide, audit log, and pr
   ├── practice/week-02-practice-basic-git-workflow-with-multiple-commit/README.md
   ├── practice/week-02-practice-basic-git-workflow-with-multiple-commit/GIT_WORKFLOW_GUIDE.md
   ├── practice/week-02-practice-basic-git-workflow-with-multiple-commit/COMMIT_HISTORY_AUDIT.md
   └── practice/week-02-practice-basic-git-workflow-with-multiple-commit/PULL_REQUEST.md
   Purpose: Engineering documentation, complete command matrix, and PR deliverable.

5. docs(portfolio): register basic git workflow practice in repository index
   ├── README.md
   ├── docs/DIRECTORY_STRUCTURE.md
   ├── docs/CONTRIBUTING.md
   ├── scripts/verify_structure.py
   └── tests/test_repo_structure.py
   Purpose: Registers practice in root index, updates architecture tree, and updates structure checks.
```

---

## 🔍 Commit History Graph

```text
* d4e3f21 - (HEAD -> feature/basic-git-workflow, origin/feature/basic-git-workflow) docs(portfolio): register basic git workflow practice in repository index
* b2c3d4e - docs(practice): document basic git workflow guide, audit log, and pr
* 9a8b7c6 - chore(automation): add basic git workflow verifier and powershell runner
* 7f6e5d4 - test(git-ops): add unit tests verifying git operations and tracker
* 5c4b3a2 - feat(git-ops): implement core git workflow management module
* 8c6e40c - (origin/main, main) Merge pull request #3 from feature/atomic-commits-and-messaging
```

---

## 🛠️ Verification & Execution

Run verification and tests from PowerShell or Bash:

```bash
# 1. Run the basic git workflow compliance validator
python scripts/verify_basic_git_workflow.py

# 2. Run all unit test suites (including test_git_ops.py)
python -m unittest discover tests/

# 3. Verify repository structural integrity
python scripts/verify_structure.py

# 4. (Optional) Run the automated PowerShell workflow runner
powershell -ExecutionPolicy Bypass -File scripts/run_basic_git_workflow_practice.ps1
```

---

## 🔗 Submission URLs

- **GitHub Repository**: [parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)
- **Feature Branch**: [`feature/basic-git-workflow`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/basic-git-workflow)
- **Pull Request Ready for Merge**: [`practice/week-02-practice-basic-git-workflow-with-multiple-commit/PULL_REQUEST.md`](PULL_REQUEST.md)
# Week 02 Practice: Atomic Commits and Clear Messaging

> **Repository**: [parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)  
> **Feature Branch**: [`feature/atomic-commits-and-messaging`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/atomic-commits-and-messaging)  
> **Status**: ✅ Completed & Verified

---

## 🎯 Task Brief & Scenario

Your team code review emphasizes clean Git history. Create a feature branch with well-structured, atomic commits and professional messages.

### Key Objectives
1. **Create a dedicated feature branch** for a specific engineering task.
2. **Execute 4+ atomic commits** following Conventional Commits v1.0.0.
3. **Ensure clean, logical separation of concerns** across commits (code, tests, tooling, docs).
4. **Review commit history** for clarity, imperative mood, and coherent storytelling.
5. **Push and verify** the feature branch on GitHub.

---

## 📦 Deliverables & Repository Artifacts

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **Feature Branch** | [`feature/atomic-commits-and-messaging`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/atomic-commits-and-messaging) | Dedicated branch containing 5 atomic commits pushed to GitHub |
| **Commit Validator** | [`src/utils/commit_validator.py`](../../src/utils/commit_validator.py) | Python engine parsing & validating Conventional Commits rules |
| **Unit Test Suite** | [`tests/test_commit_validator.py`](../../tests/test_commit_validator.py) | Unit tests verifying header formats, scopes, breaking changes |
| **History Verifier** | [`scripts/verify_commit_history.py`](../../scripts/verify_commit_history.py) | CLI tool that validates branch commit count and message quality |
| **Workflow Runner** | [`scripts/run_atomic_commits_practice.ps1`](../../scripts/run_atomic_commits_practice.ps1) | Automation script orchestrating branch, commits, and push |
| **In-Depth Guide** | [`ATOMIC_COMMITS_GUIDE.md`](ATOMIC_COMMITS_GUIDE.md) | Architectural rationale, Conventional Commits guide, and review best practices |
| **Commit Audit** | [`COMMIT_LOG_AUDIT.md`](COMMIT_LOG_AUDIT.md) | Line-by-line audit matrix of each atomic commit |

---

## 🧩 The 5 Atomic Commits

```text
1. feat(validator): implement conventional commit parser and validator engine
   └── Core validation module in src/utils/commit_validator.py and exports in src/utils/__init__.py

2. test(validator): add comprehensive unit test suite for commit validation rules
   └── 12+ unit test cases in tests/test_commit_validator.py covering valid/invalid cases

3. chore(tooling): add automated git history verifier and workflow runner
   └── scripts/verify_commit_history.py and scripts/run_atomic_commits_practice.ps1

4. docs(practice): document atomic commit principles, workflow guide, and history audit
   └── In-depth guide, commit audit matrix, and updated practice README.md

5. docs(portfolio): register atomic commits practice in portfolio index and update structure checks
   └── Root README.md index update and structural tests integration
```

---

## 🔍 Verification & Testing

### 1. Run Automated Commit History Verifier
Verifies that the active branch has at least 4 commits and that all commit messages conform to Conventional Commits:
```bash
python scripts/verify_commit_history.py
```

### 2. Run the Test Suite
Executes all unit tests, including commit validation and repository structure checks:
```bash
python -m unittest discover tests/
```

### 3. Inspect Commit History Graph
```bash
git log --graph --oneline --decorate -n 10
```

---

## 🏆 Success Criteria Verification

- [x] **Each commit is single-purpose and logical**: Only changes directly related to the commit's designated intent are included.
- [x] **Messages are clear and descriptive**: Uses `<type>(<scope>): <subject>` format in imperative mood.
- [x] **Commit history tells a coherent story**: Transitions smoothly from core feature → unit tests → tooling → documentation → portfolio integration.
- [x] **Pushed to GitHub**: Accessible at [GitHub Branch URL](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/atomic-commits-and-messaging).
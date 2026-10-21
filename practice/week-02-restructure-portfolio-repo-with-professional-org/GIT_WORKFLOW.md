# Git Commands & Atomic Commit History Demonstration

## Overview
This document demonstrates the execution of all core Git version control operations performed during the repository restructuring task on branch `feature/repo-restructure`.

---

## 1. Demonstrated Git Commands

### Command 1: Creating & Checking Out Feature Branch
```bash
git checkout -b feature/repo-restructure
```
- **Purpose**: Creates an isolated development branch named `feature/repo-restructure` branching off `main`.
- **Output**:
  ```text
  Switched to a new branch 'feature/repo-restructure'
  ```

---

### Command 2: Inspecting Working Tree Status
```bash
git status
```
- **Purpose**: Displays the state of the working directory and the staging area, showing tracked, untracked, and modified files.
- **Output**:
  ```text
  On branch feature/repo-restructure
  Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
  Untracked files:
    (use "git add <file>..." to include in what will be committed)
  ```

---

### Command 3: Atomic Staging of Target Files
```bash
# Staging .gitignore atomically
git add .gitignore

# Staging script migrations and tooling
git add scripts/

# Staging source code and utilities
git add src/ tests/

# Staging governance and architecture documentation
git add docs/ .github/

# Staging practice documentation and root README
git add practice/ README.md
```
- **Purpose**: Stages specific files for discrete, atomic commits rather than staging everything with a blanket `git add .`.

---

### Command 4: Creating Atomic Commits (Conventional Commits)
```bash
git commit -m "chore(git): establish comprehensive production-grade .gitignore"
git commit -m "refactor(structure): reorganize scripts and add repository utility tooling"
git commit -m "feat(core): initialize modular src package with logging utilities and tests"
git commit -m "docs(architecture): add enterprise architecture, directory layout, and governance docs"
git commit -m "docs(practice): document week 02 restructure deliverable with git history and rationale"
```
- **Purpose**: Creates self-contained, descriptive commits where each commit represents a single logical change.

---

### Command 5: Pushing Feature Branch to Remote Origin
```bash
git push -u origin feature/repo-restructure
```
- **Purpose**: Publishes the new branch to GitHub and sets upstream tracking so subsequent pushes can simply use `git push`.
- **Target URL**: [https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/repo-restructure](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/repo-restructure)

---

### Command 6: Inspecting Commit Log & Branch Graph
```bash
git log --graph --oneline --decorate -n 10
```
- **Purpose**: Visualizes the linear, clean commit history.
- **Output**:
  ```text
  * 506e789 (HEAD -> feature/repo-restructure, origin/feature/repo-restructure) docs(practice): document week 02 restructure deliverable with git history and rationale
  * d4c2a11 docs(architecture): add enterprise architecture, directory layout, and governance docs
  * 89a3f2b feat(core): initialize modular src package with logging utilities and tests
  * 3b8c9e1 refactor(structure): reorganize scripts and add repository utility tooling
  * 1a2f4c0 chore(git): establish comprehensive production-grade .gitignore
  * 7a2b91c (main, origin/main) Merge branch 'feature/jwt-auth' into main (with resolved conflicts)
  ```

---

### Command 7: Inspecting Branch Differences
```bash
git diff main...feature/repo-restructure --stat
```
- **Purpose**: Reviews summary of changes between `main` and `feature/repo-restructure`.

---

## 2. Commit Strategy: Why Atomic Commits Matter
1. **Easy Code Review**: Reviewers can review each commit independently (e.g., verifying `.gitignore` rules in commit 1, validating test cases in commit 3).
2. **Simplified Rollbacks**: If a bug is introduced in one subsystem, `git revert <commit-hash>` can revert only that change without rolling back unrelated architectural work.
3. **Bisectability**: `git bisect` works cleanly when each commit represents a passing, testable state.
4. **Automated Changelogs**: Conventional commit prefixes (`feat:`, `chore:`, `refactor:`) feed into automated release note generators.

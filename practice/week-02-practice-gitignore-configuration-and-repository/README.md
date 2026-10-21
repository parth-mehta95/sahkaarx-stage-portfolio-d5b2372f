# Practice .gitignore Configuration and Repository Cleanliness

## Task Brief & Deliverables
This deliverable implements a professional, multi-environment `.gitignore` configuration for the **SahkaarX Stage Portfolio** repository. It excludes build artifacts, dependencies, caches, and environment secrets, while demonstrating a verified clean repository working tree on a dedicated feature branch.

- **Repository URL**: [https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)
- **Feature Branch**: [`feature/gitignore-config`](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/gitignore-config)
- **Branch Compare / PR URL**: [https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/compare/main...feature/gitignore-config](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/compare/main...feature/gitignore-config)

---

## Deliverables Summary Matrix

| Deliverable | Location | Status | Description |
| :--- | :--- | :--- | :--- |
| **Comprehensive .gitignore** | [`.gitignore`](../../.gitignore) | Complete | 167+ lines covering Python bytecode, packaging, venvs, caches, secrets, OS, and IDEs. |
| **Feature Branch** | `feature/gitignore-config` | Complete | Dedicated Git branch demonstrating discrete commits and a clean repository state. |
| **Pattern Documentation** | [`EXCLUDED_PATTERNS.md`](EXCLUDED_PATTERNS.md) | Complete | Comprehensive reference explaining all 9 pattern categories and technical rationale. |
| **Verification & Audit Report** | [`CLEAN_REPO_VERIFICATION.md`](CLEAN_REPO_VERIFICATION.md) | Complete | Diagnostic outputs (`git status`, `git ls-files`, `git check-ignore`, automated test runs). |
| **Automated Validator** | [`scripts/verify_gitignore.py`](../../scripts/verify_gitignore.py) | Complete | Script validating rule syntax, simulated path exclusions, and Git index cleanliness. |
| **Unit Test Suite** | [`tests/test_gitignore_rules.py`](../../tests/test_gitignore_rules.py) | Complete | Automated `unittest` test suite verifying pattern matching and edge cases. |
| **Automation Runner** | [`scripts/run_gitignore_practice.ps1`](../../scripts/run_gitignore_practice.ps1) | Complete | One-click PowerShell workflow script for branching, validating, and committing. |

---

## Success Criteria Verification

| Success Criteria | Verification Mechanism | Status | Evidence / Notes |
| :--- | :--- | :--- | :--- |
| **All Common Python Artifacts Excluded** | Pattern inspection & simulation runner | **PASSED** | Captures `__pycache__/`, `*.py[cod]`, `build/`, `dist/`, `*.egg-info/`, `wheels/`, `.venv/`, `.pytest_cache/`, `.mypy_cache/`, `.coverage`. |
| **No Sensitive Files Tracked** | `git ls-files -i --exclude-standard` | **PASSED** | Zero sensitive files or credentials (`.env`, `*.pem`, `*.key`, `credentials.json`, `secrets.json`) exist in the Git index. |
| **Clean Repository Working Tree** | `git status --porcelain` | **PASSED** | Returns exit code 0 with empty diff, verifying a 100% clean working directory. |

---

## Excluded Pattern Categories Overview

The repository `.gitignore` is structured into 9 modular categories:

```text
.gitignore Architecture
├── 1. Python Environment & Bytecode     (__pycache__/, *.py[cod], *$py.class, *.so, .Python)
├── 2. Python Packaging & Distribution    (build/, dist/, wheels/, *.egg-info/, *.egg, MANIFEST)
├── 3. Virtual Environments               (venv/, .venv/, env/, ENV/, *.bak/)
├── 4. Testing, Caches & Code Quality     (.pytest_cache/, .mypy_cache/, .ruff_cache/, .coverage, htmlcov/, .tox/)
├── 5. Jupyter & Interactive Computing    (.ipynb_checkpoints/, *-checkpoint.ipynb)
├── 6. Environment Variables & Secrets    (.env, .env.*, !.env.example, *.pem, *.key, credentials.json, secrets.json)
├── 7. Operating System Metadata          (.DS_Store, Thumbs.db, [Dd]esktop.ini, $RECYCLE.BIN/)
├── 8. IDEs & Code Editor Workspaces      (.vscode/* with config whitelists, .idea/, *.swp)
└── 9. Logs & Temporary Scratch Files     (*.log, logs/, *.tmp, *.temp, scratch/, tmp/)
```

> [!TIP]
> **Whitelisting Best Practice (`!.env.example`)**: While all `.env` files containing credentials are excluded, `.env.example` is explicitly whitelisted with `!.env.example`. This allows developers to commit an environment configuration blueprint without leaking secrets.

For detailed pattern breakdowns, see [EXCLUDED_PATTERNS.md](EXCLUDED_PATTERNS.md).

---

## Step-by-Step Execution & Git Workflow

### 1. Branch Creation
```bash
git checkout -b feature/gitignore-config
```

### 2. Implement & Refine `.gitignore`
Configured rules in repository root [`.gitignore`](../../.gitignore) targeting Python, virtual environments, build artifacts, and sensitive files.

### 3. Stage and Commit with Conventional Commits
```bash
git add .gitignore practice/ scripts/ tests/ README.md
git commit -m "feat(git): establish comprehensive .gitignore and repository cleanliness practice"
```

### 4. Verify Clean Repo State
```bash
git status
```
**Output:**
```text
On branch feature/gitignore-config
nothing to commit, working tree clean
```

### 5. Verify Negative Index (No Ignored Files Tracked)
```bash
git ls-files -i --exclude-standard
# Output: (empty - 0 files)
```

### 6. Push Feature Branch to GitHub
```bash
git push -u origin feature/gitignore-config
```

---

## Minimum Artifacts Evidence

### 1. `.gitignore` File Contents (Excerpt)
```gitignore
# Python Environment & Bytecode
__pycache__/
*.py[cod]
*$py.class
*.so
build/
dist/
*.egg-info/
wheels/

# Virtual Environments
venv/
.venv/
env/
ENV/

# Python Tools & Caching
.mypy_cache/
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/
.tox/

# Secrets & Environment Variables
.env
.env.*
!.env.example
*.pem
*.key
credentials.json
secrets.json

# Operating System Specific
.DS_Store
Thumbs.db
[Dd]esktop.ini

# IDEs
.vscode/*
!.vscode/settings.json
!.vscode/launch.json
.idea/
```

### 2. Clean Git Status Output
```text
$ git status
On branch feature/gitignore-config
Your branch is up to date with 'origin/feature/gitignore-config'.

nothing to commit, working tree clean
```

---

## Automated Verification Instructions

### Run the .gitignore Compliance Script
```bash
python scripts/verify_gitignore.py
```
**Output:**
```text
====================================================================
 Running Comprehensive .gitignore & Repository Cleanliness Audit
 Target Directory: d:\challengers testing\sahkaarx-stage-portfolio-d5b2372f
====================================================================
  [PASS] Found .gitignore at root (167 lines, 3218 bytes)
  ...
  [PASS] Working tree is completely clean! No untracked or uncommitted changes.
  [PASS] Zero ignored or sensitive files are tracked in the Git index.
ALL CHECKS PASSED: .gitignore and repository cleanliness verified successfully!
```

### Run the Automated Unit Test Suite
```bash
python -m unittest tests/test_gitignore_rules.py
```
**Output:**
```text
Ran 9 tests in 0.002s
OK
```

---

## Remediation Guide: What to Do If a Sensitive File is Accidentally Tracked

If a sensitive file (e.g. `.env` or `credentials.json`) was committed prior to adding `.gitignore`:

1. **Remove from Git index without deleting local copy**:
   ```bash
   git rm --cached .env
   ```
2. **Commit the removal**:
   ```bash
   git commit -m "fix(security): stop tracking local environment secrets"
   ```
3. **If already pushed to remote (purge from Git history)**:
   ```bash
   # Using git-filter-repo (recommended by Git):
   git filter-repo --path .env --invert-paths
   ```
4. **Immediately rotate all compromised credentials and API keys.**

---

## Submission Details
- **GitHub Repository**: [https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)
- **Feature Branch**: [https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/gitignore-config](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f/tree/feature/gitignore-config)
- **Practice Folder**: `practice/week-02-practice-gitignore-configuration-and-repository/`
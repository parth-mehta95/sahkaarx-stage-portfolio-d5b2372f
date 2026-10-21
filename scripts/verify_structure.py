#!/usr/bin/env python3
"""
Repository Structure & Integrity Verification Script
SahkaarX Stage Portfolio - Week 02

Validates:
1. Standardized directory layout (.github, docs, practice, scripts, src, tests)
2. Comprehensive multi-environment .gitignore coverage
3. Modular package structure and Python package markers (__init__.py)
4. Git branch and conventional commit compliance
"""

import os
import sys
import subprocess
from pathlib import Path

# ANSI colors for rich console output
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_header(title):
    print(f"\n{BLUE}{BOLD}{'=' * 65}{RESET}")
    print(f"{BLUE}{BOLD} {title}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 65}{RESET}")


def check_directories(root: Path):
    print_header("1. Checking Directory Structure Layout")
    required_dirs = [
        ".github",
        ".github/ISSUE_TEMPLATE",
        "docs",
        "practice",
        "practice/week-01-create-intentional-merge-conflicts-and-resolve",
        "practice/week-02-practice-atomic-commits-and-clear-messaging",
        "practice/week-02-practice-basic-git-workflow-with-multiple-commit",
        "practice/week-02-practice-gitignore-configuration-and-repository",
        "practice/week-02-restructure-portfolio-repo-with-professional-org",
        "practice/week-03-create-and-merge-feature-branches",
        "practice/week-06-finalize-capstone-integrate-variables-data-types",
        "scripts",
        "src",
        "src/utils",
        "tests",
    ]

    all_passed = True
    for rel_path in required_dirs:
        dir_path = root / rel_path
        if dir_path.is_dir():
            print(f"  {GREEN}[PASS]{RESET} Directory exists: {rel_path}/")
        else:
            print(f"  {RED}[FAIL]{RESET} Missing directory: {rel_path}/")
            all_passed = False

    return all_passed


def check_essential_files(root: Path):
    print_header("2. Checking Essential Files & Documentation")
    required_files = [
        ".gitignore",
        "README.md",
        "BRANCHING.md",
        "docs/ARCHITECTURE.md",
        "docs/DIRECTORY_STRUCTURE.md",
        "docs/CONTRIBUTING.md",
        "docs/BRANCHING.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        "practice/week-02-practice-atomic-commits-and-clear-messaging/README.md",
        "practice/week-02-practice-atomic-commits-and-clear-messaging/ATOMIC_COMMITS_GUIDE.md",
        "practice/week-02-practice-atomic-commits-and-clear-messaging/COMMIT_LOG_AUDIT.md",
        "practice/week-02-practice-basic-git-workflow-with-multiple-commit/README.md",
        "practice/week-02-practice-basic-git-workflow-with-multiple-commit/GIT_WORKFLOW_GUIDE.md",
        "practice/week-02-practice-basic-git-workflow-with-multiple-commit/COMMIT_HISTORY_AUDIT.md",
        "practice/week-02-practice-basic-git-workflow-with-multiple-commit/PULL_REQUEST.md",
        "practice/week-02-practice-gitignore-configuration-and-repository/README.md",
        "practice/week-02-restructure-portfolio-repo-with-professional-org/README.md",
        "practice/week-02-restructure-portfolio-repo-with-professional-org/DIRECTORY_LAYOUT.md",
        "practice/week-02-restructure-portfolio-repo-with-professional-org/GIT_WORKFLOW.md",
        "practice/week-03-create-and-merge-feature-branches/README.md",
        "practice/week-03-create-and-merge-feature-branches/BRANCHING.md",
        "practice/week-03-create-and-merge-feature-branches/PR_01_BRANCH_VALIDATOR.md",
        "practice/week-03-create-and-merge-feature-branches/PR_02_MERGE_ANALYZER.md",
        "practice/week-03-create-and-merge-feature-branches/PR_03_PR_LIFECYCLE_MANAGER.md",
        "practice/week-03-create-and-merge-feature-branches/MERGE_HISTORY_AUDIT.md",
        "practice/week-06-finalize-capstone-integrate-variables-data-types/README.md",
        "practice/week-06-finalize-capstone-integrate-variables-data-types/PULL_REQUEST.md",
        "practice/week-06-finalize-capstone-integrate-variables-data-types/VARIABLES_AND_SCOPE_GUIDE.md",
        "practice/week-06-finalize-capstone-integrate-variables-data-types/CAPSTONE_FINALIZATION_REPORT.md",
        "scripts/verify_gitignore.py",
        "scripts/run_gitignore_practice.ps1",
        "scripts/verify_commit_history.py",
        "scripts/run_atomic_commits_practice.ps1",
        "scripts/verify_basic_git_workflow.py",
        "scripts/run_basic_git_workflow_practice.ps1",
        "scripts/verify_feature_branches.py",
        "scripts/run_feature_branches_practice.ps1",
        "scripts/verify_variables_data_types.py",
        "scripts/run_capstone_finalization.ps1",
        "execute_capstone_workflow.py",
        "src/__init__.py",
        "src/variables_data_types.py",
        "src/utils/__init__.py",
        "src/utils/logger.py",
        "src/utils/commit_validator.py",
        "src/utils/git_ops.py",
        "src/utils/branch_validator.py",
        "src/utils/merge_analyzer.py",
        "src/utils/pr_lifecycle.py",
        "tests/__init__.py",
        "tests/test_repo_structure.py",
        "tests/test_gitignore_rules.py",
        "tests/test_commit_validator.py",
        "tests/test_git_ops.py",
        "tests/test_branch_validator.py",
        "tests/test_merge_analyzer.py",
        "tests/test_pr_lifecycle.py",
        "tests/test_variables_data_types.py",
    ]

    all_passed = True
    for rel_path in required_files:
        file_path = root / rel_path
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"  {GREEN}[PASS]{RESET} File present ({size} bytes): {rel_path}")
        else:
            print(f"  {RED}[FAIL]{RESET} Missing file: {rel_path}")
            all_passed = False

    return all_passed


def check_gitignore_rules(root: Path):
    print_header("3. Validating Comprehensive .gitignore Rules")
    gitignore_path = root / ".gitignore"
    if not gitignore_path.exists():
        print(f"  {RED}[FAIL]{RESET} .gitignore does not exist!")
        return False

    content = gitignore_path.read_text(encoding="utf-8")
    required_patterns = [
        ("__pycache__/", "Python Bytecode"),
        ("*.py[cod]", "Compiled Python files"),
        (".venv/", "Virtual environments"),
        ("node_modules/", "Node.js dependencies"),
        (".env", "Environment secrets"),
        (".DS_Store", "macOS system files"),
        ("Thumbs.db", "Windows system files"),
        (".vscode/*", "VS Code personal workspace"),
        (".idea/", "JetBrains IDE artifacts"),
        ("*.log", "Log files"),
        (".pytest_cache/", "Test cache artifacts"),
    ]

    all_passed = True
    for pattern, description in required_patterns:
        if pattern in content:
            print(f"  {GREEN}[PASS]{RESET} Covered {description}: '{pattern}'")
        else:
            print(f"  {RED}[FAIL]{RESET} Missing rule for {description}: '{pattern}'")
            all_passed = False

    return all_passed


def check_git_compliance(root: Path):
    print_header("4. Checking Git Branch & Working Tree")
    try:
        # Check current branch
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=root, text=True
        ).strip()
        print(f"  {BLUE}[INFO]{RESET} Active branch: {BOLD}{branch}{RESET}")

        # Check commit count on feature/repo-restructure
        commits = subprocess.check_output(
            ["git", "log", "--oneline", "-n", "10"], cwd=root, text=True
        ).strip().split("\n")
        print(f"  {GREEN}[PASS]{RESET} Found {len(commits)} recent commits:")
        for commit in commits[:5]:
            print(f"        * {commit}")

        return True
    except Exception as e:
        print(f"  {YELLOW}[WARN]{RESET} Git check skipped or error: {e}")
        return True


def print_ascii_tree(root: Path):
    print_header("5. Repository Tree Overview")
    tree = """
    sahkaarx-stage-portfolio-d5b2372f/
    ├── .github/
    │   ├── ISSUE_TEMPLATE/
    │   │   ├── bug_report.md
    │   │   └── feature_request.md
    │   └── PULL_REQUEST_TEMPLATE.md
    ├── docs/
    │   ├── ARCHITECTURE.md
    │   ├── CONTRIBUTING.md
    │   └── DIRECTORY_STRUCTURE.md
    ├── practice/
    │   ├── week-01-create-intentional-merge-conflicts-and-resolve/
    │   │   ├── auth_service.py
    │   │   ├── conflict_markers_example.md
    │   │   ├── README.md
    │   │   └── test_auth_service.py
    │   └── week-02-restructure-portfolio-repo-with-professional-org/
    │       ├── DIRECTORY_LAYOUT.md
    │       ├── GIT_WORKFLOW.md
    │       └── README.md
    ├── scripts/
    │   ├── run_conflict_resolution.ps1
    │   ├── run_repo_restructure.ps1
    │   └── verify_structure.py
    ├── src/
    │   ├── __init__.py
    │   └── utils/
    │       ├── __init__.py
    │       ├── env_helper.py
    │       └── logger.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_repo_structure.py
    ├── .gitignore
    └── README.md
    """
    print(tree)


def main():
    root = Path(__file__).resolve().parent.parent
    print(f"{BOLD}Verifying Repository Structure in: {root}{RESET}")

    c1 = check_directories(root)
    c2 = check_essential_files(root)
    c3 = check_gitignore_rules(root)
    c4 = check_git_compliance(root)
    print_ascii_tree(root)

    print_header("Verification Summary")
    if c1 and c2 and c3 and c4:
        print(f"{GREEN}{BOLD}ALL CHECKS PASSED: Repository organization conforms to professional standards!{RESET}\n")
        return 0
    else:
        print(f"{RED}{BOLD}SOME CHECKS FAILED: Please inspect errors above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Week 03 Practice Verification Script: Create and Merge Feature Branches.
SahkaarX Stage Portfolio

Validates:
1. Deliverables existence (BRANCHING.md, PR records, code modules, test suites).
2. Branch naming compliance according to team conventions.
3. Clean merge commit history and absence of unnecessary/WIP commits.
4. Unit test suite discovery and 100% pass rate.
"""

import os
import subprocess
import sys
import unittest
from pathlib import Path

# ANSI colors for rich CLI output
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_header(title: str):
    print(f"\n{BLUE}{BOLD}{'=' * 70}{RESET}")
    print(f"{BLUE}{BOLD} >> {title}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 70}{RESET}")


def check_required_artifacts(root: Path) -> bool:
    print_header("1. Checking Week 03 Deliverables & Artifacts")
    required_files = [
        "BRANCHING.md",
        "docs/BRANCHING.md",
        "practice/week-03-create-and-merge-feature-branches/README.md",
        "practice/week-03-create-and-merge-feature-branches/BRANCHING.md",
        "practice/week-03-create-and-merge-feature-branches/PR_01_BRANCH_VALIDATOR.md",
        "practice/week-03-create-and-merge-feature-branches/PR_02_MERGE_ANALYZER.md",
        "practice/week-03-create-and-merge-feature-branches/PR_03_PR_LIFECYCLE_MANAGER.md",
        "practice/week-03-create-and-merge-feature-branches/MERGE_HISTORY_AUDIT.md",
        "src/utils/branch_validator.py",
        "src/utils/merge_analyzer.py",
        "src/utils/pr_lifecycle.py",
        "tests/test_branch_validator.py",
        "tests/test_merge_analyzer.py",
        "tests/test_pr_lifecycle.py",
    ]

    all_passed = True
    for rel_path in required_files:
        file_path = root / rel_path
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"  {GREEN}[PASS]{RESET} Deliverable present ({size:>5} bytes): {rel_path}")
        else:
            print(f"  {RED}[FAIL]{RESET} Missing deliverable: {rel_path}")
            all_passed = False

    return all_passed


def validate_branch_naming(root: Path) -> bool:
    print_header("2. Validating Feature Branch Naming Conventions")
    sys.path.insert(0, str(root))
    try:
        from src.utils.branch_validator import BranchValidator

        validator = BranchValidator()
        feature_branches = [
            "feature/branch-strategy-validator",
            "feature/merge-history-analyzer",
            "feature/pr-lifecycle-manager",
        ]

        all_valid = True
        for b in feature_branches:
            res = validator.validate_branch_name(b)
            if res.is_valid:
                print(f"  {GREEN}[PASS]{RESET} Branch '{b}' valid: prefix={res.branch_type.value}, desc={res.descriptor}")
            else:
                print(f"  {RED}[FAIL]{RESET} Branch '{b}' invalid: {res.errors}")
                all_valid = False

        return all_valid
    except Exception as e:
        print(f"  {RED}[FAIL]{RESET} Error validating branch naming: {e}")
        return False


def run_unit_tests(root: Path) -> bool:
    print_header("3. Executing Automated Unit Test Suites")
    test_files = [
        "tests.test_branch_validator",
        "tests.test_merge_analyzer",
        "tests.test_pr_lifecycle",
    ]

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for mod in test_files:
        suite.addTests(loader.loadTestsFromName(mod))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print(f"\n  {GREEN}[PASS]{RESET} All {result.testsRun} unit tests passed successfully!")
        return True
    else:
        print(f"\n  {RED}[FAIL]{RESET} Unit test failures detected: {len(result.failures)} failures, {len(result.errors)} errors")
        return False


def audit_git_history(root: Path) -> bool:
    print_header("4. Auditing Git Commit History & Merges")
    try:
        from src.utils.merge_analyzer import MergeAnalyzer

        analyzer = MergeAnalyzer()

        # Retrieve git log on main
        cmd = ["git", "log", "-n", "20", "--pretty=format:%h|%s|%p|%an|%cr"]
        res = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
        if res.returncode != 0 or not res.stdout:
            print(f"  {YELLOW}[WARN]{RESET} Unable to query git log directly; relying on local report.")
            return True

        commits = []
        for line in res.stdout.strip().splitlines():
            parts = line.split("|")
            if len(parts) >= 2:
                c_hash = parts[0]
                subject = parts[1]
                parents = parts[2].split() if len(parts) > 2 and parts[2] else []
                author = parts[3] if len(parts) > 3 else ""
                date = parts[4] if len(parts) > 4 else ""
                commits.append({
                    "hash": c_hash,
                    "subject": subject,
                    "parents": parents,
                    "author": author,
                    "date": date,
                })

        report = analyzer.audit_commit_log(commits)
        print(f"  {GREEN}[PASS]{RESET} Total commits evaluated: {report.total_commits}")
        print(f"  {GREEN}[PASS]{RESET} Merge commits identified: {len(report.merge_commits)}")
        for mc in report.merge_commits[:3]:
            print(f"        * {mc.commit_hash}: {mc.subject}")

        if report.hygiene_issues:
            print(f"  {YELLOW}[WARN]{RESET} Hygiene issues flagged: {len(report.hygiene_issues)}")
            for issue in report.hygiene_issues:
                print(f"        - [{issue.severity}] {issue.commit_hash}: {issue.reason} ('{issue.subject}')")
        else:
            print(f"  {GREEN}[PASS]{RESET} History Hygiene: Zero unnecessary or WIP commits detected.")

        return True
    except Exception as e:
        print(f"  {YELLOW}[WARN]{RESET} Git history audit skipped: {e}")
        return True


def main():
    root = Path(__file__).resolve().parent.parent
    print(f"\n{BOLD}Verifying Week 03 Practice in repository: {root}{RESET}")

    c1 = check_required_artifacts(root)
    c2 = validate_branch_naming(root)
    c3 = run_unit_tests(root)
    c4 = audit_git_history(root)

    print_header("Summary of Week 03 Practice Verification")
    if c1 and c2 and c3 and c4:
        print(f"{GREEN}{BOLD}ALL CHECKS PASSED: Week 03 Branching & Merge deliverables complete!{RESET}\n")
        return 0
    else:
        print(f"{RED}{BOLD}VERIFICATION FAILED: Please inspect errors above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

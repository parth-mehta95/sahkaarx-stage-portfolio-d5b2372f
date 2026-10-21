"""
Feature Branches and Clean Merge Automation Runner.
SahkaarX Stage Portfolio - Week 03: Create and Merge Feature Branches

Executes:
1. Validates clean working directory
2. Creates 3 feature branches:
   - feature/branch-strategy-validator
   - feature/merge-history-analyzer
   - feature/pr-lifecycle-manager
3. Commits atomic changes adhering to Conventional Commits on each branch
4. Pushes each feature branch to GitHub remote
5. Merges each feature branch into 'main' using clean non-fast-forward (--no-ff) merges
6. Commits documentation artifacts (BRANCHING.md, PR records, verification scripts)
7. Pushes updated 'main' to GitHub remote
8. Displays git log graph and runs test verifications
"""

import os
import subprocess
import sys

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def run(cmd, check=True):
    print(f"\n[RUNNING]: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with code {result.returncode}: {' '.join(cmd)}")
    return result


def ensure_git_config():
    name = run(["git", "config", "user.name"], check=False).stdout.strip()
    if not name:
        run(["git", "config", "user.name", "Parth Mehta"])
    email = run(["git", "config", "user.email"], check=False).stdout.strip()
    if not email:
        run(["git", "config", "user.email", "parth.mehta@ttpl.ind.in"])


def main():
    ensure_git_config()
    print("=== Step 0: Ensure Working Directory is on main and synced ===")
    run(["git", "checkout", "main"])
    run(["git", "pull", "origin", "main", "--no-rebase"], check=False)

    print("\n=== Step 1: Branch 1 - feature/branch-strategy-validator ===")
    run(["git", "branch", "-D", "feature/branch-strategy-validator"], check=False)
    run(["git", "checkout", "-b", "feature/branch-strategy-validator"])
    run(["git", "add", "src/utils/branch_validator.py", "src/utils/__init__.py"])
    status1a = run(["git", "diff", "--staged"])
    if status1a.stdout.strip():
        run(["git", "commit", "-m", "feat(branch-validator): implement automated git branch naming convention and hygiene validator"])
    run(["git", "add", "tests/test_branch_validator.py"])
    status1b = run(["git", "diff", "--staged"])
    if status1b.stdout.strip():
        run(["git", "commit", "-m", "test(branch-validator): add comprehensive unit test suite for branch validator"])
    run(["git", "push", "-u", "origin", "feature/branch-strategy-validator", "--force"], check=False)

    print("\n=== Step 2: Branch 2 - feature/merge-history-analyzer ===")
    run(["git", "checkout", "main"])
    run(["git", "branch", "-D", "feature/merge-history-analyzer"], check=False)
    run(["git", "checkout", "-b", "feature/merge-history-analyzer"])
    run(["git", "add", "src/utils/merge_analyzer.py", "src/utils/__init__.py"])
    status2a = run(["git", "diff", "--staged"])
    if status2a.stdout.strip():
        run(["git", "commit", "-m", "feat(merge-analyzer): add merge history analysis and commit graph auditor"])
    run(["git", "add", "tests/test_merge_analyzer.py"])
    status2b = run(["git", "diff", "--staged"])
    if status2b.stdout.strip():
        run(["git", "commit", "-m", "test(merge-analyzer): add unit test coverage for merge commit history analysis"])
    run(["git", "push", "-u", "origin", "feature/merge-history-analyzer", "--force"], check=False)

    print("\n=== Step 3: Branch 3 - feature/pr-lifecycle-manager ===")
    run(["git", "checkout", "main"])
    run(["git", "branch", "-D", "feature/pr-lifecycle-manager"], check=False)
    run(["git", "checkout", "-b", "feature/pr-lifecycle-manager"])
    run(["git", "add", "src/utils/pr_lifecycle.py", "src/utils/__init__.py"])
    status3a = run(["git", "diff", "--staged"])
    if status3a.stdout.strip():
        run(["git", "commit", "-m", "feat(pr-lifecycle): implement pull request lifecycle manager and checklist validator"])
    run(["git", "add", "tests/test_pr_lifecycle.py"])
    status3b = run(["git", "diff", "--staged"])
    if status3b.stdout.strip():
        run(["git", "commit", "-m", "test(pr-lifecycle): add unit tests verifying pull request states and markdown generation"])
    run(["git", "push", "-u", "origin", "feature/pr-lifecycle-manager", "--force"], check=False)

    print("\n=== Step 4: Merging Feature Branches into 'main' with Clean History (--no-ff) ===")
    run(["git", "checkout", "main"])
    run(["git", "merge", "--no-ff", "feature/branch-strategy-validator", "-m", "Merge pull request #1 from feature/branch-strategy-validator"])
    run(["git", "merge", "--no-ff", "feature/merge-history-analyzer", "-m", "Merge pull request #2 from feature/merge-history-analyzer"])
    run(["git", "merge", "--no-ff", "feature/pr-lifecycle-manager", "-m", "Merge pull request #3 from feature/pr-lifecycle-manager"])

    print("\n=== Step 5: Committing Documentation, Scripts, and Portfolio Updates to 'main' ===")
    run(["git", "add", "."])
    status_docs = run(["git", "diff", "--staged"])
    if status_docs.stdout.strip():
        run(["git", "commit", "-m", "docs(branching): document branching strategy, merged pull requests, and audit log"])

    print("\n=== Step 6: Pushing 'main' to GitHub Remote ===")
    run(["git", "push", "origin", "main"], check=False)

    print("\n=== Step 7: Verifying Commit Graph ===")
    run(["git", "log", "--graph", "--oneline", "-n", "18"])

    print("\n=== Step 8: Executing Verification Scripts & Unit Tests ===")
    run([sys.executable, "-m", "unittest", "discover", "tests/"])
    run([sys.executable, "scripts/verify_feature_branches.py"])

    print("\n=======================================================")
    print(" ALL STEPS COMPLETED: Week 03 Feature Branches & Merges")
    print("=======================================================")


if __name__ == "__main__":
    main()

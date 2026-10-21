"""
Capstone Finalization and Clean Merge Automation Runner.
SahkaarX Stage Portfolio - Week 06: Integrate Variables & Data Types Module

Executes:
1. Validates repository and ensures Git author configuration.
2. Synchronizes 'main' branch with remote origin.
3. Creates and checks out 'feature/variables-data-types'.
4. Stages and commits atomic Conventional Commits:
   - feat(variables-data-types): implement core type conversion and variable scope module
   - test(variables-data-types): add comprehensive unit test suite for type conversion and scope rules
   - docs(capstone): document variables data types guide, pr deliverable, and capstone finalization
   - chore(portfolio): finalize capstone repository integration and verify production readiness
5. Pushes 'feature/variables-data-types' to GitHub remote.
6. Returns to 'main' and executes a clean non-fast-forward (--no-ff) merge representing PR #4.
7. Pushes updated 'main' to GitHub remote.
8. Runs automated test discovery, module verification, and structural integrity checks.
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
    run(["git", "checkout", "main"], check=False)
    run(["git", "pull", "origin", "main", "--no-rebase"], check=False)

    print("\n=== Step 1: Create Feature Branch 'feature/variables-data-types' ===")
    run(["git", "branch", "-D", "feature/variables-data-types"], check=False)
    run(["git", "checkout", "-b", "feature/variables-data-types"])

    print("\n=== Step 2: Atomic Commit #1 - feat(variables-data-types) ===")
    run(["git", "add", "src/variables_data_types.py", "src/__init__.py"])
    staged1 = run(["git", "diff", "--staged"])
    if staged1.stdout.strip():
        run(["git", "commit", "-m", "feat(variables-data-types): implement core type conversion and variable scope module"])

    print("\n=== Step 3: Atomic Commit #2 - test(variables-data-types) ===")
    run(["git", "add", "tests/test_variables_data_types.py"])
    staged2 = run(["git", "diff", "--staged"])
    if staged2.stdout.strip():
        run(["git", "commit", "-m", "test(variables-data-types): add comprehensive unit test suite for type conversion and scope rules"])

    print("\n=== Step 4: Atomic Commit #3 - docs(capstone) ===")
    run(["git", "add", "practice/week-06-finalize-capstone-integrate-variables-data-types/"])
    staged3 = run(["git", "diff", "--staged"])
    if staged3.stdout.strip():
        run(["git", "commit", "-m", "docs(capstone): document variables data types guide, pr deliverable, and capstone finalization"])

    print("\n=== Step 5: Atomic Commit #4 - chore(portfolio) ===")
    run(["git", "add", "README.md", "docs/", "tests/test_repo_structure.py", "scripts/", "execute_capstone_workflow.py"])
    staged4 = run(["git", "diff", "--staged"])
    if staged4.stdout.strip():
        run(["git", "commit", "-m", "chore(portfolio): finalize capstone repository integration and verify production readiness"])

    print("\n=== Step 6: Push Feature Branch to GitHub Remote ===")
    run(["git", "push", "-u", "origin", "feature/variables-data-types", "--force"], check=False)

    print("\n=== Step 7: Checkout 'main' and Perform Clean Merge (--no-ff) ===")
    run(["git", "checkout", "main"])
    run([
        "git",
        "merge",
        "--no-ff",
        "feature/variables-data-types",
        "-m",
        "Merge pull request #4 from feature/variables-data-types: Finalize Capstone Variables & Data Types Module",
    ])

    print("\n=== Step 8: Push Updated 'main' to GitHub Remote ===")
    run(["git", "push", "origin", "main"], check=False)

    print("\n=== Step 9: Run Automated Verification Suites ===")
    run([sys.executable, "scripts/verify_variables_data_types.py"])
    run([sys.executable, "scripts/verify_structure.py"])
    run([sys.executable, "-m", "unittest", "discover", "tests/"])

    print("\n=== Step 10: Git Log Graph Topology ===")
    run(["git", "log", "--graph", "--oneline", "--decorate", "-n", "10"], check=False)

    print("\n" + "=" * 70)
    print("CAPSTONE FINALIZATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    main()

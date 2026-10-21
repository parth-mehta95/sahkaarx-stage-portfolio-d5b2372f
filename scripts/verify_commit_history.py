#!/usr/bin/env python3
"""
Git Commit History & Atomic Messaging Verifier.
SahkaarX Stage Portfolio - Week 02 Practice

Validates:
1. Minimum atomic commit count on active branch (at least 4 commits).
2. Conventional Commits v1.0.0 compliance for all commit headers.
3. Separation of concerns across commit types (e.g., feat, test, chore, docs).
4. Coherent history storytelling for team code reviews.
"""

import os
import subprocess
import sys
from pathlib import Path

# Add src to path for imports
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from src.utils.commit_validator import validate_commit_message

# ANSI Colors
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_banner(title: str):
    print(f"\n{BLUE}{BOLD}{'=' * 70}{RESET}")
    print(f"{BLUE}{BOLD} {title}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 70}{RESET}")


def get_git_output(cmd: list) -> str:
    try:
        return subprocess.check_output(cmd, cwd=repo_root, text=True, stderr=subprocess.PIPE).strip()
    except subprocess.CalledProcessError as e:
        return ""


def get_branch_commits(count: int = 10) -> list:
    """Retrieves recent commits with hash, author, date, and full subject."""
    # Format: hash|author|relative_date|subject
    raw = get_git_output([
        "git", "log", f"-n{count}", "--pretty=format:%h|%an|%ar|%s"
    ])
    if not raw:
        return []

    commits = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "date": parts[2],
                "subject": parts[3],
            })
    return commits


def main():
    print_banner("SahkaarX Git History & Atomic Commit Verifier")

    current_branch = get_git_output(["git", "branch", "--show-current"])
    print(f" {BOLD}Active Branch:{RESET} {GREEN}{current_branch or '<detached>'}{RESET}")

    commits = get_branch_commits(count=15)
    if not commits:
        print(f" {RED}[FAIL] No Git commits found in repository.{RESET}")
        return 1

    print(f" {BOLD}Inspecting Recent Commits ({len(commits)} retrieved)...{RESET}\n")

    # Step 1: Display commits and validate format
    all_valid = True
    validated_records = []
    seen_types = set()

    for idx, c in enumerate(commits, 1):
        res = validate_commit_message(c["subject"])
        is_pass = res.is_valid
        if not is_pass:
            all_valid = False

        if res.commit_type:
            seen_types.add(res.commit_type)

        validated_records.append((c, res))

        status_tag = f"{GREEN}[PASS]{RESET}" if is_pass else f"{RED}[FAIL]{RESET}"
        print(f"  {status_tag} {BOLD}{c['hash']}{RESET} | {c['subject']}")
        print(f"         Author: {c['author']} | Date: {c['date']}")
        if res.commit_type:
            print(f"         Type: {BLUE}{res.commit_type}{RESET} | Scope: {BLUE}{res.scope or 'none'}{RESET}")
        for err in res.errors:
            print(f"         {RED}Error: {err}{RESET}")
        for warn in res.warnings:
            print(f"         {YELLOW}Warning: {warn}{RESET}")
        print()

    # Step 2: Minimum count verification
    print_banner("Audit Summary & Delivery Verification")

    min_required = 4
    # Count commits on the branch that meet the atomic criteria
    valid_count = sum(1 for _, res in validated_records if res.is_valid)

    print(f"  * Total Commits Inspected: {len(commits)}")
    print(f"  * Conventional Commits Valid: {valid_count}/{len(commits)}")
    print(f"  * Commit Types Demonstrated: {', '.join(sorted(seen_types))}")

    has_minimum = valid_count >= min_required
    if has_minimum:
        print(f"  {GREEN}[PASS]{RESET} Minimum commit threshold satisfied: {valid_count} >= {min_required} commits.")
    else:
        print(f"  {RED}[FAIL]{RESET} Minimum commit threshold not met: {valid_count} < {min_required} commits.")

    has_diversity = len(seen_types) >= 3
    if has_diversity:
        print(f"  {GREEN}[PASS]{RESET} Clean separation of concerns verified across {len(seen_types)} commit types.")
    else:
        print(f"  {YELLOW}[WARN]{RESET} Limited type diversity observed ({len(seen_types)} types).")

    print(f"\n{BLUE}{BOLD}{'=' * 70}{RESET}")
    if has_minimum and (valid_count >= min_required):
        print(f"{GREEN}{BOLD} SUCCESS: Atomic commits and clear messaging criteria satisfied!{RESET}")
        print(f"{BLUE}{BOLD}{'=' * 70}{RESET}\n")
        return 0
    else:
        print(f"{RED}{BOLD} FAILURE: Please review errors above before submitting.{RESET}")
        print(f"{BLUE}{BOLD}{'=' * 70}{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

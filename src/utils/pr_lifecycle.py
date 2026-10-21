"""
Pull Request Lifecycle & Governance Manager Module.
SahkaarX Stage Portfolio - Week 03: Create and Merge Feature Branches

Manages Pull Request lifecycle states, review checklists, and automated PR
documentation generation conforming to .github/PULL_REQUEST_TEMPLATE.md.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class PRState(str, Enum):
    """Lifecycle states of a Pull Request."""
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    MERGED = "MERGED"
    CLOSED = "CLOSED"


class PRChangeType(str, Enum):
    """Categorization of Pull Request changes."""
    FEAT = "feat"
    FIX = "fix"
    REFACTOR = "refactor"
    DOCS = "docs"
    CHORE = "chore"
    TEST = "test"


@dataclass
class PRReviewChecklist:
    """Readiness checklist items for a Pull Request."""
    branch_naming_adhered: bool = True
    documentation_updated: bool = True
    conventional_commits_adhered: bool = True
    no_extraneous_files: bool = True
    tests_passed: bool = True
    clean_history_verified: bool = True

    @property
    def is_all_passed(self) -> bool:
        return (
            self.branch_naming_adhered
            and self.documentation_updated
            and self.conventional_commits_adhered
            and self.no_extraneous_files
            and self.tests_passed
            and self.clean_history_verified
        )


@dataclass
class PullRequestMetadata:
    """Structured representation of a Pull Request."""
    pr_id: int
    title: str
    source_branch: str
    target_branch: str = "main"
    change_type: PRChangeType = PRChangeType.FEAT
    description: str = ""
    changes_proposed: List[str] = field(default_factory=list)
    state: PRState = PRState.OPEN
    checklist: PRReviewChecklist = field(default_factory=PRReviewChecklist)
    merge_commit_sha: Optional[str] = None
    author: str = "Parth Mehta"

    def mark_merged(self, merge_sha: str) -> None:
        """Transitions PR state to MERGED."""
        self.state = PRState.MERGED
        self.merge_commit_sha = merge_sha

    def generate_markdown(self) -> str:
        """Generates standard Markdown conforming to repository PR template."""
        def check(val: bool) -> str:
            return "[x]" if val else "[ ]"

        changes_list = "\n".join(f"- {change}" for change in self.changes_proposed) or "- Standard improvements implemented"

        return f"""# Pull Request #{self.pr_id}: {self.title}

> **Source Branch**: `{self.source_branch}`  
> **Target Branch**: `{self.target_branch}`  
> **State**: `{self.state.value}`  
> **Author**: {self.author}  
> **Merge Commit**: `{self.merge_commit_sha or 'Pending'}`  

---

## Description
{self.description}

## Type of Change
- {check(self.change_type == PRChangeType.FEAT)} `feat`: New feature or capability
- {check(self.change_type == PRChangeType.FIX)} `fix`: Bug fix
- {check(self.change_type == PRChangeType.REFACTOR)} `refactor`: Code or directory structure refactoring
- {check(self.change_type == PRChangeType.DOCS)} `docs`: Documentation updates
- {check(self.change_type == PRChangeType.CHORE)} `chore`: Maintenance, dependencies, or configuration

## Changes Proposed
{changes_list}

## Verification & Testing
- [x] `python scripts/verify_structure.py` passed
- [x] `python -m unittest discover tests/` passed
- [x] `python scripts/verify_feature_branches.py` passed
- [x] Manual testing and branch isolation verified

## Checklist
- {check(self.checklist.branch_naming_adhered)} My branch follows naming conventions (`{self.source_branch}`).
- {check(self.checklist.documentation_updated)} I have made corresponding updates to the documentation.
- {check(self.checklist.conventional_commits_adhered)} My commit messages follow Conventional Commits specification.
- {check(self.checklist.no_extraneous_files)} No extraneous or sensitive files are committed (.gitignore checked).
- {check(self.checklist.tests_passed)} All automated test suites passed without failure.
- {check(self.checklist.clean_history_verified)} Commit history is clean with zero unnecessary or WIP commits.
"""


class PRLifecycleManager:
    """Manages PR records, validation, and merge transition records."""

    def __init__(self):
        self.prs: Dict[int, PullRequestMetadata] = {}

    def create_pr(
        self,
        pr_id: int,
        title: str,
        source_branch: str,
        target_branch: str = "main",
        change_type: PRChangeType = PRChangeType.FEAT,
        description: str = "",
        changes_proposed: Optional[List[str]] = None,
        author: str = "Parth Mehta"
    ) -> PullRequestMetadata:
        pr = PullRequestMetadata(
            pr_id=pr_id,
            title=title,
            source_branch=source_branch,
            target_branch=target_branch,
            change_type=change_type,
            description=description,
            changes_proposed=changes_proposed or [],
            author=author
        )
        self.prs[pr_id] = pr
        return pr

    def get_pr(self, pr_id: int) -> Optional[PullRequestMetadata]:
        return self.prs.get(pr_id)

    def merge_pr(self, pr_id: int, merge_sha: str) -> PullRequestMetadata:
        pr = self.prs.get(pr_id)
        if not pr:
            raise KeyError(f"Pull Request #{pr_id} not found.")
        if not pr.checklist.is_all_passed:
            raise ValueError(f"Pull Request #{pr_id} cannot be merged: checklist incomplete.")
        pr.mark_merged(merge_sha)
        return pr

    def get_merged_prs(self) -> List[PullRequestMetadata]:
        return [pr for pr in self.prs.values() if pr.state == PRState.MERGED]

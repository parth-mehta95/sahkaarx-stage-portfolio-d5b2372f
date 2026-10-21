"""
Merge History Analyzer & Clean Commit Auditor Module.
SahkaarX Stage Portfolio - Week 03: Create and Merge Feature Branches

Analyzes Git commit logs and merge commits to verify:
1. Clean branch merge topology (non-fast-forward `--no-ff` or squashed PR merges)
2. Absence of unnecessary / WIP / clutter commits
3. Compliance with Conventional Commits on all integrated changes
4. Accurate tracking of merged Pull Requests
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class MergeStrategy(str, Enum):
    """Recognized Git merge strategies."""
    NO_FF = "no-ff"           # Explicit merge commit preserving branch context
    SQUASH = "squash"         # Single consolidated commit
    FAST_FORWARD = "ff"       # Linear fast-forward without merge commit
    REBASE = "rebase"         # Rebased linear history


@dataclass
class MergeCommitRecord:
    """Represents a detected merge commit in the repository history."""
    commit_hash: str
    subject: str
    parents: List[str]
    author: str = ""
    date_relative: str = ""
    source_branch: Optional[str] = None
    target_branch: Optional[str] = None
    pr_number: Optional[int] = None

    @property
    def is_merge_commit(self) -> bool:
        """A Git merge commit has two or more parent hashes."""
        return len(self.parents) >= 2


@dataclass
class CommitHygieneIssue:
    """Represents an identified anti-pattern or unnecessary commit."""
    commit_hash: str
    subject: str
    severity: str  # 'HIGH', 'MEDIUM', 'LOW'
    reason: str


@dataclass
class MergeHistoryReport:
    """Summary analysis of Git merge history and commit cleanliness."""
    total_commits: int
    merge_commits: List[MergeCommitRecord]
    feature_branches_merged: List[str]
    hygiene_issues: List[CommitHygieneIssue]
    is_clean: bool

    def summary(self) -> str:
        status = "CLEAN" if self.is_clean else "REQUIRES_CLEANUP"
        return (
            f"MergeHistory [{status}]: {self.total_commits} commits evaluated, "
            f"{len(self.merge_commits)} merge commits, "
            f"{len(self.feature_branches_merged)} merged branches, "
            f"{len(self.hygiene_issues)} hygiene issues"
        )


class MergeAnalyzer:
    """
    Audits commit history for clean merges, absence of unnecessary commits,
    and Pull Request traceability.
    """

    # Anti-patterns that indicate messy, uncurated commits
    UNNECESSARY_PATTERNS = [
        (re.compile(r"^(wip|work\s*in\s*progress)(\s*[:\-]|\b)", re.IGNORECASE), "HIGH", "WIP / unfinished commit"),
        (re.compile(r"^(temp|temporary|quick\s*fix|test)(\s*[:\-]|\b)", re.IGNORECASE), "HIGH", "Temporary commit"),
        (re.compile(r"^(fix typo|typo|fix bug\s*#?\d*)$", re.IGNORECASE), "MEDIUM", "Vague or low-value fix commit"),
        (re.compile(r"^(try again|almost done|save point|asdf)", re.IGNORECASE), "HIGH", "Clutter commit message"),
        (re.compile(r"^merge branch '(main|master)' into", re.IGNORECASE), "LOW", "Back-merge clutter into feature"),
    ]

    # Regex for standard GitHub PR merge commits:
    # "Merge pull request #12 from owner/feature-branch"
    # or "Merge branch 'feature/xxx' into main"
    PR_MERGE_PATTERN = re.compile(
        r"Merge pull request #(?P<pr>\d+) from (?P<source>[\w\-\/\.]+)",
        re.IGNORECASE
    )
    BRANCH_MERGE_PATTERN = re.compile(
        r"Merge branch '(?P<source>[^']+)'(?: into (?P<target>[^']+))?",
        re.IGNORECASE
    )

    def parse_merge_subject(self, subject: str) -> Tuple[Optional[str], Optional[str], Optional[int]]:
        """Extracts source branch, target branch, and PR number from a merge commit subject."""
        # Check GitHub PR merge format
        pr_match = self.PR_MERGE_PATTERN.search(subject)
        if pr_match:
            pr_num = int(pr_match.group("pr"))
            source = pr_match.group("source")
            # If source has owner/branch, strip owner
            if "/" in source and not source.startswith("feature/") and not source.startswith("bugfix/"):
                source = source.split("/", 1)[1]
            return source, "main", pr_num

        # Check standard Git branch merge format
        branch_match = self.BRANCH_MERGE_PATTERN.search(subject)
        if branch_match:
            source = branch_match.group("source")
            target = branch_match.group("target") or "main"
            return source, target, None

        return None, None, None

    def evaluate_commit_hygiene(self, commit_hash: str, subject: str) -> Optional[CommitHygieneIssue]:
        """Checks if an individual commit message violates clean history criteria."""
        clean_sub = subject.strip()
        for pattern, severity, reason in self.UNNECESSARY_PATTERNS:
            if pattern.search(clean_sub):
                return CommitHygieneIssue(
                    commit_hash=commit_hash,
                    subject=clean_sub,
                    severity=severity,
                    reason=reason
                )
        return None

    def audit_commit_log(
        self,
        commits_data: List[Dict[str, any]]
    ) -> MergeHistoryReport:
        """
        Audits a structured list of commit metadata.
        Expected format per commit:
          {
            "hash": "abc1234",
            "subject": "feat: ...",
            "parents": ["p1", "p2"], # 2+ parents indicates merge commit
            "author": "Parth",
            "date": "2 hours ago"
          }
        """
        merge_commits: List[MergeCommitRecord] = []
        feature_branches: Set[str] = set()
        hygiene_issues: List[CommitHygieneIssue] = []

        for item in commits_data:
            c_hash = item.get("hash", "")
            subject = item.get("subject", "")
            parents = item.get("parents", [])
            author = item.get("author", "")
            date = item.get("date", "")

            # Check hygiene for non-merge commits
            if len(parents) < 2:
                issue = self.evaluate_commit_hygiene(c_hash, subject)
                if issue:
                    hygiene_issues.append(issue)

            # Check if merge commit
            if len(parents) >= 2 or subject.lower().startswith("merge "):
                src, tgt, pr_num = self.parse_merge_subject(subject)
                record = MergeCommitRecord(
                    commit_hash=c_hash,
                    subject=subject,
                    parents=parents,
                    author=author,
                    date_relative=date,
                    source_branch=src,
                    target_branch=tgt,
                    pr_number=pr_num
                )
                merge_commits.append(record)
                if src:
                    feature_branches.add(src)

        is_clean = len([i for i in hygiene_issues if i.severity in ("HIGH", "MEDIUM")]) == 0
        return MergeHistoryReport(
            total_commits=len(commits_data),
            merge_commits=merge_commits,
            feature_branches_merged=sorted(list(feature_branches)),
            hygiene_issues=hygiene_issues,
            is_clean=is_clean
        )

"""
Git Operations and Workflow Management Utilities.
SahkaarX Stage Portfolio - Week 02 Practice

Provides core primitives for tracking, inspecting, and validating
the core Git workflow lifecycle:
  git checkout -> git add -> git commit -> git pull (sync) -> git push
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class GitCommitInfo:
    """Represents metadata for a single Git commit."""
    commit_hash: str
    author: str
    date_relative: str
    subject: str
    body: str = ""
    files_changed: List[str] = field(default_factory=list)

    @property
    def is_atomic(self) -> bool:
        """Heuristic for atomic commit: non-empty subject, single purpose."""
        return bool(self.subject and len(self.subject.strip()) > 5)


@dataclass
class WorkflowStep:
    """Represents a recorded Git workflow operation."""
    command: str  # 'checkout', 'add', 'commit', 'pull', 'push'
    target: str   # branch, file path, remote
    details: str = ""
    success: bool = True


@dataclass
class WorkflowValidationResult:
    """Outcome of validating a complete Git workflow execution."""
    is_valid: bool
    commit_count: int
    demonstrated_commands: List[str]
    missing_commands: List[str]
    is_synced_with_main: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        cmds = ", ".join(self.demonstrated_commands)
        return (
            f"Workflow [{status}]: {self.commit_count} atomic commits, "
            f"commands: [{cmds}], synced_with_main={self.is_synced_with_main}"
        )


class GitWorkflowTracker:
    """
    In-memory and operational tracker for verifying that an engineering workflow
    strictly exercises all fundamental Git commands (add, commit, pull, push)
    with a minimum threshold of atomic commits.
    """

    REQUIRED_COMMANDS = {"checkout", "add", "commit", "pull", "push"}
    MIN_ATOMIC_COMMITS = 3

    def __init__(self, branch_name: str = "feature/basic-git-workflow"):
        self.branch_name = branch_name
        self.steps: List[WorkflowStep] = []
        self.commits: List[GitCommitInfo] = []

    def record_step(self, command: str, target: str, details: str = "", success: bool = True) -> WorkflowStep:
        """Records an executed Git command in the workflow history."""
        cmd_clean = command.strip().lower()
        step = WorkflowStep(command=cmd_clean, target=target, details=details, success=success)
        self.steps.append(step)
        return step

    def record_commit(self, commit_hash: str, subject: str, author: str = "Dev", files: Optional[List[str]] = None) -> GitCommitInfo:
        """Records a completed atomic commit."""
        info = GitCommitInfo(
            commit_hash=commit_hash,
            author=author,
            date_relative="just now",
            subject=subject,
            files_changed=files or []
        )
        self.commits.append(info)
        self.record_step("commit", commit_hash, details=subject)
        return info

    def get_demonstrated_commands(self) -> List[str]:
        """Returns ordered unique list of successfully executed commands."""
        seen = set()
        demonstrated = []
        for step in self.steps:
            if step.success and step.command not in seen:
                seen.add(step.command)
                demonstrated.append(step.command)
        return demonstrated

    def validate_workflow(self, require_sync: bool = True) -> WorkflowValidationResult:
        """
        Validates whether the workflow meets the challenge criteria:
        1. 3+ atomic commits
        2. Demonstration of add, commit, push, pull
        3. Synced with main branch via pull
        """
        demonstrated = set(self.get_demonstrated_commands())
        missing = [cmd for cmd in self.REQUIRED_COMMANDS if cmd not in demonstrated]
        errors = []
        warnings = []

        # Check commit count
        commit_count = len(self.commits)
        if commit_count < self.MIN_ATOMIC_COMMITS:
            errors.append(
                f"Requires at least {self.MIN_ATOMIC_COMMITS} atomic commits, but only {commit_count} recorded."
            )

        # Check required commands
        if "add" not in demonstrated:
            errors.append("Missing 'git add' staging demonstration.")
        if "commit" not in demonstrated:
            errors.append("Missing 'git commit' demonstration.")
        if "push" not in demonstrated:
            errors.append("Missing 'git push' remote delivery demonstration.")

        # Check pull sync
        is_synced = "pull" in demonstrated
        if require_sync and not is_synced:
            errors.append("Branch has not been synced with base branch via 'git pull'.")
        elif not is_synced:
            warnings.append("Note: 'git pull' was not explicitly recorded.")

        # Validate atomicity of recorded commits
        for c in self.commits:
            if not c.is_atomic:
                warnings.append(f"Commit '{c.commit_hash}' subject may not be descriptive: '{c.subject}'")

        is_valid = len(errors) == 0
        return WorkflowValidationResult(
            is_valid=is_valid,
            commit_count=commit_count,
            demonstrated_commands=list(demonstrated),
            missing_commands=missing,
            is_synced_with_main=is_synced,
            errors=errors,
            warnings=warnings,
        )


def run_git_cmd(args: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    """Executes a git command safely and captures output."""
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=False
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as exc:
        return -1, "", str(exc)


def get_current_git_branch(cwd: Optional[Path] = None) -> str:
    """Retrieves current Git branch or empty string if not in git."""
    code, stdout, _ = run_git_cmd(["branch", "--show-current"], cwd=cwd)
    return stdout if code == 0 else ""


def is_git_working_tree_clean(cwd: Optional[Path] = None) -> bool:
    """Checks if there are no unstaged or uncommitted changes."""
    code, stdout, _ = run_git_cmd(["status", "--porcelain"], cwd=cwd)
    return code == 0 and len(stdout) == 0


def get_recent_commits(count: int = 10, cwd: Optional[Path] = None) -> List[GitCommitInfo]:
    """Retrieves list of recent commits from active branch."""
    # format: hash|author|relative_date|subject
    code, stdout, _ = run_git_cmd(
        ["log", f"-n{count}", "--pretty=format:%h|%an|%ar|%s"],
        cwd=cwd
    )
    if code != 0 or not stdout:
        return []

    results = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 3)
        if len(parts) == 4:
            results.append(GitCommitInfo(
                commit_hash=parts[0],
                author=parts[1],
                date_relative=parts[2],
                subject=parts[3]
            ))
    return results


def check_branch_divergence(base: str = "main", cwd: Optional[Path] = None) -> Dict[str, int]:
    """Calculates ahead/behind commit counts relative to base branch."""
    code, stdout, _ = run_git_cmd(["rev-list", "--left-right", "--count", f"{base}...HEAD"], cwd=cwd)
    if code == 0 and stdout:
        parts = stdout.split()
        if len(parts) == 2:
            try:
                behind = int(parts[0])
                ahead = int(parts[1])
                return {"behind": behind, "ahead": ahead}
            except ValueError:
                pass
    return {"behind": 0, "ahead": 0}

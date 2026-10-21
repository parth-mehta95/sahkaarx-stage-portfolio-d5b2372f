"""
Branch Naming & Branching Strategy Validator Module.
SahkaarX Stage Portfolio - Week 03: Create and Merge Feature Branches

Provides enterprise-grade validation of Git branch naming conventions,
branch hygiene rules, and protection checks according to GitHub Flow
and team engineering guidelines.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class BranchType(str, Enum):
    """Recognized standard branch type prefixes."""
    FEATURE = "feature"
    BUGFIX = "bugfix"
    HOTFIX = "hotfix"
    RELEASE = "release"
    DOCS = "docs"
    REFACTOR = "refactor"
    CHORE = "chore"
    TEST = "test"


@dataclass
class BranchNameValidationResult:
    """Represents the evaluation outcome for a single branch name."""
    branch_name: str
    is_valid: bool
    branch_type: Optional[BranchType] = None
    descriptor: str = ""
    ticket_id: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        type_str = self.branch_type.value if self.branch_type else "unknown"
        return f"Branch '{self.branch_name}' [{status}] (type={type_str}, descriptor='{self.descriptor}')"


class BranchValidator:
    """
    Validates branch names against team branching conventions and rules.
    Standard syntax:
      <type>/<descriptor>
      or
      <type>/<ticket-id>-<descriptor>
    Examples:
      - feature/branch-strategy-validator
      - bugfix/PROJ-102-fix-null-pointer
      - docs/update-readme
    """

    PROTECTED_BRANCHES: Set[str] = {"main", "master", "develop", "production", "staging"}
    
    ALLOWED_PREFIXES: Set[str] = {
        BranchType.FEATURE.value,
        BranchType.BUGFIX.value,
        BranchType.HOTFIX.value,
        BranchType.RELEASE.value,
        BranchType.DOCS.value,
        BranchType.REFACTOR.value,
        BranchType.CHORE.value,
        BranchType.TEST.value,
    }

    # Pattern: <prefix>/[<TICKET-123>-]<lowercase-kebab-descriptor>
    BRANCH_PATTERN = re.compile(
        r"^(?P<prefix>[a-z]+)\/(?:(?P<ticket>[A-Z]{2,10}-\d+)-)?(?P<descriptor>[a-z0-9]+(?:-[a-z0-9]+)*)$"
    )

    def __init__(self, allowed_prefixes: Optional[Set[str]] = None, max_length: int = 60):
        self.allowed_prefixes = allowed_prefixes or set(self.ALLOWED_PREFIXES)
        self.max_length = max_length

    def validate_branch_name(self, branch_name: str) -> BranchNameValidationResult:
        """Evaluates whether a branch name complies with team naming conventions."""
        errors: List[str] = []
        warnings: List[str] = []

        if not branch_name or not branch_name.strip():
            return BranchNameValidationResult(
                branch_name=branch_name or "",
                is_valid=False,
                errors=["Branch name cannot be empty or whitespace."]
            )

        name = branch_name.strip()

        # Check protected branch name directly
        if name in self.PROTECTED_BRANCHES:
            return BranchNameValidationResult(
                branch_name=name,
                is_valid=True,
                descriptor=name,
                warnings=[f"'{name}' is a protected trunk branch, not a feature branch."]
            )

        # Check length
        if len(name) > self.max_length:
            errors.append(f"Branch name length ({len(name)}) exceeds maximum allowed ({self.max_length} chars).")

        # Check for whitespace
        if " " in name or "\t" in name:
            errors.append("Branch name must not contain whitespace characters.")

        # Check for uppercase letters in non-ticket portions
        if not name.startswith("hotfix/") and not name.startswith("bugfix/"):
            # Check if there are uppercase characters outside of prefix/
            parts = name.split("/", 1)
            if len(parts) == 2 and any(c.isupper() for c in parts[0]):
                errors.append("Branch prefix must be lowercase.")

        # Check format with regex
        match = self.BRANCH_PATTERN.match(name)
        if not match:
            if "/" not in name:
                errors.append(
                    f"Branch name '{name}' must include a recognized category prefix followed by '/' (e.g., 'feature/...')."
                )
            else:
                prefix = name.split("/", 1)[0]
                if prefix not in self.allowed_prefixes:
                    errors.append(
                        f"Unrecognized branch prefix '{prefix}'. Allowed prefixes: {sorted(self.allowed_prefixes)}"
                    )
                else:
                    errors.append(
                        "Branch descriptor must use lowercase kebab-case (e.g. 'feature/add-user-login')."
                    )
            return BranchNameValidationResult(
                branch_name=name,
                is_valid=False,
                errors=errors,
                warnings=warnings
            )

        prefix_str = match.group("prefix")
        ticket = match.group("ticket")
        descriptor = match.group("descriptor")

        if prefix_str not in self.allowed_prefixes:
            errors.append(
                f"Prefix '{prefix_str}' is not in allowed prefixes: {sorted(self.allowed_prefixes)}"
            )

        # Verify descriptor quality
        if len(descriptor) < 3:
            errors.append(f"Descriptor '{descriptor}' is too short (minimum 3 characters).")
        if descriptor in {"test", "temp", "wip", "branch", "feature", "fix"}:
            warnings.append(f"Descriptor '{descriptor}' is generic; prefer descriptive naming.")

        try:
            b_type = BranchType(prefix_str)
        except ValueError:
            b_type = None

        is_valid = len(errors) == 0
        return BranchNameValidationResult(
            branch_name=name,
            is_valid=is_valid,
            branch_type=b_type,
            descriptor=descriptor,
            ticket_id=ticket,
            errors=errors,
            warnings=warnings
        )

    def audit_branches(self, branch_names: List[str]) -> Dict[str, BranchNameValidationResult]:
        """Audits a collection of branch names and returns validation results."""
        return {name: self.validate_branch_name(name) for name in branch_names}

    def filter_valid_feature_branches(self, branch_names: List[str]) -> List[str]:
        """Returns only names of valid non-protected feature/bugfix branches."""
        valid_branches = []
        for name in branch_names:
            res = self.validate_branch_name(name)
            if res.is_valid and name not in self.PROTECTED_BRANCHES:
                valid_branches.append(name)
        return valid_branches

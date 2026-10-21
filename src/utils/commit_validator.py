"""
Conventional Commit Validator and Hygiene Module.
SahkaarX Stage Portfolio - Week 02 Practice

Provides validation rules and parsing logic adhering to the Conventional Commits
v1.0.0 specification (https://www.conventionalcommits.org/).
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple


STANDARD_COMMIT_TYPES: Set[str] = {
    "feat",      # A new feature
    "fix",       # A bug fix
    "docs",      # Documentation only changes
    "style",     # Formatting, missing semi-colons, etc (no code logic change)
    "refactor",  # Refactoring production code without changing behavior
    "perf",      # Performance optimization
    "test",      # Adding or correcting tests
    "build",     # Build system or external dependency updates
    "ci",        # CI/CD configuration files and scripts
    "chore",     # Maintenance, tooling, and internal repository tasks
    "revert",    # Reverting a previous commit
}

# Heuristic list of non-imperative words commonly flagged in commit subject lines
NON_IMPERATIVE_VERBS = {
    "added": "add",
    "adds": "add",
    "fixing": "fix",
    "fixes": "fix",
    "fixed": "fix",
    "updated": "update",
    "updates": "update",
    "updating": "update",
    "created": "create",
    "creates": "create",
    "creating": "create",
    "removed": "remove",
    "removes": "remove",
    "removing": "remove",
    "changed": "change",
    "changes": "change",
    "changing": "change",
    "implemented": "implement",
    "implements": "implement",
}

HEADER_REGEX = re.compile(
    r"^(?P<type>[a-zA-Z]+)"
    r"(?:\((?P<scope>[a-zA-Z0-9_\-\./]+)\))?"
    r"(?P<breaking>!)?"
    r":\s(?P<subject>.+)$"
)


@dataclass
class CommitValidationResult:
    """Represents the structured evaluation of a single commit message."""
    raw_message: str
    is_valid: bool = True
    commit_type: Optional[str] = None
    scope: Optional[str] = None
    is_breaking: bool = False
    subject: Optional[str] = None
    body: Optional[str] = None
    footers: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        """Returns human-readable validation summary."""
        status = "VALID" if self.is_valid else "INVALID"
        output = [f"[{status}] {self.raw_message.splitlines()[0] if self.raw_message else '<empty>'}"]
        for err in self.errors:
            output.append(f"  - ERROR: {err}")
        for warn in self.warnings:
            output.append(f"  - WARN:  {warn}")
        return "\n".join(output)


def validate_commit_message(
    message: str,
    max_header_length: int = 72,
    allowed_types: Optional[Set[str]] = None,
    enforce_lowercase_type: bool = True,
) -> CommitValidationResult:
    """
    Validates a commit message string against Conventional Commits standards.

    :param message: Full commit message string (header + optional body & footers).
    :param max_header_length: Maximum allowed characters for the first line (header).
    :param allowed_types: Set of allowed commit types (defaults to STANDARD_COMMIT_TYPES).
    :param enforce_lowercase_type: Whether the type prefix must be strictly lowercase.
    :return: CommitValidationResult instance with parsing metadata, errors, and warnings.
    """
    if allowed_types is None:
        allowed_types = STANDARD_COMMIT_TYPES

    result = CommitValidationResult(raw_message=message)

    if not message or not message.strip():
        result.is_valid = False
        result.errors.append("Commit message cannot be empty.")
        return result

    lines = message.splitlines()
    header = lines[0].strip()

    # Rule 1: Header length validation
    if len(header) > max_header_length:
        result.is_valid = False
        result.errors.append(
            f"Commit header exceeds maximum length of {max_header_length} chars ({len(header)} chars)."
        )

    # Rule 2: Header format match
    match = HEADER_REGEX.match(header)
    if not match:
        result.is_valid = False
        result.errors.append(
            "Header does not follow '<type>(<scope>): <subject>' or '<type>: <subject>' format."
        )
        return result

    commit_type = match.group("type")
    scope = match.group("scope")
    breaking_marker = match.group("breaking")
    subject = match.group("subject").strip()

    result.commit_type = commit_type.lower()
    result.scope = scope
    result.subject = subject
    result.is_breaking = bool(breaking_marker)

    # Rule 3: Enforce lowercase type
    if enforce_lowercase_type and commit_type != commit_type.lower():
        result.is_valid = False
        result.errors.append(f"Commit type '{commit_type}' must be lowercase '{commit_type.lower()}'.")

    # Rule 4: Type must belong to allowed types
    if result.commit_type not in allowed_types:
        result.is_valid = False
        result.errors.append(
            f"Invalid commit type '{result.commit_type}'. Allowed types: {', '.join(sorted(allowed_types))}."
        )

    # Rule 5: Subject should not be empty
    if not subject:
        result.is_valid = False
        result.errors.append("Commit subject description cannot be empty.")

    # Rule 6: Subject should not end with punctuation (period)
    if subject.endswith((".", "!", "?")):
        result.is_valid = False
        result.errors.append("Commit subject must not end with trailing punctuation ('.', '!', '?').")

    # Rule 7: Heuristic check for imperative mood (first word of subject)
    first_word = subject.split()[0].lower() if subject.split() else ""
    if first_word in NON_IMPERATIVE_VERBS:
        suggested = NON_IMPERATIVE_VERBS[first_word]
        result.warnings.append(
            f"Subject starts with '{first_word}'. Prefer imperative mood (e.g., '{suggested}')."
        )

    # Parse body and footers if multi-line
    if len(lines) > 1:
        # Check blank line between header and body
        if lines[1].strip() != "":
            result.warnings.append("Expected a blank line separating header and commit body.")

        body_lines = []
        footer_lines = []
        is_footer_section = False

        for line in lines[1:]:
            trimmed = line.strip()
            if trimmed.startswith("BREAKING CHANGE:") or trimmed.startswith("BREAKING-CHANGE:"):
                is_footer_section = True
                result.is_breaking = True
            elif re.match(r"^[a-zA-Z\-]+:\s", trimmed):
                is_footer_section = True

            if is_footer_section:
                if trimmed:
                    footer_lines.append(trimmed)
            else:
                body_lines.append(line)

        result.body = "\n".join(body_lines).strip() or None
        result.footers = footer_lines

    return result


def validate_commit_list(messages: List[str]) -> Tuple[bool, List[CommitValidationResult]]:
    """
    Validates a collection of commit messages.

    :param messages: List of commit message strings.
    :return: Tuple of (all_valid, list of CommitValidationResult).
    """
    results = [validate_commit_message(msg) for msg in messages]
    all_valid = all(res.is_valid for res in results)
    return all_valid, results

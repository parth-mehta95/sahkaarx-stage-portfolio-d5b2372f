"""
Unit tests for BranchValidator.
SahkaarX Stage Portfolio - Week 03: Create and Merge Feature Branches
"""

import unittest
from src.utils.branch_validator import (
    BranchValidator,
    BranchType,
    BranchNameValidationResult,
)


class TestBranchValidator(unittest.TestCase):
    """Test suite for branch naming convention and hygiene rules."""

    def setUp(self):
        self.validator = BranchValidator()

    def test_valid_standard_feature_branches(self):
        """Tests that standard feature branch naming formats are recognized as valid."""
        valid_cases = [
            "feature/branch-strategy-validator",
            "feature/merge-history-analyzer",
            "feature/pr-lifecycle-manager",
            "feature/user-authentication",
            "bugfix/fix-null-pointer",
            "hotfix/critical-security-patch",
            "docs/update-branching-guidelines",
            "refactor/optimize-git-queries",
            "chore/bump-dependencies",
            "test/add-unit-test-suite",
        ]
        for branch in valid_cases:
            with self.subTest(branch=branch):
                result = self.validator.validate_branch_name(branch)
                self.assertTrue(result.is_valid, f"Expected '{branch}' to be valid: {result.errors}")
                self.assertIsNotNone(result.branch_type)
                self.assertTrue(len(result.descriptor) >= 3)

    def test_valid_branch_with_ticket_id(self):
        """Tests branch names containing issue / ticket trackers."""
        cases = [
            ("feature/PROJ-101-user-login", "PROJ-101", "user-login"),
            ("bugfix/ENG-404-connection-timeout", "ENG-404", "connection-timeout"),
            ("hotfix/SEC-99-patch-auth-leak", "SEC-99", "patch-auth-leak"),
        ]
        for branch, expected_ticket, expected_desc in cases:
            with self.subTest(branch=branch):
                result = self.validator.validate_branch_name(branch)
                self.assertTrue(result.is_valid)
                self.assertEqual(result.ticket_id, expected_ticket)
                self.assertEqual(result.descriptor, expected_desc)

    def test_protected_branches(self):
        """Tests that main, master, and develop are recognized as trunk branches."""
        for trunk in ["main", "master", "develop"]:
            result = self.validator.validate_branch_name(trunk)
            self.assertTrue(result.is_valid)
            self.assertTrue(any("protected trunk branch" in w for w in result.warnings))

    def test_invalid_branch_names(self):
        """Tests that improperly formatted branches are flagged as invalid."""
        invalid_cases = [
            ("", "Branch name cannot be empty"),
            ("   ", "Branch name cannot be empty"),
            ("just-a-name-no-prefix", "must include a recognized category prefix"),
            ("Feature/capital-prefix", "Branch prefix must be lowercase"),
            ("feature/HAS_UPPERCASE", "must use lowercase kebab-case"),
            ("unknown_prefix/my-feature", "must include a recognized category prefix"),
            ("feature/has space", "must not contain whitespace"),
            ("feature/ab", "too short"),
        ]
        for branch, error_keyword in invalid_cases:
            with self.subTest(branch=branch):
                result = self.validator.validate_branch_name(branch)
                self.assertFalse(result.is_valid, f"Expected '{branch}' to be invalid")
                self.assertTrue(any(error_keyword.lower() in err.lower() for err in result.errors))

    def test_audit_branches(self):
        """Tests bulk branch audit capability."""
        branches = [
            "main",
            "feature/branch-strategy-validator",
            "feature/merge-history-analyzer",
            "bugfix/resolve-conflict",
            "invalid_branch_name",
        ]
        audit_results = self.validator.audit_branches(branches)
        self.assertEqual(len(audit_results), 5)
        self.assertTrue(audit_results["feature/branch-strategy-validator"].is_valid)
        self.assertFalse(audit_results["invalid_branch_name"].is_valid)

    def test_filter_valid_feature_branches(self):
        """Tests filtering to retrieve only valid non-protected feature branches."""
        branches = [
            "main",
            "feature/branch-strategy-validator",
            "feature/merge-history-analyzer",
            "feature/pr-lifecycle-manager",
            "temp_work",
        ]
        filtered = self.validator.filter_valid_feature_branches(branches)
        self.assertEqual(
            filtered,
            [
                "feature/branch-strategy-validator",
                "feature/merge-history-analyzer",
                "feature/pr-lifecycle-manager",
            ]
        )


if __name__ == "__main__":
    unittest.main()

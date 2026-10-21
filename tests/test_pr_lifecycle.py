"""
Unit tests for PRLifecycleManager.
SahkaarX Stage Portfolio - Week 03: Create and Merge Feature Branches
"""

import unittest
from src.utils.pr_lifecycle import (
    PRLifecycleManager,
    PullRequestMetadata,
    PRState,
    PRChangeType,
    PRReviewChecklist,
)


class TestPRLifecycleManager(unittest.TestCase):
    """Test suite for Pull Request lifecycle and verification."""

    def setUp(self):
        self.manager = PRLifecycleManager()

    def test_create_and_retrieve_pr(self):
        """Tests standard PR creation and retrieval."""
        pr = self.manager.create_pr(
            pr_id=1,
            title="Implement Branch Strategy Validator",
            source_branch="feature/branch-strategy-validator",
            target_branch="main",
            change_type=PRChangeType.FEAT,
            description="Adds automated branch naming and hygiene checks.",
            changes_proposed=[
                "Implement BranchValidator in src/utils/branch_validator.py",
                "Add unit tests in tests/test_branch_validator.py",
            ]
        )
        self.assertEqual(pr.pr_id, 1)
        self.assertEqual(pr.state, PRState.OPEN)
        self.assertEqual(pr.source_branch, "feature/branch-strategy-validator")
        retrieved = self.manager.get_pr(1)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Implement Branch Strategy Validator")

    def test_merge_pr_with_valid_checklist(self):
        """Tests merging a PR whose checklist is fully satisfied."""
        pr = self.manager.create_pr(
            pr_id=2,
            title="Implement Merge History Analyzer",
            source_branch="feature/merge-history-analyzer"
        )
        self.assertTrue(pr.checklist.is_all_passed)
        merged_pr = self.manager.merge_pr(2, merge_sha="abc1234567")
        self.assertEqual(merged_pr.state, PRState.MERGED)
        self.assertEqual(merged_pr.merge_commit_sha, "abc1234567")

        merged_list = self.manager.get_merged_prs()
        self.assertEqual(len(merged_list), 1)
        self.assertEqual(merged_list[0].pr_id, 2)

    def test_merge_pr_fails_when_checklist_incomplete(self):
        """Tests that attempting to merge a PR with incomplete checklist raises ValueError."""
        pr = self.manager.create_pr(
            pr_id=3,
            title="Failing PR",
            source_branch="feature/broken"
        )
        pr.checklist.tests_passed = False
        with self.assertRaises(ValueError):
            self.manager.merge_pr(3, merge_sha="sha999")

    def test_generate_markdown(self):
        """Tests generation of PR markdown conforming to PR template format."""
        pr = self.manager.create_pr(
            pr_id=1,
            title="Add Branch Strategy Validator",
            source_branch="feature/branch-strategy-validator",
            description="Comprehensive validator for branch naming conventions.",
            changes_proposed=["Created branch_validator.py", "Added test suite"]
        )
        md = pr.generate_markdown()
        self.assertIn("# Pull Request #1: Add Branch Strategy Validator", md)
        self.assertIn("`feature/branch-strategy-validator`", md)
        self.assertIn("- [x] `feat`: New feature or capability", md)
        self.assertIn("Created branch_validator.py", md)
        self.assertIn("`python scripts/verify_structure.py` passed", md)


if __name__ == "__main__":
    unittest.main()

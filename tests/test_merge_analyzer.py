"""
Unit tests for MergeAnalyzer.
SahkaarX Stage Portfolio - Week 03: Create and Merge Feature Branches
"""

import unittest
from src.utils.merge_analyzer import (
    MergeAnalyzer,
    MergeHistoryReport,
    MergeCommitRecord,
    CommitHygieneIssue,
    MergeStrategy,
)


class TestMergeAnalyzer(unittest.TestCase):
    """Test suite for merge commit identification and commit hygiene analysis."""

    def setUp(self):
        self.analyzer = MergeAnalyzer()

    def test_parse_github_pr_merge_commit(self):
        """Tests parsing standard GitHub Pull Request merge commit subjects."""
        subject = "Merge pull request #1 from parth-mehta95/feature/branch-strategy-validator"
        src, tgt, pr_num = self.analyzer.parse_merge_subject(subject)
        self.assertEqual(src, "feature/branch-strategy-validator")
        self.assertEqual(tgt, "main")
        self.assertEqual(pr_num, 1)

    def test_parse_git_branch_merge_commit(self):
        """Tests parsing standard Git non-fast-forward merge commits."""
        subject = "Merge branch 'feature/merge-history-analyzer' into main"
        src, tgt, pr_num = self.analyzer.parse_merge_subject(subject)
        self.assertEqual(src, "feature/merge-history-analyzer")
        self.assertEqual(tgt, "main")
        self.assertIsNone(pr_num)

    def test_evaluate_commit_hygiene_clean_commits(self):
        """Tests that well-formed Conventional Commits pass hygiene checks."""
        clean_commits = [
            ("a1b2c3d", "feat(branch-validator): implement branch naming validator"),
            ("d4e5f6g", "test(merge-analyzer): add unit test coverage for merge commit history"),
            ("h7i8j9k", "docs(branching): author comprehensive branching strategy documentation"),
            ("l0m1n2o", "fix(git-ops): resolve detached head branch detection"),
        ]
        for c_hash, subject in clean_commits:
            with self.subTest(subject=subject):
                issue = self.analyzer.evaluate_commit_hygiene(c_hash, subject)
                self.assertIsNone(issue, f"Clean commit '{subject}' should not produce an issue")

    def test_evaluate_commit_hygiene_unnecessary_commits(self):
        """Tests that WIP, temporary, and clutter commit messages are flagged."""
        messy_commits = [
            ("1111111", "wip: working on branch validator", "HIGH"),
            ("2222222", "temp commit before lunch", "HIGH"),
            ("3333333", "fix typo", "MEDIUM"),
            ("4444444", "try again", "HIGH"),
        ]
        for c_hash, subject, expected_severity in messy_commits:
            with self.subTest(subject=subject):
                issue = self.analyzer.evaluate_commit_hygiene(c_hash, subject)
                self.assertIsNotNone(issue, f"Unclean commit '{subject}' must be flagged")
                self.assertEqual(issue.severity, expected_severity)

    def test_audit_commit_log_clean_scenario(self):
        """Tests an audit of a clean Git log with 3 feature branch merges."""
        mock_log = [
            {
                "hash": "m003",
                "subject": "Merge pull request #3 from feature/pr-lifecycle-manager",
                "parents": ["m002", "c005"],
                "author": "Parth Mehta",
                "date": "5 minutes ago",
            },
            {
                "hash": "c005",
                "subject": "feat(pr-lifecycle): implement pull request lifecycle manager",
                "parents": ["c004"],
                "author": "Parth Mehta",
                "date": "10 minutes ago",
            },
            {
                "hash": "m002",
                "subject": "Merge pull request #2 from feature/merge-history-analyzer",
                "parents": ["m001", "c003"],
                "author": "Parth Mehta",
                "date": "15 minutes ago",
            },
            {
                "hash": "c003",
                "subject": "feat(merge-analyzer): add merge history analysis utility",
                "parents": ["c002"],
                "author": "Parth Mehta",
                "date": "20 minutes ago",
            },
            {
                "hash": "m001",
                "subject": "Merge pull request #1 from feature/branch-strategy-validator",
                "parents": ["base", "c001"],
                "author": "Parth Mehta",
                "date": "25 minutes ago",
            },
            {
                "hash": "c001",
                "subject": "feat(branch-validator): implement branch naming validator",
                "parents": ["base"],
                "author": "Parth Mehta",
                "date": "30 minutes ago",
            },
        ]
        report = self.analyzer.audit_commit_log(mock_log)
        self.assertTrue(report.is_clean)
        self.assertEqual(len(report.merge_commits), 3)
        self.assertEqual(len(report.hygiene_issues), 0)
        self.assertIn("feature/branch-strategy-validator", report.feature_branches_merged)
        self.assertIn("feature/merge-history-analyzer", report.feature_branches_merged)
        self.assertIn("feature/pr-lifecycle-manager", report.feature_branches_merged)


if __name__ == "__main__":
    unittest.main()

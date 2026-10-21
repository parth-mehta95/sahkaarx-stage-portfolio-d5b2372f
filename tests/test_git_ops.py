"""
Unit Tests for Git Operations and Workflow Utilities.
SahkaarX Stage Portfolio - Week 02 Practice Deliverable
"""

import unittest
from pathlib import Path

from src.utils.git_ops import (
    GitCommitInfo,
    WorkflowStep,
    WorkflowValidationResult,
    GitWorkflowTracker,
    get_current_git_branch,
    is_git_working_tree_clean,
    get_recent_commits,
    check_branch_divergence,
)


class TestGitOperations(unittest.TestCase):
    """Test suite verifying basic Git workflow tracking, atomic commits, and sync checks."""

    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent

    def test_git_commit_info_atomicity(self):
        """Verifies atomic detection heuristic on commit messages."""
        c1 = GitCommitInfo(
            commit_hash="a1b2c3d",
            author="Dev",
            date_relative="1 hour ago",
            subject="feat(git-ops): implement git workflow tracker"
        )
        self.assertTrue(c1.is_atomic)

        c2 = GitCommitInfo(
            commit_hash="e4f5g6h",
            author="Dev",
            date_relative="now",
            subject="wip"
        )
        self.assertFalse(c2.is_atomic)

    def test_workflow_tracker_records_steps(self):
        """Verifies that GitWorkflowTracker correctly logs lifecycle steps."""
        tracker = GitWorkflowTracker(branch_name="feature/basic-git-workflow")
        s1 = tracker.record_step("checkout", "feature/basic-git-workflow")
        s2 = tracker.record_step("add", "src/utils/git_ops.py")
        s3 = tracker.record_commit("abc1234", "feat(git-ops): add core workflow module", files=["src/utils/git_ops.py"])

        self.assertEqual(len(tracker.steps), 3)
        self.assertEqual(tracker.steps[0].command, "checkout")
        self.assertEqual(tracker.steps[1].command, "add")
        self.assertEqual(tracker.steps[2].command, "commit")
        self.assertEqual(len(tracker.commits), 1)

    def test_workflow_tracker_demonstrated_commands(self):
        """Verifies deduplication of successfully demonstrated commands."""
        tracker = GitWorkflowTracker()
        tracker.record_step("add", "file1.py")
        tracker.record_step("add", "file2.py")
        tracker.record_step("commit", "hash1")
        tracker.record_step("commit", "hash2")
        tracker.record_step("pull", "origin main")
        tracker.record_step("push", "origin feature/test")

        cmds = tracker.get_demonstrated_commands()
        self.assertEqual(cmds, ["add", "commit", "pull", "push"])

    def test_workflow_tracker_valid_lifecycle(self):
        """Verifies that a full workflow with 3+ commits and sync passes validation."""
        tracker = GitWorkflowTracker(branch_name="feature/basic-git-workflow")
        tracker.record_step("checkout", "feature/basic-git-workflow")
        
        # 1. Add + commit 1
        tracker.record_step("add", "src/utils/git_ops.py")
        tracker.record_commit("hash101", "feat(git-ops): implement core workflow engine")

        # 2. Add + commit 2
        tracker.record_step("add", "tests/test_git_ops.py")
        tracker.record_commit("hash102", "test(git-ops): add unit tests for workflow tracker")

        # 3. Add + commit 3
        tracker.record_step("add", "practice/week-02-practice-basic-git-workflow-with-multiple-commit/")
        tracker.record_commit("hash103", "docs(practice): document basic git workflow and pr guide")

        # 4. Pull to sync with main
        tracker.record_step("pull", "origin main", details="Fast-forward or merge base sync")

        # 5. Push to GitHub
        tracker.record_step("push", "origin feature/basic-git-workflow")

        result = tracker.validate_workflow(require_sync=True)
        self.assertTrue(result.is_valid, f"Expected valid workflow, got errors: {result.errors}")
        self.assertEqual(result.commit_count, 3)
        self.assertTrue(result.is_synced_with_main)
        self.assertEqual(len(result.missing_commands), 0)

    def test_workflow_tracker_fails_with_under_three_commits(self):
        """Verifies failure when fewer than 3 atomic commits exist."""
        tracker = GitWorkflowTracker()
        tracker.record_step("checkout", "feature/test")
        tracker.record_step("add", "file.py")
        tracker.record_commit("hash1", "feat: initial commit")
        tracker.record_step("pull", "origin main")
        tracker.record_step("push", "origin feature/test")

        result = tracker.validate_workflow()
        self.assertFalse(result.is_valid)
        self.assertTrue(any("at least 3 atomic commits" in err for err in result.errors))

    def test_workflow_tracker_detects_missing_add_or_push(self):
        """Verifies that missing core commands trigger validation errors."""
        tracker = GitWorkflowTracker()
        tracker.record_step("checkout", "feature/test")
        # only commits recorded without add/push/pull
        for i in range(3):
            tracker.record_commit(f"hash{i}", f"feat: component change {i}")

        result = tracker.validate_workflow(require_sync=True)
        self.assertFalse(result.is_valid)
        self.assertIn("Missing 'git add' staging demonstration.", result.errors)
        self.assertIn("Missing 'git push' remote delivery demonstration.", result.errors)
        self.assertIn("Branch has not been synced with base branch via 'git pull'.", result.errors)

    def test_validation_result_summary_format(self):
        """Verifies format of human-readable summary output."""
        res = WorkflowValidationResult(
            is_valid=True,
            commit_count=3,
            demonstrated_commands=["checkout", "add", "commit", "pull", "push"],
            missing_commands=[],
            is_synced_with_main=True,
        )
        summary = res.summary()
        self.assertIn("Workflow [VALID]", summary)
        self.assertIn("3 atomic commits", summary)
        self.assertIn("synced_with_main=True", summary)

    def test_git_branch_and_status_helpers(self):
        """Verifies live inspection helpers return expected types safely."""
        branch = get_current_git_branch(self.repo_root)
        self.assertIsInstance(branch, str)

        clean = is_git_working_tree_clean(self.repo_root)
        self.assertIsInstance(clean, bool)

        commits = get_recent_commits(count=5, cwd=self.repo_root)
        self.assertIsInstance(commits, list)

        divergence = check_branch_divergence(base="main", cwd=self.repo_root)
        self.assertIsInstance(divergence, dict)
        self.assertIn("ahead", divergence)
        self.assertIn("behind", divergence)


if __name__ == "__main__":
    unittest.main()

"""
Unit and Integration Tests for Repository Structure and Core Utilities.
"""

import os
import unittest
from pathlib import Path

from src.utils.logger import setup_logger
from src.utils.env_helper import load_env_var


class TestRepositoryStructure(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent

    def test_essential_directories_exist(self):
        """Verifies that all required professional repository directories exist."""
        expected_dirs = [
            ".github",
            ".github/ISSUE_TEMPLATE",
            "docs",
            "practice",
            "practice/week-01-create-intentional-merge-conflicts-and-resolve",
            "practice/week-02-practice-atomic-commits-and-clear-messaging",
            "practice/week-02-practice-basic-git-workflow-with-multiple-commit",
            "practice/week-02-practice-gitignore-configuration-and-repository",
            "practice/week-02-restructure-portfolio-repo-with-professional-org",
            "practice/week-03-create-and-merge-feature-branches",
            "practice/week-06-finalize-capstone-integrate-variables-data-types",
            "scripts",
            "src",
            "src/utils",
            "tests",
        ]
        for rel_dir in expected_dirs:
            target = self.repo_root / rel_dir
            self.assertTrue(target.is_dir(), f"Expected directory '{rel_dir}' to exist.")

    def test_gitignore_contains_standard_ignores(self):
        """Verifies that .gitignore includes critical environment and language patterns."""
        gitignore_file = self.repo_root / ".gitignore"
        self.assertTrue(gitignore_file.is_file(), ".gitignore must exist in root.")
        content = gitignore_file.read_text(encoding="utf-8")

        required_patterns = [
            "__pycache__/",
            ".venv/",
            "node_modules/",
            ".env",
            ".DS_Store",
            "Thumbs.db",
            "*.log",
        ]
        for pattern in required_patterns:
            self.assertIn(pattern, content, f"Expected '{pattern}' in .gitignore")

    def test_logger_utility(self):
        """Verifies that setup_logger initializes cleanly and logs without error."""
        logger = setup_logger("TestLogger")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "TestLogger")
        logger.info("Structured logger test message")

    def test_env_helper_default(self):
        """Verifies fallback retrieval in load_env_var."""
        val = load_env_var("NON_EXISTENT_PORTFOLIO_KEY_XYZ", default="fallback_val")
        self.assertEqual(val, "fallback_val")

    def test_env_helper_required_raises(self):
        """Verifies load_env_var raises EnvironmentError when required key is missing."""
        with self.assertRaises(EnvironmentError):
            load_env_var("DEFINITELY_MISSING_KEY_12345", required=True)


if __name__ == "__main__":
    unittest.main()

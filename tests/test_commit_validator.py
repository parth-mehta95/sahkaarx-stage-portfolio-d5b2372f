"""
Unit Tests for Conventional Commit Validator and Hygiene Module.
SahkaarX Stage Portfolio - Week 02 Practice Deliverable
"""

import unittest

from src.utils.commit_validator import (
    validate_commit_message,
    validate_commit_list,
    CommitValidationResult,
    STANDARD_COMMIT_TYPES,
)


class TestCommitValidator(unittest.TestCase):
    """Test suite verifying Conventional Commits v1.0.0 compliance rules."""

    def test_valid_standard_commit_header(self):
        """Verifies simple valid header without scope."""
        msg = "feat: add user authentication controller"
        res = validate_commit_message(msg)
        self.assertTrue(res.is_valid, f"Expected valid, got: {res.errors}")
        self.assertEqual(res.commit_type, "feat")
        self.assertIsNone(res.scope)
        self.assertFalse(res.is_breaking)
        self.assertEqual(res.subject, "add user authentication controller")
        self.assertEqual(len(res.errors), 0)

    def test_valid_scoped_commit(self):
        """Verifies valid commit with scope."""
        msg = "fix(auth): handle expired jwt token gracefully"
        res = validate_commit_message(msg)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.commit_type, "fix")
        self.assertEqual(res.scope, "auth")
        self.assertFalse(res.is_breaking)

    def test_valid_breaking_change_exclamation(self):
        """Verifies breaking change exclamation mark syntax."""
        msg = "refactor(api)!: change user endpoint payload structure"
        res = validate_commit_message(msg)
        self.assertTrue(res.is_valid)
        self.assertTrue(res.is_breaking)
        self.assertEqual(res.commit_type, "refactor")
        self.assertEqual(res.scope, "api")

    def test_all_standard_types_recognized(self):
        """Verifies that all defined standard commit types pass validation."""
        for ctype in STANDARD_COMMIT_TYPES:
            msg = f"{ctype}(scope): implement test workflow for type {ctype}"
            res = validate_commit_message(msg)
            self.assertTrue(res.is_valid, f"Type '{ctype}' should be valid, errors: {res.errors}")
            self.assertEqual(res.commit_type, ctype)

    def test_empty_message_invalid(self):
        """Verifies empty and whitespace-only strings fail validation."""
        for empty_val in ["", "   ", "\n\n"]:
            res = validate_commit_message(empty_val)
            self.assertFalse(res.is_valid)
            self.assertIn("Commit message cannot be empty.", res.errors)

    def test_non_conventional_format_invalid(self):
        """Verifies messages lacking proper conventional structure are rejected."""
        invalid_messages = [
            "updated several files for review",
            "WIP",
            "fixed bug in checkout",
            "merge branch 'main' of github.com",
            "feat add new feature without colon",
        ]
        for msg in invalid_messages:
            res = validate_commit_message(msg)
            self.assertFalse(res.is_valid, f"Message '{msg}' should be invalid")

    def test_unknown_commit_type_rejected(self):
        """Verifies unknown commit types are rejected."""
        msg = "foo(core): add unknown operation"
        res = validate_commit_message(msg)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Invalid commit type 'foo'" in e for e in res.errors))

    def test_uppercase_type_rejected(self):
        """Verifies commit type must be strictly lowercase."""
        msg = "FEAT(auth): add google oauth provider"
        res = validate_commit_message(msg)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("must be lowercase" in e for e in res.errors))

    def test_trailing_punctuation_rejected(self):
        """Verifies subject ending in a period or exclamation is rejected."""
        for punct in [".", "!", "?"]:
            msg = f"chore(deps): bump urllib3 to 2.2.1{punct}"
            res = validate_commit_message(msg)
            self.assertFalse(res.is_valid)
            self.assertTrue(any("trailing punctuation" in e for e in res.errors))

    def test_header_length_limit(self):
        """Verifies header exceeding maximum length (72 chars) fails validation."""
        long_subject = "a" * 70
        msg = f"fix(core): {long_subject}"
        res = validate_commit_message(msg, max_header_length=72)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("exceeds maximum length" in e for e in res.errors))

    def test_imperative_mood_warning(self):
        """Verifies non-imperative verbs trigger helpful warnings without hard-failing."""
        msg = "feat(auth): added new session storage mechanism"
        res = validate_commit_message(msg)
        # Message format is valid, but should contain warning
        self.assertTrue(res.is_valid)
        self.assertTrue(any("Prefer imperative mood" in w for w in res.warnings))

    def test_multiline_commit_with_body_and_footer(self):
        """Verifies multi-line commit messages with body and breaking change footer."""
        full_msg = (
            "feat(auth): implement token rotation mechanism\n"
            "\n"
            "Rotate refresh tokens on each token grant to mitigate replay attacks.\n"
            "Old tokens are invalidated immediately upon exchange.\n"
            "\n"
            "BREAKING CHANGE: Auth header requires Bearer format exclusively.\n"
            "Fixes: #1024"
        )
        res = validate_commit_message(full_msg)
        self.assertTrue(res.is_valid)
        self.assertTrue(res.is_breaking)
        self.assertIsNotNone(res.body)
        self.assertIn("Rotate refresh tokens", res.body)
        self.assertGreaterEqual(len(res.footers), 2)

    def test_validate_commit_list(self):
        """Verifies batch validation of multiple commit messages."""
        valid_batch = [
            "feat(validator): implement conventional commit parser",
            "test(validator): add test coverage for parsing rules",
            "docs(guide): update atomic commits documentation",
        ]
        all_valid, results = validate_commit_list(valid_batch)
        self.assertTrue(all_valid)
        self.assertEqual(len(results), 3)

        mixed_batch = [
            "feat(validator): implement conventional commit parser",
            "bad commit message that fails",
        ]
        all_valid, results = validate_commit_list(mixed_batch)
        self.assertFalse(all_valid)
        self.assertTrue(results[0].is_valid)
        self.assertFalse(results[1].is_valid)


if __name__ == "__main__":
    unittest.main()

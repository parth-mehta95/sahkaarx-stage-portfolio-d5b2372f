"""
Unit Tests for .gitignore Configuration and Repository Cleanliness.
SahkaarX Stage Portfolio - Week 02 Practice Deliverable
"""

import fnmatch
import unittest
from pathlib import Path


class TestGitignoreRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent
        cls.gitignore_path = cls.repo_root / ".gitignore"
        if not cls.gitignore_path.is_file():
            raise FileNotFoundError(f".gitignore missing at {cls.gitignore_path}")
        cls.gitignore_content = cls.gitignore_path.read_text(encoding="utf-8")
        cls.lines = [
            line.strip()
            for line in cls.gitignore_content.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    def _is_matched(self, test_path: str) -> bool:
        """Determines if test_path matches any rule in .gitignore (handling negation)."""
        test_path = test_path.replace("\\", "/")
        is_ignored = False
        is_whitelisted = False

        for rule in self.lines:
            if rule.startswith("!"):
                pattern = rule[1:].strip()
                if self._match_single_pattern(test_path, pattern):
                    is_whitelisted = True
                    break
            else:
                if self._match_single_pattern(test_path, rule):
                    is_ignored = True

        return is_ignored and not is_whitelisted

    def _match_single_pattern(self, path_str: str, pattern: str) -> bool:
        pat = pattern.strip()
        if pat.endswith("/"):
            dir_pat = pat.rstrip("/")
            parts = path_str.split("/")
            if any(fnmatch.fnmatch(p, dir_pat) for p in parts[:-1]):
                return True
            if fnmatch.fnmatch(parts[-1], dir_pat):
                return True

        if "/" in pat:
            if pat.startswith("/"):
                return fnmatch.fnmatch(path_str, pat.lstrip("/"))
            return fnmatch.fnmatch(path_str, f"*{pat}*")

        file_name = path_str.split("/")[-1]
        if fnmatch.fnmatch(file_name, pat):
            return True
        for part in path_str.split("/"):
            if fnmatch.fnmatch(part, pat):
                return True
        return False

    def test_gitignore_file_present(self):
        """Validates that .gitignore exists and has substantial content."""
        self.assertTrue(self.gitignore_path.is_file())
        self.assertGreater(len(self.lines), 50, "Should contain at least 50 active rules")

    def test_python_bytecode_ignored(self):
        """Verifies bytecode patterns are excluded."""
        self.assertTrue(self._is_matched("module.pyc"))
        self.assertTrue(self._is_matched("pkg/__pycache__/module.cpython-310.pyc"))
        self.assertTrue(self._is_matched("compiled.pyo"))
        self.assertTrue(self._is_matched("lib.so"))

    def test_virtual_environments_ignored(self):
        """Verifies virtual environment directories are excluded."""
        self.assertTrue(self._is_matched(".venv/bin/python"))
        self.assertTrue(self._is_matched("venv/Scripts/pip.exe"))
        self.assertTrue(self._is_matched("env/lib/site-packages"))

    def test_packaging_and_builds_ignored(self):
        """Verifies Python build and distribution artifacts are excluded."""
        self.assertTrue(self._is_matched("dist/package-0.1.0-py3-none-any.whl"))
        self.assertTrue(self._is_matched("build/bdist.linux-x86_64/"))
        self.assertTrue(self._is_matched("src/package.egg-info/SOURCES.txt"))

    def test_testing_and_coverage_caches_ignored(self):
        """Verifies pytest, mypy, and coverage files are excluded."""
        self.assertTrue(self._is_matched(".pytest_cache/v/cache/stepwise"))
        self.assertTrue(self._is_matched(".mypy_cache/3.10/main.data.json"))
        self.assertTrue(self._is_matched(".ruff_cache/content"))
        self.assertTrue(self._is_matched(".coverage"))
        self.assertTrue(self._is_matched(".coverage.machine123"))
        self.assertTrue(self._is_matched("htmlcov/index.html"))

    def test_secrets_and_credentials_ignored(self):
        """Verifies sensitive secrets, private keys, and credential stores are excluded."""
        self.assertTrue(self._is_matched(".env"))
        self.assertTrue(self._is_matched(".env.local"))
        self.assertTrue(self._is_matched(".env.production"))
        self.assertTrue(self._is_matched("api_key.pem"))
        self.assertTrue(self._is_matched("server.key"))
        self.assertTrue(self._is_matched("client.crt"))
        self.assertTrue(self._is_matched("credentials.json"))
        self.assertTrue(self._is_matched("secrets.json"))
        self.assertTrue(self._is_matched("token.json"))

    def test_env_example_is_whitelisted(self):
        """Ensures .env.example template file is allowed to be tracked."""
        self.assertFalse(self._is_matched(".env.example"))

    def test_os_and_ide_artifacts_ignored(self):
        """Verifies OS metadata and editor specific configs are excluded."""
        self.assertTrue(self._is_matched(".DS_Store"))
        self.assertTrue(self._is_matched("Thumbs.db"))
        self.assertTrue(self._is_matched("desktop.ini"))
        self.assertTrue(self._is_matched(".idea/modules.xml"))
        self.assertTrue(self._is_matched("editor.swp"))

    def test_legitimate_code_is_not_ignored(self):
        """Ensures valid source files, tests, and documentation are NOT accidentally ignored."""
        self.assertFalse(self._is_matched("src/__init__.py"))
        self.assertFalse(self._is_matched("src/utils/logger.py"))
        self.assertFalse(self._is_matched("tests/test_repo_structure.py"))
        self.assertFalse(self._is_matched("README.md"))
        self.assertFalse(self._is_matched("docs/ARCHITECTURE.md"))


if __name__ == "__main__":
    unittest.main()

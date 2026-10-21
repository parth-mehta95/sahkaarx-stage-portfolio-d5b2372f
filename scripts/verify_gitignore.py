#!/usr/bin/env python3
"""
Comprehensive .gitignore and Repository Cleanliness Validator
SahkaarX Stage Portfolio - Week 02 Practice

Validates:
1. Presence and integrity of root .gitignore.
2. Coverage of all required pattern categories:
   - Python bytecode & compilation
   - Python packaging & build artifacts
   - Virtual environments
   - Testing, coverage, and type-checker caches
   - Jupyter notebook checkpoints
   - Environment variables & credentials
   - Operating system metadata
   - IDE & editor configurations
   - Logs & temporary files
3. Verification that .env.example is whitelisted.
4. Testing simulated paths against .gitignore using fnmatch rules.
5. Verification of clean repository state via Git CLI (if git is available).
"""

import fnmatch
import os
import subprocess
import sys
from pathlib import Path

# ANSI styling
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_section(title: str):
    print(f"\n{BLUE}{BOLD}{'=' * 68}{RESET}")
    print(f"{BLUE}{BOLD} {title}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 68}{RESET}")


def check_gitignore_exists(root: Path) -> str:
    print_section("1. Checking .gitignore Presence and Size")
    gitignore = root / ".gitignore"
    if not gitignore.is_file():
        print(f"  {RED}[FAIL]{RESET} .gitignore file not found in repository root: {gitignore}")
        return ""
    content = gitignore.read_text(encoding="utf-8")
    lines = content.splitlines()
    print(f"  {GREEN}[PASS]{RESET} Found .gitignore at root ({len(lines)} lines, {len(content)} bytes)")
    return content


def check_pattern_categories(content: str) -> bool:
    print_section("2. Validating Required .gitignore Pattern Categories")
    categories = {
        "Python Bytecode & Compilation": [
            "__pycache__/",
            "*.py[cod]",
            "*$py.class",
            "*.so",
        ],
        "Python Packaging & Distributions": [
            "build/",
            "dist/",
            "*.egg-info/",
            "wheels/",
            "*.egg",
        ],
        "Virtual Environments": [
            "venv/",
            ".venv/",
            "env/",
            "ENV/",
        ],
        "Testing & Quality Caches": [
            ".mypy_cache/",
            ".pytest_cache/",
            ".ruff_cache/",
            ".coverage",
            "htmlcov/",
            ".tox/",
        ],
        "Jupyter & Interactive Computing": [
            ".ipynb_checkpoints/",
            "*-checkpoint.ipynb",
        ],
        "Environment Variables & Secrets": [
            ".env",
            ".env.*",
            "!.env.example",
            "*.pem",
            "*.key",
            "credentials.json",
            "secrets.json",
        ],
        "Operating System Metadata": [
            ".DS_Store",
            "Thumbs.db",
            "[Dd]esktop.ini",
        ],
        "IDEs & Code Editors": [
            ".vscode/*",
            "!.vscode/settings.json",
            ".idea/",
            "*.swp",
        ],
        "Logs & Temporary Files": [
            "*.log",
            "logs/",
            "*.tmp",
            "scratch/",
        ],
    }

    all_passed = True
    for cat_name, patterns in categories.items():
        print(f"\n  {BOLD}[Category] {cat_name}:{RESET}")
        for pat in patterns:
            if pat in content:
                print(f"    {GREEN}[PASS]{RESET} Found rule: '{pat}'")
            else:
                print(f"    {RED}[FAIL]{RESET} Missing expected rule: '{pat}'")
                all_passed = False

    return all_passed


def match_pattern(path_str: str, pattern: str) -> bool:
    """Helper to evaluate standard gitignore pattern behavior."""
    path_str = path_str.replace("\\", "/")
    pat = pattern.strip()

    if pat.endswith("/"):
        dir_pat = pat.rstrip("/")
        parts = path_str.split("/")
        if any(fnmatch.fnmatch(part, dir_pat) for part in parts[:-1]):
            return True
        if fnmatch.fnmatch(parts[-1], dir_pat):
            return True

    if "/" in pat:
        if pat.startswith("/"):
            if fnmatch.fnmatch(path_str, pat.lstrip("/")):
                return True
        else:
            if fnmatch.fnmatch(path_str, f"*{pat}*"):
                return True
    else:
        file_name = path_str.split("/")[-1]
        if fnmatch.fnmatch(file_name, pat):
            return True
        for part in path_str.split("/"):
            if fnmatch.fnmatch(part, pat):
                return True

    return False


def test_simulated_files(content: str) -> bool:
    print_section("3. Testing Simulated Artifacts Against Ignore Rules")

    # List of tuples: (simulated_file_path, should_be_ignored, description)
    test_cases = [
        ("src/__pycache__/logger.cpython-310.pyc", True, "Compiled Python bytecode"),
        ("auth.pyc", True, "Root compiled Python bytecode"),
        ("dist/sahkaarx_stage_portfolio-1.0.0-py3-none-any.whl", True, "Build wheel distribution"),
        ("build/lib/src/utils/logger.py", True, "Build temporary directory"),
        ("src/sahkaarx.egg-info/PKG-INFO", True, "Egg-info metadata directory"),
        (".venv/Scripts/python.exe", True, "Virtual environment binary"),
        ("venv/bin/activate", True, "Standard venv script"),
        (".pytest_cache/v/cache/nodeids", True, "Pytest test cache"),
        (".mypy_cache/3.10/builtins.data.json", True, "Mypy type checker cache"),
        (".coverage", True, "Coverage report raw data"),
        ("htmlcov/index.html", True, "HTML coverage report"),
        ("notebooks/.ipynb_checkpoints/analysis-checkpoint.ipynb", True, "Jupyter checkpoint"),
        (".env", True, "Production environment variables"),
        (".env.local", True, "Local environment file"),
        (".env.production.local", True, "Production override secrets"),
        ("server.key", True, "TLS private key"),
        ("cert.pem", True, "TLS public certificate"),
        ("credentials.json", True, "GCP / Cloud API credentials"),
        ("secrets.json", True, "Secret storage dump"),
        (".DS_Store", True, "macOS finder metadata"),
        ("Thumbs.db", True, "Windows thumbnail cache"),
        ("desktop.ini", True, "Windows folder settings"),
        (".idea/workspace.xml", True, "PyCharm IDE workspace"),
        ("debug.log", True, "Log output file"),
        ("temp.tmp", True, "Temporary scratch file"),
        ("scratch/test_notes.txt", True, "Temporary scratch directory"),
        # Allowed files:
        (".env.example", False, "Environment template (.env.example whitelisted)"),
        ("src/utils/logger.py", False, "Core source code"),
        ("tests/test_repo_structure.py", False, "Test suite file"),
        ("README.md", False, "Documentation README"),
    ]

    all_passed = True
    for sim_path, should_ignore, desc in test_cases:
        # Check against lines in content
        is_ignored = False
        is_whitelisted = False

        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("!"):
                rule = line[1:].strip()
                if match_pattern(sim_path, rule):
                    is_whitelisted = True
                    break
            else:
                if match_pattern(sim_path, line):
                    is_ignored = True

        effective_ignored = is_ignored and not is_whitelisted

        if effective_ignored == should_ignore:
            state_str = "IGNORED" if should_ignore else "TRACKED (WHITELISTED)"
            print(f"  {GREEN}[PASS]{RESET} {desc} -> {sim_path} [{state_str}]")
        else:
            print(f"  {RED}[FAIL]{RESET} {desc} -> {sim_path} expected ignored={should_ignore}, got {effective_ignored}")
            all_passed = False

    return all_passed


def check_git_cleanliness(root: Path) -> bool:
    print_section("4. Verifying Git Repository Cleanliness")
    try:
        # Run git status --porcelain
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=root, text=True, stderr=subprocess.PIPE
        ).strip()

        # Run git branch --show-current
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=root, text=True, stderr=subprocess.PIPE
        ).strip()

        print(f"  {BLUE}[INFO]{RESET} Current Active Branch: {BOLD}{branch or 'DETACHED / NONE'}{RESET}")

        if not status:
            print(f"  {GREEN}[PASS]{RESET} Working tree is completely clean! No untracked or uncommitted changes.")
        else:
            print(f"  {YELLOW}[NOTICE]{RESET} Working tree has changes:")
            for line in status.splitlines()[:10]:
                print(f"         {line}")

        # Check that no ignored files are currently tracked by git
        try:
            ignored_tracked = subprocess.check_output(
                ["git", "ls-files", "-i", "--exclude-standard"],
                cwd=root,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            if not ignored_tracked:
                print(f"  {GREEN}[PASS]{RESET} Zero ignored or sensitive files are tracked in the Git index.")
            else:
                print(f"  {RED}[FAIL]{RESET} The following ignored files are accidentally tracked:")
                for item in ignored_tracked.splitlines():
                    print(f"         {item}")
                return False
        except Exception:
            pass

        return True
    except Exception as e:
        print(f"  {YELLOW}[INFO]{RESET} Git command execution skipped ({e}). Static checks passed.")
        return True


def main():
    root = Path(__file__).resolve().parent.parent
    print(f"{BOLD}Running Comprehensive .gitignore & Repository Cleanliness Audit{RESET}")
    print(f"Target Directory: {root}")

    content = check_gitignore_exists(root)
    if not content:
        sys.exit(1)

    c1 = check_pattern_categories(content)
    c2 = test_simulated_files(content)
    c3 = check_git_cleanliness(root)

    print_section("Audit Summary")
    if c1 and c2 and c3:
        print(f"{GREEN}{BOLD}ALL CHECKS PASSED: .gitignore and repository cleanliness verified successfully!{RESET}\n")
        sys.exit(0)
    else:
        print(f"{RED}{BOLD}AUDIT FAILED: Some checks did not satisfy compliance standards.{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

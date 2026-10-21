#!/usr/bin/env python3
"""
Week 06 Capstone Verification Script: Variables & Data Types Integration.
SahkaarX Stage Portfolio

Validates:
1. Presence of all required deliverables and documentation artifacts.
2. Type conversion engine accuracy, strictness, and Decimal precision.
3. Variable scope (LEGB) resolution order, closures, and isolation.
4. Comprehensive unit test execution and 100% pass rate.
"""

from decimal import Decimal
import os
from pathlib import Path
import sys
import unittest

# Ensure project root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# ANSI terminal colors
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_header(title: str):
    print(f"\n{BLUE}{BOLD}{'=' * 70}{RESET}")
    print(f"{BLUE}{BOLD} >> {title}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 70}{RESET}")


def check_deliverable_artifacts(root: Path) -> bool:
    print_header("1. Checking Capstone Deliverables & Documentation Artifacts")
    required_files = [
        "src/variables_data_types.py",
        "tests/test_variables_data_types.py",
        "practice/week-06-finalize-capstone-integrate-variables-data-types/README.md",
        "practice/week-06-finalize-capstone-integrate-variables-data-types/PULL_REQUEST.md",
        "practice/week-06-finalize-capstone-integrate-variables-data-types/VARIABLES_AND_SCOPE_GUIDE.md",
        "practice/week-06-finalize-capstone-integrate-variables-data-types/CAPSTONE_FINALIZATION_REPORT.md",
        "scripts/verify_variables_data_types.py",
        "scripts/run_capstone_finalization.ps1",
        "execute_capstone_workflow.py",
    ]

    all_passed = True
    for rel_path in required_files:
        p = root / rel_path
        if p.is_file():
            size = p.stat().st_size
            print(f"  {GREEN}[PASS]{RESET} Found: {rel_path} ({size} bytes)")
        else:
            print(f"  {RED}[FAIL]{RESET} Missing: {rel_path}")
            all_passed = False

    return all_passed


def check_type_conversions() -> bool:
    print_header("2. Validating Type Conversion Engine & Precision Rules")
    try:
        from src.variables_data_types import TypeConverter, TypeConversionError

        # 1. Integer conversion
        i1 = TypeConverter.to_int("256")
        assert i1 == 256, f"Expected 256, got {i1}"
        i_hex = TypeConverter.to_int("0x20", base=16)
        assert i_hex == 32, f"Expected 32, got {i_hex}"
        print(f"  {GREEN}[PASS]{RESET} Integer parsing (radix & standard) verified.")

        # Strict int rejects float fractional
        try:
            TypeConverter.to_int(99.9, strict=True)
            print(f"  {RED}[FAIL]{RESET} Strict int conversion did not reject float with fraction")
            return False
        except TypeConversionError:
            print(f"  {GREEN}[PASS]{RESET} Strict int conversion properly rejected float with fraction.")

        # 2. Float conversion
        f1 = TypeConverter.to_float("3.14159")
        assert abs(f1 - 3.14159) < 1e-6
        print(f"  {GREEN}[PASS]{RESET} Float conversion verified.")

        # 3. Boolean strict conversion
        b_true = TypeConverter.to_bool("enabled", strict=True)
        b_false = TypeConverter.to_bool("disabled", strict=True)
        assert b_true is True and b_false is False
        print(f"  {GREEN}[PASS]{RESET} Strict boolean token parsing ('enabled'/'disabled') verified.")

        # 4. Decimal precision
        d = TypeConverter.to_decimal(0.1, precision=2)
        assert d == Decimal("0.10"), f"Expected Decimal('0.10'), got {d}"
        print(f"  {GREEN}[PASS]{RESET} High-precision Decimal monetary quantization verified.")

        # 5. Collection conversions
        f_set = TypeConverter.to_collection([1, 2, 2, 3], target_type=frozenset)
        assert f_set == frozenset({1, 2, 3})
        print(f"  {GREEN}[PASS]{RESET} Collection transformation to frozenset verified.")

        return True
    except Exception as err:
        print(f"  {RED}[FAIL]{RESET} Type conversion check encountered error: {err}")
        return False


def check_scope_manager() -> bool:
    print_header("3. Validating Variable Scope Engine (LEGB) & Stateful Closures")
    try:
        from src.variables_data_types import ScopeManager, ScopeLevel

        # 1. LEGB Hierarchy
        legb = ScopeManager.demonstrate_legb_hierarchy()
        assert legb["local"] == "Local Scope Level [L]"
        assert legb["enclosing"] == "Enclosing-Outer [E]"
        assert legb["nonlocal_mutated"] == 15
        assert legb["global"] == "1.0.0"
        print(f"  {GREEN}[PASS]{RESET} LEGB Scope resolution order (Local, Enclosing, Global, Built-in) verified.")

        # 2. Stateful closure with nonlocal
        counter = ScopeManager.create_counter_closure(10, 5)
        v1, v2 = counter(), counter()
        assert v1 == 15 and v2 == 20, f"Expected 15, 20, got {v1}, {v2}"
        print(f"  {GREEN}[PASS]{RESET} Stateful closure maintaining enclosing scope with 'nonlocal' verified.")

        # 3. Comprehension scope isolation
        comp = ScopeManager.demonstrate_comprehension_scope()
        assert comp["scope_isolated_successfully"] is True
        print(f"  {GREEN}[PASS]{RESET} Python 3 comprehension scope isolation (preventing variable leak) verified.")

        # 4. Scope inspection
        snap = ScopeManager.inspect_variable_scope("x", local_scope={"x": [10, 20]})
        assert snap.scope_level == ScopeLevel.LOCAL and snap.is_mutable is True
        print(f"  {GREEN}[PASS]{RESET} Dynamic variable scope inspection and snapshot model verified.")

        return True
    except Exception as err:
        print(f"  {RED}[FAIL]{RESET} Scope manager check encountered error: {err}")
        return False


def run_unit_tests() -> bool:
    print_header("4. Running Automated Unit Test Suite (tests/test_variables_data_types.py)")
    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test_variables_data_types.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print(f"\n  {GREEN}[PASS]{RESET} All unit tests in test_variables_data_types.py passed ({result.testsRun} tests run).")
        return True
    else:
        print(f"\n  {RED}[FAIL]{RESET} Unit tests failed: {len(result.failures)} failures, {len(result.errors)} errors.")
        return False


def main():
    print(f"\n{BOLD}{'#' * 70}{RESET}")
    print(f"{BOLD}# SahkaarX Stage Portfolio: Week 06 Capstone Verification Suite    #{RESET}")
    print(f"{BOLD}{'#' * 70}{RESET}")

    artifacts_ok = check_deliverable_artifacts(REPO_ROOT)
    types_ok = check_type_conversions()
    scope_ok = check_scope_manager()
    tests_ok = run_unit_tests()

    print_header("5. Capstone Verification Summary")
    all_ok = artifacts_ok and types_ok and scope_ok and tests_ok

    if all_ok:
        print(f"  {GREEN}{BOLD}[ALL CHECKS PASSED]{RESET} The Variables & Data Types module is verified and production-ready!")
        sys.exit(0)
    else:
        print(f"  {RED}{BOLD}[SOME CHECKS FAILED]{RESET} Please review the failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

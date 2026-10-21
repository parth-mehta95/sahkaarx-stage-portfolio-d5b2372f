"""
Unit Tests for Variables & Data Types Core Engineering Module.
SahkaarX Stage Portfolio - Week 06 Capstone Finalization
"""

from datetime import datetime
from decimal import Decimal
import math
import unittest

from src.variables_data_types import (
    ConversionResult,
    DataProtection,
    ImmutableConfig,
    ImmutabilityViolationError,
    ScopeLevel,
    ScopeManager,
    ScopeResolutionError,
    ScopeSnapshot,
    TypeConverter,
    TypeConversionError,
)


class TestTypeConverter(unittest.TestCase):
    """Test suite validating the TypeConverter engine."""

    def test_to_int_standard_and_strict(self):
        # Standard valid cases
        self.assertEqual(TypeConverter.to_int(42), 42)
        self.assertEqual(TypeConverter.to_int("128"), 128)
        self.assertEqual(TypeConverter.to_int("  -500  "), -500)
        self.assertEqual(TypeConverter.to_int(45.99), 45)  # Truncation
        self.assertEqual(TypeConverter.to_int(True), 1)
        self.assertEqual(TypeConverter.to_int(False), 0)

        # Base parsing
        self.assertEqual(TypeConverter.to_int("0xff", base=16), 255)
        self.assertEqual(TypeConverter.to_int("1010", base=2), 10)

        # Strict mode
        with self.assertRaises(TypeConversionError):
            TypeConverter.to_int(True, strict=True)
        with self.assertRaises(TypeConversionError):
            TypeConverter.to_int(12.34, strict=True)
        self.assertEqual(TypeConverter.to_int(12.0, strict=True), 12)

        # Non-finite float handling
        with self.assertRaises(TypeConversionError):
            TypeConverter.to_int(float("nan"))
        with self.assertRaises(TypeConversionError):
            TypeConverter.to_int(float("inf"))

        # Fallbacks & Defaults
        self.assertEqual(TypeConverter.to_int("invalid_num", default=-1), -1)
        self.assertEqual(TypeConverter.to_int(None, default=0), 0)

    def test_to_float_standard_and_strict(self):
        self.assertAlmostEqual(TypeConverter.to_float(3.14159), 3.14159)
        self.assertAlmostEqual(TypeConverter.to_float("12.5e2"), 1250.0)
        self.assertEqual(TypeConverter.to_float(100), 100.0)
        self.assertEqual(TypeConverter.to_float(True), 1.0)

        # Strict checks
        with self.assertRaises(TypeConversionError):
            TypeConverter.to_float(True, strict=True)

        # Non-finite validation
        with self.assertRaises(TypeConversionError):
            TypeConverter.to_float(float("nan"), allow_nan_inf=False)
        self.assertTrue(math.isnan(TypeConverter.to_float(float("nan"), allow_nan_inf=True)))

        # Default fallback
        self.assertEqual(TypeConverter.to_float("bad_float", default=99.9), 99.9)

    def test_to_bool_standard_and_strict(self):
        # Non-strict truthiness
        self.assertTrue(TypeConverter.to_bool("True"))
        self.assertTrue(TypeConverter.to_bool("yes"))
        self.assertTrue(TypeConverter.to_bool("1"))
        self.assertTrue(TypeConverter.to_bool([1, 2]))
        self.assertFalse(TypeConverter.to_bool("false"))
        self.assertFalse(TypeConverter.to_bool("no"))
        self.assertFalse(TypeConverter.to_bool("0"))
        self.assertFalse(TypeConverter.to_bool([]))

        # Strict truthiness
        self.assertTrue(TypeConverter.to_bool("enabled", strict=True))
        self.assertFalse(TypeConverter.to_bool("disabled", strict=True))
        self.assertTrue(TypeConverter.to_bool(1, strict=True))
        self.assertFalse(TypeConverter.to_bool(0, strict=True))

        with self.assertRaises(TypeConversionError):
            TypeConverter.to_bool("random_string", strict=True)
        with self.assertRaises(TypeConversionError):
            TypeConverter.to_bool([1, 2, 3], strict=True)

    def test_to_decimal_precision(self):
        d1 = TypeConverter.to_decimal("19.99")
        self.assertEqual(d1, Decimal("19.99"))

        # Exact conversion from float avoids 0.1 float representation anomalies
        d2 = TypeConverter.to_decimal(0.1, precision=2)
        self.assertEqual(d2, Decimal("0.10"))

        d3 = TypeConverter.to_decimal("123.456789", precision=4)
        self.assertEqual(d3, Decimal("123.4568"))

        with self.assertRaises(TypeConversionError):
            TypeConverter.to_decimal("invalid_decimal")

        self.assertEqual(TypeConverter.to_decimal(None, default=Decimal("0.00")), Decimal("0.00"))

    def test_to_datetime_parsing(self):
        dt_str = "2026-10-21 14:00:00"
        parsed = TypeConverter.to_datetime(dt_str)
        self.assertEqual(parsed.year, 2026)
        self.assertEqual(parsed.month, 10)
        self.assertEqual(parsed.day, 21)

        # Custom format
        custom_dt = TypeConverter.to_datetime("21/10/2026", date_format="%d/%m/%Y")
        self.assertEqual(custom_dt.day, 21)

        # Unix timestamp
        ts_dt = TypeConverter.to_datetime(1700000000)
        self.assertIsInstance(ts_dt, datetime)

        # Fallback
        self.assertIsNone(TypeConverter.to_datetime("not a date", default=None))

    def test_to_collection_conversions(self):
        # List to frozenset
        src_list = [3, 1, 2, 2]
        f_set = TypeConverter.to_collection(src_list, target_type=frozenset)
        self.assertEqual(f_set, frozenset({1, 2, 3}))

        # Per-element converter
        str_nums = ["10", "20", "30"]
        int_tuple = TypeConverter.to_collection(str_nums, target_type=tuple, element_converter=int)
        self.assertEqual(int_tuple, (10, 20, 30))

    def test_safe_convert_result_contract(self):
        # Success
        res_ok = TypeConverter.safe_convert("100", "int")
        self.assertTrue(res_ok.success)
        self.assertEqual(res_ok.value, 100)
        self.assertEqual(res_ok.original_value, "100")
        self.assertEqual(res_ok.target_type, "int")
        self.assertIsNone(res_ok.error_message)

        # Failure
        res_fail = TypeConverter.safe_convert("abc", "int")
        self.assertFalse(res_fail.success)
        self.assertIsNone(res_fail.value)
        self.assertIn("Failed to parse int", res_fail.error_message)

    def test_implicit_vs_explicit_conversions_report(self):
        report = TypeConverter.demonstrate_implicit_vs_explicit_conversions()
        self.assertIn("implicit_conversions", report)
        self.assertIn("explicit_conversions", report)
        self.assertEqual(report["implicit_conversions"]["bool_arithmetic"]["result"], 7)
        self.assertEqual(report["explicit_conversions"]["float_to_int"]["result"], 45)


class TestScopeManager(unittest.TestCase):
    """Test suite validating the LEGB Variable Scope Engine."""

    def setUp(self):
        ScopeManager.reset_global_state()

    def tearDown(self):
        ScopeManager.reset_global_state()

    def test_demonstrate_legb_hierarchy(self):
        results = ScopeManager.demonstrate_legb_hierarchy()
        self.assertEqual(results["local"], "Local Scope Level [L]")
        self.assertEqual(results["enclosing"], "Enclosing-Outer [E]")
        self.assertEqual(results["nonlocal_mutated"], 15)  # 10 + 5
        self.assertEqual(results["global"], "1.0.0")
        self.assertEqual(results["builtin_len"], len("Local Scope Level [L]"))

    def test_counter_closure_stateful_nonlocal(self):
        counter = ScopeManager.create_counter_closure(initial_value=10, step=3)
        self.assertEqual(counter(), 13)
        self.assertEqual(counter(), 16)
        self.assertEqual(counter(), 19)

        # Independent closure instance
        counter2 = ScopeManager.create_counter_closure(initial_value=0, step=1)
        self.assertEqual(counter2(), 1)
        self.assertEqual(counter(), 22)  # Counter 1 remains unaffected

    def test_comprehension_scope_isolation(self):
        res = ScopeManager.demonstrate_comprehension_scope()
        self.assertTrue(res["scope_isolated_successfully"])
        self.assertEqual(res["enclosing_x_before_and_after"], "ENCLOSING_X")
        self.assertEqual(len(res["comprehension_values"]), 5)

    def test_update_global_state(self):
        initial_state = ScopeManager.update_global_state("test_param", "verified_val")
        self.assertEqual(initial_state["test_param"], "verified_val")
        self.assertEqual(initial_state["access_counter"], 1)
        self.assertEqual(len(initial_state["audit_log"]), 1)

    def test_inspect_variable_scope(self):
        local_env = {"x_local": 10}
        enclosing_env = {"y_enclosing": [1, 2, 3]}
        global_env = {"z_global": "active"}

        # Local
        s_local = ScopeManager.inspect_variable_scope("x_local", local_scope=local_env)
        self.assertEqual(s_local.scope_level, ScopeLevel.LOCAL)
        self.assertFalse(s_local.is_mutable)

        # Enclosing
        s_enc = ScopeManager.inspect_variable_scope("y_enclosing", local_scope=local_env, enclosing_scope=enclosing_env)
        self.assertEqual(s_enc.scope_level, ScopeLevel.ENCLOSING)
        self.assertTrue(s_enc.is_mutable)

        # Global
        s_glob = ScopeManager.inspect_variable_scope("z_global", local_scope=local_env, global_scope=global_env)
        self.assertEqual(s_glob.scope_level, ScopeLevel.GLOBAL)

        # Built-in
        s_builtin = ScopeManager.inspect_variable_scope("len", local_scope=local_env)
        self.assertEqual(s_builtin.scope_level, ScopeLevel.BUILTIN)

        # Not found
        with self.assertRaises(ScopeResolutionError):
            ScopeManager.inspect_variable_scope("undefined_var_xyz", local_scope=local_env, global_scope=global_env)


class TestDataProtectionAndBestPractices(unittest.TestCase):
    """Test suite validating Immutability and Defensive Copying."""

    def test_reference_vs_copy_isolation(self):
        data = [1, 2, [3, 4]]
        report = DataProtection.demonstrate_reference_vs_copy(data)
        self.assertTrue(report["alias_is_identical"])
        self.assertFalse(report["shallow_is_identical"])
        self.assertFalse(report["deep_is_identical"])

    def test_freeze_data(self):
        mutable_input = {"nums": [1, 2, 3], "tags": {"alpha", "beta"}}
        frozen = DataProtection.freeze_data(mutable_input)
        # Result should be nested tuples and frozensets
        self.assertIsInstance(frozen, tuple)
        for k, v in frozen:
            if k == "nums":
                self.assertIsInstance(v, tuple)
            elif k == "tags":
                self.assertIsInstance(v, frozenset)

    def test_immutable_config_namedtuple(self):
        cfg = ImmutableConfig(
            app_name="SahkaarX",
            timeout_seconds=30,
            debug_mode=False,
            tags=("capstone", "v1.0"),
        )
        self.assertEqual(cfg.app_name, "SahkaarX")
        with self.assertRaises(AttributeError):
            cfg.timeout_seconds = 60


if __name__ == "__main__":
    unittest.main()

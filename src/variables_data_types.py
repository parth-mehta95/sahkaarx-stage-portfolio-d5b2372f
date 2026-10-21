"""
Variables & Data Types Core Engineering Module.
SahkaarX Stage Portfolio - Week 06 Capstone Finalization

Provides enterprise-grade demonstrations, utilities, and validation for:
1. Explicit and Implicit Type Conversions (primitives, collections, decimals, datetimes).
2. Variable Scope Resolution following Python's LEGB rule (Local, Enclosing, Global, Built-in).
3. Stateful Closures and the 'nonlocal' and 'global' keywords.
4. Immutability patterns, defensive copying, and type-safe data structures.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
import math
from typing import Any, Callable, Dict, Final, FrozenSet, List, NamedTuple, Optional, Set, Tuple, Type, TypeVar, Union

from src.utils.logger import setup_logger

logger = setup_logger("VariablesDataTypes")

T = TypeVar("T")

# ---------------------------------------------------------------------------
# Constants & Best Practices: UPPERCASE naming and typing.Final
# ---------------------------------------------------------------------------
DEFAULT_FLOAT_TOLERANCE: Final[float] = 1e-9
MAX_INT_CONVERSION_STR_LEN: Final[int] = 4300
PORTFOLIO_MODULE_NAME: Final[str] = "SahkaarX.VariablesDataTypes"

# Global Module-Level Registry demonstrating Global Scope ('G' in LEGB)
GLOBAL_MODULE_STATE: Dict[str, Any] = {
    "version": "1.0.0",
    "environment": "production",
    "access_counter": 0,
    "audit_log": [],
}


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------
class TypeConversionError(ValueError):
    """Raised when an explicit type conversion fails or input is invalid."""
    def __init__(self, message: str, original_value: Any = None, target_type: Optional[str] = None):
        super().__init__(message)
        self.original_value = original_value
        self.target_type = target_type


class ScopeResolutionError(LookupError):
    """Raised when a variable cannot be resolved within the expected LEGB scope."""
    def __init__(self, var_name: str, checked_scopes: List[str]):
        super().__init__(f"Variable '{var_name}' could not be resolved across scopes: {', '.join(checked_scopes)}")
        self.var_name = var_name
        self.checked_scopes = checked_scopes


class ImmutabilityViolationError(TypeError):
    """Raised when attempting an unauthorized in-place mutation of a frozen data structure."""
    pass


# ---------------------------------------------------------------------------
# Scope Data Models & Enums
# ---------------------------------------------------------------------------
class ScopeLevel(str, Enum):
    """Enumeration representing Python's LEGB Scope hierarchy."""
    LOCAL = "Local (L)"
    ENCLOSING = "Enclosing (E)"
    GLOBAL = "Global (G)"
    BUILTIN = "Built-in (B)"


@dataclass(frozen=True)
class ConversionResult:
    """Immutable result encapsulation for safe type conversions."""
    success: bool
    value: Any
    original_value: Any
    original_type: str
    target_type: str
    error_message: Optional[str] = None


@dataclass(frozen=True)
class ScopeSnapshot:
    """Snapshot of a variable's resolution within the LEGB hierarchy."""
    variable_name: str
    scope_level: ScopeLevel
    value_repr: str
    is_mutable: bool
    memory_id: int
    type_name: str


class ImmutableConfig(NamedTuple):
    """Immutable configuration demonstrating NamedTuple best practice."""
    app_name: str
    timeout_seconds: int
    debug_mode: bool
    tags: Tuple[str, ...]


# ---------------------------------------------------------------------------
# 1. Type Conversion Engine
# ---------------------------------------------------------------------------
class TypeConverter:
    """
    Robust type conversion engine providing explicit, safe, and loss-preventing
    conversions across Python standard primitives and collections.
    """

    BOOLEAN_TRUE_STRINGS: Final[FrozenSet[str]] = frozenset({"true", "1", "yes", "y", "t", "on", "enabled"})
    BOOLEAN_FALSE_STRINGS: Final[FrozenSet[str]] = frozenset({"false", "0", "no", "n", "f", "off", "disabled"})

    @staticmethod
    def to_int(val: Any, default: Optional[int] = None, strict: bool = False, base: int = 10) -> int:
        """
        Converts value to int.
        - Supports int, float (truncated), numeric strings (with optional base).
        - If strict=True, floats with fractional parts or non-pure strings raise TypeConversionError.
        """
        if val is None:
            if default is not None:
                return default
            raise TypeConversionError("Cannot convert None to int without a default", val, "int")

        if isinstance(val, bool):
            if strict:
                raise TypeConversionError("Strict conversion rejects bool to int coercion", val, "int")
            return 1 if val else 0

        if isinstance(val, int):
            return val

        if isinstance(val, float):
            if math.isnan(val) or math.isinf(val):
                raise TypeConversionError(f"Cannot convert non-finite float {val} to int", val, "int")
            if strict and not val.is_integer():
                raise TypeConversionError(f"Strict conversion rejected float with fraction: {val}", val, "int")
            return int(val)

        if isinstance(val, str):
            clean_str = val.strip()
            if not clean_str:
                if default is not None:
                    return default
                raise TypeConversionError("Cannot convert empty string to int", val, "int")
            try:
                # Check for decimal string representation
                if "." in clean_str or "e" in clean_str.lower():
                    parsed_float = float(clean_str)
                    if strict and not parsed_float.is_integer():
                        raise TypeConversionError(f"Strict conversion rejected decimal string: {val}", val, "int")
                    return int(parsed_float)
                return int(clean_str, base)
            except ValueError as err:
                if default is not None:
                    return default
                raise TypeConversionError(f"Failed to parse int from string '{val}': {err}", val, "int") from err

        # Object implementing __int__
        if hasattr(val, "__int__"):
            try:
                return int(val)
            except Exception as err:
                if default is not None:
                    return default
                raise TypeConversionError(f"Object __int__ failed: {err}", val, "int") from err

        if default is not None:
            return default
        raise TypeConversionError(f"Unsupported type for int conversion: {type(val).__name__}", val, "int")

    @staticmethod
    def to_float(val: Any, default: Optional[float] = None, strict: bool = False, allow_nan_inf: bool = False) -> float:
        """
        Converts value to float with strictness and NaN/Inf validation.
        """
        if val is None:
            if default is not None:
                return default
            raise TypeConversionError("Cannot convert None to float without a default", val, "float")

        if isinstance(val, bool):
            if strict:
                raise TypeConversionError("Strict conversion rejects bool to float", val, "float")
            return 1.0 if val else 0.0

        try:
            result = float(val)
            if not allow_nan_inf and (math.isnan(result) or math.isinf(result)):
                if default is not None:
                    return default
                raise TypeConversionError(f"Non-finite float value '{result}' rejected by policy", val, "float")
            return result
        except (ValueError, TypeError) as err:
            if default is not None:
                return default
            raise TypeConversionError(f"Failed to convert '{val}' of type {type(val).__name__} to float", val, "float") from err

    @classmethod
    def to_bool(cls, val: Any, strict: bool = False) -> bool:
        """
        Converts value to boolean.
        - Under non-strict: standard Python truthiness rules apply.
        - Under strict: only real booleans, 0/1 integers, and standard strings ("true"/"false") pass.
        """
        if isinstance(val, bool):
            return val

        if strict:
            if isinstance(val, (int, float)) and val in (0, 1):
                return bool(val)
            if isinstance(val, str):
                normalized = val.strip().lower()
                if normalized in cls.BOOLEAN_TRUE_STRINGS:
                    return True
                if normalized in cls.BOOLEAN_FALSE_STRINGS:
                    return False
                raise TypeConversionError(f"Strict bool conversion unrecognized token: '{val}'", val, "bool")
            raise TypeConversionError(f"Strict bool conversion cannot accept type {type(val).__name__}", val, "bool")

        # Standard non-strict Python truthiness
        if isinstance(val, str):
            normalized = val.strip().lower()
            if normalized in cls.BOOLEAN_FALSE_STRINGS:
                return False
            if normalized in cls.BOOLEAN_TRUE_STRINGS:
                return True
        return bool(val)

    @staticmethod
    def to_decimal(val: Any, precision: Optional[int] = None, default: Optional[Decimal] = None) -> Decimal:
        """
        Converts value to high-precision Decimal, preventing binary floating-point inaccuracy.
        """
        if val is None:
            if default is not None:
                return default
            raise TypeConversionError("Cannot convert None to Decimal", val, "Decimal")

        try:
            # Float conversion should pass through string representation to avoid imprecise floats
            if isinstance(val, float):
                d = Decimal(str(val))
            elif isinstance(val, Decimal):
                d = val
            else:
                d = Decimal(str(val).strip())

            if precision is not None and precision >= 0:
                quantize_target = Decimal(f"1e-{precision}")
                return d.quantize(quantize_target)
            return d
        except (InvalidOperation, TypeError) as err:
            if default is not None:
                return default
            raise TypeConversionError(f"Failed converting '{val}' to Decimal: {err}", val, "Decimal") from err

    @staticmethod
    def to_datetime(val: Any, date_format: Optional[str] = None, default: Optional[datetime] = None) -> datetime:
        """
        Converts string, numeric timestamp, or date instance to datetime.
        """
        if isinstance(val, datetime):
            return val

        if val is None:
            if default is not None:
                return default
            raise TypeConversionError("Cannot convert None to datetime", val, "datetime")

        # Numeric Unix timestamp
        if isinstance(val, (int, float)):
            try:
                return datetime.fromtimestamp(val)
            except (ValueError, OverflowError, OSError) as err:
                if default is not None:
                    return default
                raise TypeConversionError(f"Invalid timestamp '{val}': {err}", val, "datetime") from err

        if isinstance(val, str):
            clean = val.strip()
            if date_format:
                try:
                    return datetime.strptime(clean, date_format)
                except ValueError as err:
                    if default is not None:
                        return default
                    raise TypeConversionError(f"String '{val}' does not match format '{date_format}'", val, "datetime") from err
            # ISO 8601 fallback
            try:
                return datetime.fromisoformat(clean)
            except ValueError:
                # Try common standard formats
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                    try:
                        return datetime.strptime(clean, fmt)
                    except ValueError:
                        continue
                if default is not None:
                    return default
                raise TypeConversionError(f"Cannot parse datetime from string '{val}'", val, "datetime")

        if default is not None:
            return default
        raise TypeConversionError(f"Unsupported datetime conversion source type: {type(val).__name__}", val, "datetime")

    @staticmethod
    def to_collection(
        val: Any,
        target_type: Type[Union[List, Tuple, Set, FrozenSet]] = list,
        element_converter: Optional[Callable[[Any], Any]] = None,
    ) -> Union[List, Tuple, Set, FrozenSet]:
        """
        Converts between iterable collections (list, tuple, set, frozenset)
        with optional per-element transformation.
        """
        if val is None:
            elements = []
        elif isinstance(val, (list, tuple, set, frozenset)):
            elements = val
        elif isinstance(val, (str, bytes)):
            elements = [val]  # Do not decompose string into characters by default
        elif hasattr(val, "__iter__"):
            elements = list(val)
        else:
            elements = [val]

        if element_converter:
            converted_elements = [element_converter(item) for item in elements]
        else:
            converted_elements = elements

        if target_type is list:
            return list(converted_elements)
        if target_type is tuple:
            return tuple(converted_elements)
        if target_type is set:
            return set(converted_elements)
        if target_type is frozenset:
            return frozenset(converted_elements)

        raise TypeConversionError(f"Unsupported target collection type: {target_type}", val, str(target_type))

    @classmethod
    def safe_convert(cls, val: Any, target_type_name: str, **kwargs) -> ConversionResult:
        """
        Safely converts a value to the specified type without raising exceptions,
        returning a standardized ConversionResult.
        """
        orig_type = type(val).__name__
        try:
            conv_map = {
                "int": cls.to_int,
                "float": cls.to_float,
                "bool": cls.to_bool,
                "decimal": cls.to_decimal,
                "datetime": cls.to_datetime,
                "str": lambda v, **kw: str(v),
            }
            converter = conv_map.get(target_type_name.lower())
            if not converter:
                return ConversionResult(
                    success=False,
                    value=None,
                    original_value=val,
                    original_type=orig_type,
                    target_type=target_type_name,
                    error_message=f"No safe converter registered for '{target_type_name}'",
                )

            converted_val = converter(val, **kwargs)
            return ConversionResult(
                success=True,
                value=converted_val,
                original_value=val,
                original_type=orig_type,
                target_type=target_type_name,
            )
        except Exception as err:
            return ConversionResult(
                success=False,
                value=None,
                original_value=val,
                original_type=orig_type,
                target_type=target_type_name,
                error_message=str(err),
            )

    @staticmethod
    def demonstrate_implicit_vs_explicit_conversions() -> Dict[str, Any]:
        """
        Demonstrates and returns comparative examples of implicit coercion vs explicit casting.
        """
        # Implicit Coercions
        implicit_int_plus_float = 42 + 3.14159           # int implicitly coerced to float -> 45.14159
        implicit_bool_arithmetic = True + True + 5       # bool implicitly coerced to int (1 + 1 + 5 = 7)
        implicit_bool_in_multiplication = False * 100    # bool coerced to 0

        # Explicit Conversions
        explicit_float_to_int = int(45.99)               # Explicit truncation -> 45
        explicit_str_to_int = int("1024")                # Explicit string parsing
        explicit_float_to_decimal = Decimal(str(0.1))    # Exact decimal representation
        explicit_list_to_frozenset = frozenset([1, 2, 2, 3])  # Deduplicated and immutable

        return {
            "implicit_conversions": {
                "int_plus_float": {"expression": "42 + 3.14159", "result": implicit_int_plus_float, "type": type(implicit_int_plus_float).__name__},
                "bool_arithmetic": {"expression": "True + True + 5", "result": implicit_bool_arithmetic, "type": type(implicit_bool_arithmetic).__name__},
                "bool_multiplication": {"expression": "False * 100", "result": implicit_bool_in_multiplication, "type": type(implicit_bool_in_multiplication).__name__},
            },
            "explicit_conversions": {
                "float_to_int": {"expression": "int(45.99)", "result": explicit_float_to_int, "type": type(explicit_float_to_int).__name__},
                "str_to_int": {"expression": 'int("1024")', "result": explicit_str_to_int, "type": type(explicit_str_to_int).__name__},
                "str_to_decimal": {"expression": 'Decimal("0.1")', "result": str(explicit_float_to_decimal), "type": "Decimal"},
                "list_to_frozenset": {"expression": "frozenset([1, 2, 2, 3])", "result": tuple(sorted(explicit_list_to_frozenset)), "type": "frozenset"},
            },
        }


# ---------------------------------------------------------------------------
# 2. Variable Scope Engine (LEGB Hierarchy)
# ---------------------------------------------------------------------------
class ScopeManager:
    """
    Encapsulates demonstration, state tracking, and introspection of Python's
    LEGB (Local, Enclosing, Global, Built-in) variable scope hierarchy.
    """

    @classmethod
    def demonstrate_legb_hierarchy(cls) -> Dict[str, Any]:
        """
        Executes a nested function structure demonstrating resolution at all 4 LEGB tiers:
        - Local (L): Inner function scope
        - Enclosing (E): Outer function scope surrounding inner closures
        - Global (G): Module-level global scope
        - Built-in (B): Python built-in namespace
        """
        # Global variable accessed:
        global_val = GLOBAL_MODULE_STATE["version"]

        # Enclosing scope variable
        enclosing_val = "Enclosing Scope Level [E]"
        enclosing_counter = 100

        def outer_function():
            # Local to outer, but Enclosing to inner
            outer_local = "Enclosing-Outer [E]"
            nonlocal_target = 10

            def inner_closure():
                # Local scope [L]
                local_val = "Local Scope Level [L]"
                # Nonlocal mutation of enclosing variable
                nonlocal nonlocal_target
                nonlocal_target += 5

                # Built-in [B] accessed without shadowing
                builtin_len_result = len(local_val)

                return {
                    "local": local_val,
                    "enclosing": outer_local,
                    "nonlocal_mutated": nonlocal_target,
                    "global": global_val,
                    "builtin_len": builtin_len_result,
                }

            return inner_closure()

        return outer_function()

    @staticmethod
    def create_counter_closure(initial_value: int = 0, step: int = 1) -> Callable[[], int]:
        """
        Demonstrates Enclosing Scope (E) and stateful closures using the 'nonlocal' keyword.
        The inner function maintains mutable state across invocations without global variables.
        """
        count = initial_value

        def increment() -> int:
            nonlocal count
            count += step
            return count

        return increment

    @staticmethod
    def demonstrate_comprehension_scope() -> Dict[str, Any]:
        """
        Demonstrates scope isolation in comprehensions.
        In Python 3, list, set, and dict comprehensions have their own local scope,
        preventing loop variable leakage into the enclosing function.
        """
        x = "ENCLOSING_X"
        # List comprehension uses variable 'x', but Python 3 does not overwrite enclosing 'x'
        comp_result = [x * 2 for x in range(5)]
        leak_prevented = (x == "ENCLOSING_X")

        return {
            "enclosing_x_before_and_after": x,
            "comprehension_values": comp_result,
            "scope_isolated_successfully": leak_prevented,
        }

    @classmethod
    def update_global_state(cls, key: str, value: Any) -> Dict[str, Any]:
        """
        Demonstrates controlled, audited modification of Global Scope ('G')
        using the 'global' keyword with defensive copying.
        """
        global GLOBAL_MODULE_STATE

        old_value = GLOBAL_MODULE_STATE.get(key)
        GLOBAL_MODULE_STATE[key] = value
        GLOBAL_MODULE_STATE["access_counter"] += 1
        GLOBAL_MODULE_STATE["audit_log"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "key": key,
            "old_value": str(old_value),
            "new_value": str(value),
        })

        logger.info(f"Global module state updated: key='{key}', counter={GLOBAL_MODULE_STATE['access_counter']}")
        return copy.deepcopy(GLOBAL_MODULE_STATE)

    @classmethod
    def reset_global_state(cls) -> None:
        """Resets global state to defaults for clean test isolation."""
        global GLOBAL_MODULE_STATE
        GLOBAL_MODULE_STATE = {
            "version": "1.0.0",
            "environment": "production",
            "access_counter": 0,
            "audit_log": [],
        }

    @staticmethod
    def inspect_variable_scope(
        var_name: str,
        local_scope: Optional[Dict[str, Any]] = None,
        enclosing_scope: Optional[Dict[str, Any]] = None,
        global_scope: Optional[Dict[str, Any]] = None,
    ) -> ScopeSnapshot:
        """
        Inspects where a given variable name resolves within the LEGB chain.
        Returns a ScopeSnapshot with metadata (scope level, mutability, memory id).
        """
        local_scope = local_scope if local_scope is not None else {}
        enclosing_scope = enclosing_scope if enclosing_scope is not None else {}
        global_scope = global_scope if global_scope is not None else globals()

        # 1. Local
        if var_name in local_scope:
            val = local_scope[var_name]
            level = ScopeLevel.LOCAL
        # 2. Enclosing
        elif var_name in enclosing_scope:
            val = enclosing_scope[var_name]
            level = ScopeLevel.ENCLOSING
        # 3. Global
        elif var_name in global_scope:
            val = global_scope[var_name]
            level = ScopeLevel.GLOBAL
        # 4. Built-in
        elif hasattr(__builtins__, var_name) if hasattr(__builtins__, "__dict__") else var_name in __builtins__:
            val = getattr(__builtins__, var_name) if hasattr(__builtins__, "__dict__") else __builtins__[var_name]
            level = ScopeLevel.BUILTIN
        else:
            raise ScopeResolutionError(var_name, ["Local", "Enclosing", "Global", "Built-in"])

        is_mutable = isinstance(val, (list, dict, set, bytearray))
        return ScopeSnapshot(
            variable_name=var_name,
            scope_level=level,
            value_repr=repr(val)[:100],
            is_mutable=is_mutable,
            memory_id=id(val),
            type_name=type(val).__name__,
        )


# ---------------------------------------------------------------------------
# 3. Best Practices: Immutability, Defensive Copying & Deep Diagnostics
# ---------------------------------------------------------------------------
class DataProtection:
    """
    Utilities demonstrating immutability, safe defensive copies, and protection
    against unintended mutable reference side-effects across scopes.
    """

    @staticmethod
    def create_safe_deep_copy(data: T) -> T:
        """
        Creates an independent deep copy of mutable structures, preventing
        downstream mutations from corrupting upstream or caller scopes.
        """
        return copy.deepcopy(data)

    @staticmethod
    def demonstrate_reference_vs_copy(original_list: List[int]) -> Dict[str, Any]:
        """
        Demonstrates the danger of reference aliasing vs the safety of defensive copies.
        """
        # Shallow alias: modifying alias modifies original!
        alias = original_list

        # Defensive shallow copy (slice or list())
        shallow = list(original_list)

        # Deep copy
        deep = copy.deepcopy(original_list)

        return {
            "alias_is_identical": (alias is original_list),
            "shallow_is_identical": (shallow is original_list),
            "deep_is_identical": (deep is original_list),
            "alias_id": id(alias),
            "original_id": id(original_list),
            "shallow_id": id(shallow),
            "deep_id": id(deep),
        }

    @staticmethod
    def freeze_data(val: Any) -> Any:
        """
        Recursively converts mutable collections (dict, list, set) into immutable equivalents
        (frozenset, tuple, mappingproxy).
        """
        if isinstance(val, (list, tuple)):
            return tuple(DataProtection.freeze_data(item) for item in val)
        if isinstance(val, (set, frozenset)):
            return frozenset(DataProtection.freeze_data(item) for item in val)
        if isinstance(val, dict):
            return tuple(sorted((k, DataProtection.freeze_data(v)) for k, v in val.items()))
        return val


# ---------------------------------------------------------------------------
# Self-Verification CLI Execution
# ---------------------------------------------------------------------------
def run_diagnostics() -> Dict[str, Any]:
    """Runs a full suite of diagnostics across the module and outputs results."""
    print("=" * 60)
    print(f"Running Diagnostics: {PORTFOLIO_MODULE_NAME}")
    print("=" * 60)

    converter_demos = TypeConverter.demonstrate_implicit_vs_explicit_conversions()
    legb_demo = ScopeManager.demonstrate_legb_hierarchy()
    closure = ScopeManager.create_counter_closure(10, 5)
    closure_vals = [closure(), closure(), closure()]
    comp_scope = ScopeManager.demonstrate_comprehension_scope()

    report = {
        "status": "HEALTHY",
        "converter_demonstrations": converter_demos,
        "legb_hierarchy_resolution": legb_demo,
        "closure_state_values": closure_vals,
        "comprehension_scope": comp_scope,
        "global_state_snapshot": GLOBAL_MODULE_STATE,
    }
    return report


if __name__ == "__main__":
    import pprint
    pprint.pprint(run_diagnostics())

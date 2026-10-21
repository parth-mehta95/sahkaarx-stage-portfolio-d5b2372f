"""
SahkaarX Stage Portfolio Core Module.
"""

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

__version__ = "1.0.0"
__author__ = "Parth Mehta"

__all__ = [
    "TypeConverter",
    "ScopeManager",
    "DataProtection",
    "ConversionResult",
    "ScopeSnapshot",
    "ScopeLevel",
    "ImmutableConfig",
    "TypeConversionError",
    "ScopeResolutionError",
    "ImmutabilityViolationError",
]

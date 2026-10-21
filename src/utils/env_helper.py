"""
Environment configuration helper for retrieving settings with fallbacks and type safety.
"""

import os
from typing import Any, Optional


def load_env_var(key: str, default: Optional[Any] = None, required: bool = False) -> Any:
    """
    Safely retrieves an environment variable.

    :param key: Environment variable name.
    :param default: Default fallback value if not defined.
    :param required: If True and key is missing, raises EnvironmentError.
    :return: Environment variable value or default.
    """
    val = os.getenv(key, default)
    if required and val is None:
        raise EnvironmentError(f"Required environment variable '{key}' is not set.")
    return val

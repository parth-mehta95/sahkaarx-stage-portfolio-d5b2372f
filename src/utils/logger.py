"""
Structured logging module for portfolio applications.
Provides standardized formatting and level controls.
"""

import logging
import sys


def setup_logger(name: str = "SahkaarX", level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a standardized console logger.

    :param name: Logger name identifier.
    :param level: Logging severity level (default: logging.INFO).
    :return: Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

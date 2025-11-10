"""Custom logging configuration using Loguru.

This module configures structured logging with multiple outputs:
file logging, error logging, and console output with colorization.
"""

import sys

from loguru import logger

handlers = [
    {
        "sink": "logs/.logfile.log",
        "level": "TRACE",
        "format": "[{time:YYYY-MM-DD HH:mm:ss} UTC] - [{level:7}] - [{name:10}:{line}] - {message}",
        "colorize": False,
        "rotation": "31 day",
        "compression": "zip",
        "enqueue": True,
        "catch": True,
    },
    {
        "sink": "logs/.errorfile.log",
        "level": "WARNING",
        "format": "[{time:YYYY-MM-DD HH:mm:ss} UTC] - [{level:7}] - [{name:10}:{line}] - {message}",
        "colorize": False,
        "rotation": "31 day",
        "compression": "zip",
        "enqueue": True,
        "catch": True,
    },
    {
        "sink": sys.stdout,
        "level": "TRACE",
        "format": "<level>[{time:YYYY-MM-DD HH:mm:ss} UTC] - [{level:7}] - [{name:10}:{line}] - {message}</level>",
        "colorize": True,
        "enqueue": True,
        "catch": True,
    }
]

logger.configure(handlers=handlers)

def logger_test():
    """Test all logging levels to verify configuration.

    This function logs messages at all levels to test the logging setup.
    """
    logger.trace("Test TRACE message")
    logger.debug("Test DEBUG message")
    logger.info("Test INFO message")
    logger.success("Test SUCCESS message")
    logger.warning("Test WARNING message")
    logger.error("Test ERROR message")
    logger.critical("Test CRITICAL message")

custom_logger = logger

"""
Set up a common logger for scripts that wish to use it
"""
import logging


def init(loglevel='info'):
    """
    Initialize preferred configuration for logging module
    """
    level = getattr(logging, loglevel.upper())
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level)

"""
Set up a common logger for scripts that wish to use it
"""
import logging


def init():
    """
    Initialize preferred configuration for logging module
    """
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

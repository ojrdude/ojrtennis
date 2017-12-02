"""
Utilities that don't belong in the files of any of the game components.
"""

from enum import Enum
import logging


class LeftOrRight(Enum):
    """
    Simple enumeration of game board sides left or right
    """
    LEFT = 1
    RIGHT = 2


def get_logger(instance):
    """
    Get the logger for this instance. Primarily implemented so logger can be mocked during testing.
    """
    return logging.getLogger(instance.__class__.__name__)

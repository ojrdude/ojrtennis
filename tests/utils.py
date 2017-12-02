"""
Test utilities.
"""
import unittest.mock


class MockLogger(unittest.mock.Mock):
    """
    Mock log object that stores the logged messages for assertions.
    """

    def __init__(self):
        super(MockLogger, self).__init__()
        self.logged_error_messages = []
        self.logging_level = None

    def error(self, msg, *args, **kwargs):
        """
        Mock of call to log an error. Stores the message.
        """
        if args or kwargs:
            raise AssertionError("Mock logger doesn't handle args and kwargs.")

        self.logged_error_messages.append(msg)

    def critical(self, msg, *args, **kwargs):
        """
        Mock of call to log a critical error. Stores the message.
        """
        self.error(msg, *args, **kwargs)

    def setLevel(self, lvl):
        # pylint: disable=invalid-name
        # That's the name in logging
        """
        Mock a call to set the level of logging. Stores the value
        """
        self.logging_level = lvl

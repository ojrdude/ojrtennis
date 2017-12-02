"""
Unit tests for the ojrtennis module.
"""
import logging
import unittest

from ojrtennis import Ojrtennis
from tests.utils import MockLogger


class OjrtennisTest(unittest.TestCase):
    # pylint: disable=invalid-name
    # Descriptive test names more important than naming convention
    """
    Unit tests for OjrTennis
    """

    def setUp(self):
        self.ojrtennis = _MockOjrtennis()  # pylint: disable=not-callable

    def test_check_config_no_config_file(self):
        """
        Test that when there's no config file, an appropriate error is logged and the program terminates.
        """
        # Given
        missing_config = 'Somethingthatisnevergoingtoexist'

        # When
        with self.assertRaises(SystemExit) as context_manager:
            self.ojrtennis.check_config(missing_config)
        exit_exception = context_manager.exception
        logged_messages = self.ojrtennis.get_logged_messages()

        # Then
        self.assertEqual(1, exit_exception.code)
        self.assertEqual(1, len(logged_messages))
        self.assertEqual('No config found called Somethingthatisnevergoingtoexist', logged_messages[0])

    def test_check_config_stanzas_missing(self):
        """
        Test that when an expected stanza is missing from the config file, an appropriate error is logged and
        the program terminates.
        """
        # Given
        file_names_and_stanzas = [('general', 'General'),
                                  ('gamescreen', 'Game Screen'),
                                  ('menuscreen', 'Menu Screen')]

        for file_name, stanza in file_names_and_stanzas:
            self.ojrtennis._logger.logged_error_messages = []

            # When
            with self.assertRaises(SystemExit) as context_manager:
                self.ojrtennis.check_config(f'testconfig/missingstanzas/{file_name}.ini')
            exit_exception = context_manager.exception
            logged_messages = self.ojrtennis.get_logged_messages()

            # Then
            self.assertEqual(1, exit_exception.code)
            self.assertEqual(1, len(logged_messages))
            self.assertEqual(f'Config has missing stanza "{stanza}"', logged_messages[0])

    def test_logging_level(self):
        """
        Test that the logging level can be set with the config file.
        """
        # Given
        file_names_and_config_levels = [('debug', logging.DEBUG),
                                        ('info', logging.INFO),
                                        ('warning', logging.WARNING),
                                        ('error', logging.ERROR),
                                        ('critical', logging.CRITICAL)]

        for file_name, config_level in file_names_and_config_levels:
            # When
            self.ojrtennis.check_config(f'testconfig/logginglevels/{file_name}.ini')

            # Then
            self.assertEqual(config_level, self.ojrtennis.get_logging_level())

    def test_logging_level_not_specified(self):
        """
        Test that if the logging level isn't set in the config file, an appropriate error is logged and the
        program terminates.
        """
        for i in range(1, 3):
            # Given
            file_name = f'testconfig/logginglevels/missing{i}.ini'

            # When
            with self.assertRaises(SystemExit) as context_manager:
                self.ojrtennis.check_config(file_name)
            exit_exception = context_manager.exception
            logged_messages = self.ojrtennis.get_logged_messages()

            # Then
            self.assertEqual(1, exit_exception.code)
            self.assertEqual(1, len(logged_messages))
            self.assertEqual('Logging Level not set in config', logged_messages[0])

    def test_unknown_logging_level(self):
        """
        Test that if the logging level in the config file isn't a valid value, an appropriate error is logged and the
        program terminates.
        """
        # Given
        file_name = 'testconfig/logginglevels/nonsense.ini'

        # When
        with self.assertRaises(SystemExit) as context_manager:
            self.ojrtennis.check_config(file_name)
        exit_exception = context_manager.exception
        logged_messages = self.ojrtennis.get_logged_messages()

        # Then
        self.assertEqual(1, exit_exception.code)
        self.assertEqual(1, len(logged_messages))
        self.assertEqual('Logging Level value not valid: "Not a valid value"', logged_messages[0])


class _MockOjrtennis(Ojrtennis):
    # pylint: disable=inherit-non-class
    # It is a class, I can't tell why Pylint thinks it isn't.
    """
    Ojrtennis but with the logger mocked.
    """

    def __init__(self):
        super(_MockOjrtennis, self).__init__()
        self._logger = MockLogger()

    def get_logged_messages(self):
        """
        Return all the messages logged by the class's logger.
        """
        return self._logger.logged_error_messages

    def get_logging_level(self):
        """
        Return the value that the logging level has been set at.
        """
        return self._logger.logging_level


if __name__ == '__main__':
    unittest.main()

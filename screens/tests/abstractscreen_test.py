"""
Tests for abstractscreen
"""
import configparser
import unittest.mock

from screens.abstractscreen import AbstractScreen
from tests.utils import MockLogger


class AbstractScreenTest(unittest.TestCase):
    """
    Unit tests for AbstractScreen
    """

    _EXPECTED_DEFAULT_BG_COLOUR = (0, 0, 0)
    _EXPECTED_DEFAULT_TEXT_COLOUR = (255, 255, 255)

    def setUp(self):
        self._config = configparser.ConfigParser()

    def test_valid_colours_in_config(self):
        """
        Test that when the colours in the config file are OK, no errors are logged.
        """
        self._set_config_colours('0,0,0', '255,255,255')
        screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
        self.assertEqual(0, len(screen.get_logged_messages()))
        self._assert_colours(screen, (0, 0, 0), (255, 255, 255))

        self._set_config_colours('255,255,255', '0,0,0')
        screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
        self.assertEqual(0, len(screen.get_logged_messages()))
        self._assert_colours(screen, (255, 255, 255), (0, 0, 0))

        self._set_config_colours('31,122,11', '254,190,97')
        screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
        self.assertEqual(0, len(screen.get_logged_messages()))
        self._assert_colours(screen, (31, 122, 11), (254, 190, 97))

    def test_too_many_colours_in_config(self):
        """
        Test that when there are too many colours in the config file, an error is logged and the default
        values are used.
        """
        self._set_config_colours('0,0,0,0', '255,255,255')
        screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
        self.assertEqual(1, len(screen.get_logged_messages()))
        self._assert_default_colours(screen)

        self._set_config_colours('0,0,0', '255,255,255,255')
        screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
        self.assertEqual(1, len(screen.get_logged_messages()))
        self._assert_default_colours(screen)

    def test_too_few_colours_in_config(self):
        """
        Test that when there are too few colours in the config file, an error is logged and the default
        values are used.
        """
        self._set_config_colours('0,0', '255,255,255')
        screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
        self.assertEqual(1, len(screen.get_logged_messages()))
        self._assert_default_colours(screen)

        self._set_config_colours('0,0,0', '255,255')
        screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
        self.assertEqual(1, len(screen.get_logged_messages()))
        self._assert_default_colours(screen)

    def test_colours_out_of_range(self):
        """
        Test that when the colours are not in the range of 0 <= x <= 255, an error is logged and the
        default values are used.
        """
        for bg_colour in ['-1,0,0', '0,-1,0', '0,0,-1', '256,0,0', '0,256,0', '0,0,256']:
            self._set_config_colours(bg_colour, '5,5,5')
            screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
            self.assertEqual(1, len(screen.get_logged_messages()))
            self._assert_default_colours(screen)

        for text_colour in ['-1,0,0', '0,-1,0', '0,0,-1', '256,0,0', '0,256,0', '0,0,256']:
            self._set_config_colours('5,5,5', text_colour)
            screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
            self.assertEqual(1, len(screen.get_logged_messages()))
            self._assert_default_colours(screen)

    def test_non_integer_values(self):
        """
        Test that when the colours are not integers an error is logged and the default colours are used.
        """
        for bg_colour in ['1.2', 'True', '?', '-0.3', '', ' ']:
            self._set_config_colours(bg_colour, '9,9,9')
            screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
            self.assertEqual(1, len(screen.get_logged_messages()))
            self._assert_default_colours(screen)

        for text_colour in ['1.2', 'True', '?', '-0.3', '', ' ']:
            self._set_config_colours('9,9,9', text_colour)
            screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
            self.assertEqual(1, len(screen.get_logged_messages()))
            self._assert_default_colours(screen)

    def test_no_keys(self):
        """
        Test that when the expected keys are missing an error is logged and the default colours are used.
        """
        self._config.read_dict({'Screen': {}})
        screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
        self.assertEqual(1, len(screen.get_logged_messages()))
        self._assert_default_colours(screen)

    def test_spaces_in_colours(self):
        """
        Test that when there are spaces in the config values it is tolerated and the colours are still set.
        """
        colours_with_spaces = [' 1,2,3', '1 ,2,3', '1, 2,3', '1,2 ,3', '1,2, 3', '1,2,3 ', '  1,2,3', ' 1,   2 ,3   ']
        for space_colour in colours_with_spaces:
            self._set_config_colours('9,9,9', space_colour)
            screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
            self.assertEqual(0, len(screen.get_logged_messages()))
            self._assert_colours(screen, (9, 9, 9), (1, 2, 3))

            self._set_config_colours(space_colour, '9,9,9')
            screen = MockAbstractScreen(unittest.mock.Mock(), self._config['Screen'])
            self.assertEqual(0, len(screen.get_logged_messages()))
            self._assert_colours(screen, (1, 2, 3), (9, 9, 9))

    def _set_config_colours(self, bg_colour, text_colour):
        """
        Set the config reader up with the specified values for Background Colour and Text Colour.
        """
        self._config.read_dict({
            'Screen': {
                'Background Colour': bg_colour,
                'Text Colour': text_colour}
        })

    def _assert_default_colours(self, screen):
        # pylint: disable=protected-access
        # Performing assertions against these protected values.
        """
        Assert that the colours for the background and text in the screen are set to their default values.
        """
        self.assertEqual(self._EXPECTED_DEFAULT_BG_COLOUR, screen._bg_colour)
        self.assertEqual(self._EXPECTED_DEFAULT_TEXT_COLOUR, screen._text_colour)

    def _assert_colours(self, screen, expected_bg_colour, expected_text_colour):
        # pylint: disable=protected-access
        # Performing assertions against these protected values.
        """
        Assert that the colours for the background and text in the screen are set to the expected values.
        """
        self.assertEqual(expected_bg_colour, screen._bg_colour)
        self.assertEqual(expected_text_colour, screen._text_colour)


class MockAbstractScreen(AbstractScreen):
    """
    AbstractScreen with abstract methods stubbed so the others can be tested.
    """

    def __init__(self, display_surf, config):
        with unittest.mock.patch('screens.abstractscreen.get_logger') as mock_get_logger:
            mock_get_logger.return_value = MockLogger()
            super(MockAbstractScreen, self).__init__(display_surf, config)

    def main_screen_loop(self):
        pass

    def get_logged_messages(self):
        """
        Return all the messages logged by the class's logger.
        """
        return self._logger.logged_error_messages


if __name__ == "__main__":
    unittest.main()

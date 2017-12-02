"""
Ojrtennis 'main' module i.e. the starting point for the game.
"""
import configparser
import logging
import sys

import pygame

from screens import game, gamemenu
from utilities import get_logger


class Ojrtennis:
    """
    Runs the game, handling transfers between different screens etc.
    """
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    CONFIG_FILE_LOC = 'config.ini'

    _EXPECTED_CONFIG_STANZAS = ['General', 'Game Screen', 'Menu Screen']

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self._logger = get_logger(self)

        self._config_parser = configparser.ConfigParser()

        pygame.display.set_caption('ojrtennis')

    def run_game(self):
        """
        Run the game, starting with the game menu. Creates classes to handle
        each individual screen depending on what stage in the game we are at.
        """
        pygame.init()  # @UndefinedVariable
        display_surf = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        while True:
            game_menu = gamemenu.GameMenu(display_surf, self._config_parser['Menu Screen'])
            user_choice = game_menu.main_screen_loop()

            if user_choice == gamemenu.MenuReturnValue.GAME:
                self._logger.info('Game option selected, starting game.')
                game_screen = game.Game(display_surf, self._config_parser['Game Screen'])
                game_screen.main_screen_loop()
                self._logger.info('Game has ended, returning to menu.')
            elif user_choice == gamemenu.MenuReturnValue.QUIT:
                self._logger.info('Quit option selected, quiting.')
                pygame.quit()  # @UndefinedVariable
                sys.exit()

    def check_config(self, config_file_location):
        """
        Check that all required values are in the config file. Log an error and terminate program if not.
        """
        config_found = self._config_parser.read(config_file_location)
        if not config_found:
            self._logger.critical(f'No config found called {config_file_location}')
            sys.exit(1)

        for stanza in self._EXPECTED_CONFIG_STANZAS:
            if stanza not in self._config_parser:
                self._logger.critical(f'Config has missing stanza "{stanza}"')
                sys.exit(1)


if __name__ == '__main__':
    # pylint: disable=invalid-name
    # _ojrtennis isn't a constant, it's a variables so the name is fine.
    _ojrtennis = Ojrtennis()
    _ojrtennis.check_config(Ojrtennis.CONFIG_FILE_LOC)
    _ojrtennis.run_game()
    # pylint: enable=invalid-name

"""
Ojrtennis 'main' module i.e. the starting point for the game.
"""
import logging
import sys

import pygame

from screens import game, gamemenu


class Ojrtennis:
    """
    Runs the game, handling transfers between different screens etc.
    """
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(self.__class__.__name__)
        self.display_surf = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('ojrtennis')

        self._menu_choice_functions = {gamemenu.MenuReturnValue.QUIT: self._quit_game,
                                       gamemenu.MenuReturnValue.ONE_PLAYER: self._one_player_game,
                                       gamemenu.MenuReturnValue.TWO_PLAYER: self._two_player_game}

    def run_game(self):
        """
        Run the game, starting with the game menu. Creates classes to handle
        each individual screen depending on what stage in the game we are at.
        """
        pygame.init()  # @UndefinedVariable

        while True:
            game_menu = gamemenu.GameMenu(self.display_surf)
            user_choice = game_menu.main_screen_loop()

            self._menu_choice_functions[user_choice]()

    def _one_player_game(self):
        """
        Start a one player game.
        """
        self._logger.info('One player game option selected, starting game.')
        game_screen = game.Game(self.display_surf, one_player=True)
        game_screen.main_screen_loop()
        self._logger.info('Game has ended, returning to menu.')

    def _two_player_game(self):
        """
        Start a two player game.
        """
        self._logger.info('Two player game option selected, starting game.')
        game_screen = game.Game(self.display_surf)
        game_screen.main_screen_loop()
        self._logger.info('Game has ended, returning to menu.')

    def _quit_game(self):
        """
        Quit the game.
        """
        self._logger.info('Quit option selected, quiting.')
        sys.exit()


if __name__ == '__main__':
    Ojrtennis().run_game()

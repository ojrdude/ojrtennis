"""
Ojrtennis 'main' module i.e. the starting point for the game.
"""
import pygame
import game
import gamemenu
import logging
import sys

class Ojrtennis: # TODO: Does this need to be a class?
    """
    Runs the game, handling transfers between different screens etc.
    """
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480

    def __init__(self):
        self._logger = logging.getLogger('ojrtennis')
    
    def run_game(self):
        """
        Run the game, starting with the game menu. Creates classes to handle
        each individual screen depending on what stage in the game we are at.
        """
        pygame.init()
        display_surf = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        while True:
            game_menu = gamemenu.GameMenu(display_surf)
            user_choice = game_menu.menu_loop()

            if user_choice == gamemenu.MenuReturnValue.GAME:
                self._logger.info('Game option selected, starting game.')
                game_screen = game.Game(display_surf)
                game_screen.main_game_loop()
                self._logger.info('Game has ended, returning to menu.')
            elif user_choice == gamemenu.MenuReturnValue.QUIT:
                self._logger.info('Quit option selected, quiting.')
                pygame.quit()
                sys.exit()
        
if __name__ == '__main__':
    ojrtennis = Ojrtennis()
    ojrtennis.run_game()

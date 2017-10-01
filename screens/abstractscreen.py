"""
Abstract base game screen.
"""

import abc
import logging
import sys

import pygame
import pygame.locals as pgLocals

class AbstractScreen(abc.ABC):
    """
    Abstract base class which contains common methods required by all different game
    screens such as handling quit and common attributes like the display surface.
    """

    def __init__(self, display_surf):
        self._display_surf = display_surf
        self._fps_clock = pygame.time.Clock()

        self._logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def main_screen_loop(self):
        """
        The entry point into a screen. Loops continuously until that screen
        is 'done' at which point it returns. Whether a value is returned is
        at the discretion of the subclass.
        """
        pass

    def _check_for_quit(self):
        """
        Check if the user wants to quit i.e. has clicked the cross or pressed
        Esc.
        """
        for event in pygame.event.get():
            if event.type == pgLocals.QUIT:
                self._quit('Quit Event - Exiting')
            elif event.type == pgLocals.KEYDOWN and event.key == pgLocals.K_ESCAPE:
                self._quit('Escape Key pressed - Exiting')
            else:
                pygame.event.post(event)

    def _quit(self, log_message):
        """
        Log the log_message and quit the game. Shuts down Pygame before killing
        process.
        """
        self._logger.info(log_message)
        pygame.quit()
        sys.exit()

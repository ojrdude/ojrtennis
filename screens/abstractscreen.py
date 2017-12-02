"""
Abstract base game screen.
"""

import abc
import sys

import pygame

import pygame.locals as pgLocals
from utilities import get_logger


class AbstractScreen(abc.ABC):
    """
    Abstract base class which contains common methods required by all different game
    screens such as handling quit and common attributes like the display surface.
    """
    _DEFAULT_BG_COLOUR = (0, 0, 0)
    _DEFAULT_TEXT_COLOUR = (255, 255, 255)

    def __init__(self, display_surf, config):
        self._display_surf = display_surf
        self._fps_clock = pygame.time.Clock()

        self._logger = get_logger(self)

        try:
            bg_colour = (int(x) for x in config['Background Colour'].split(','))
            text_colour = (int(x) for x in config['Text Colour'].split(','))
            self._bg_colour = tuple(bg_colour)
            self._text_colour = tuple(text_colour)
            assert len(self._bg_colour) == len(self._text_colour) == 3, 'Colours must be 3 parts'
            for colour_component in self._bg_colour + self._text_colour:
                assert 0 <= colour_component <= 255, 'RGB Colour compenents must be between 0 and 255 (inc.)'
        except (KeyError, ValueError, AssertionError) as e:
            self._logger.error('Error initialising from config. Default values will be used. '
                               f'Error="{e}"')
            self._bg_colour = self._DEFAULT_BG_COLOUR
            self._text_colour = self._DEFAULT_TEXT_COLOUR

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
        pygame.quit()  # @UndefinedVariable
        sys.exit()

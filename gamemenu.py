"""
The game menu.
"""
from enum import Enum
import logging
import sys

import pygame
# pylint: disable=unused-wildcard-import, wildcard-import
# pygame.locals is designed to be safe to wildcard import. Obviously not every value
# is used!
from pygame.locals import *
# pylint: enable=unused-wildcard-import, wildcard-import

pygame.init() # TODO: Work out why I need this here. Doesn't seem right to me.

class MenuReturnValue(Enum):
    """
    Enumerated type of the possible menu choices that could be returned to the
    caller by GameMenu. Could later have options like '1-player', '2-player' etc.
    """
    GAME = 1
    QUIT = 2


class MenuItem: # TODO: Is this just a namedtuple?
    """
    Represents an item on the menu that is displayed to the user.
    """

    def __init__(self, text, return_value):
        self.text = text
        self.return_value = return_value


class GameMenu:
    """
    Displays the menu to the user, controls the user's navigation within it and
    returns his/her choice of option.
    """
    
    _FPS = 50

    _BG_COLOUR = (0, 0, 0)

    _FONT_SIZE = 50
    _FONT = pygame.font.Font('freesansbold.ttf', _FONT_SIZE)
    _GAP_BETWEEN_OPTIONS = 30
    
    _TEXT_COLOUR = (255, 255, 255)

    _OPTIONS = [
        MenuItem('Start', MenuReturnValue.GAME),
        MenuItem('Quit', MenuReturnValue.QUIT),
        # Uncomment the below options to check menu renders properly with more options
##        MenuItem('Bollocks1', MenuReturnValue.QUIT),
##        MenuItem('MORE BOLLOCKS', MenuReturnValue.QUIT),
##        MenuItem('B0110ck5', MenuReturnValue.QUIT),
##        MenuItem('twat', MenuReturnValue.QUIT),
        ]
    
    def __init__(self, display_surface):
        # TODO: factor out a superclass Screen for Game, GameMenu as they both
        # have self._display_surf and are both Screens
        # Common methods: _check_for_quit, _quit
        # Common attributes: _fps_clock, _logger
        # Common but leave uncoupled for now: _BG_COLOUR
        self._display_surf = display_surface
        self._fps_clock = pygame.time.Clock()

        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)

        self._selected_option_number = 0

    @property
    def _highlighted_option(self):
        """
        Return the hightlighted option in the menu
        """
        return self._OPTIONS[self._selected_option_number]
    
    def menu_loop(self):
        """
        Loops through every frame and handles the user input to change the selection
        or return the choice to the caller.
        """
        while True:
            self._check_for_quit()
            self._handle_selection_change()
            if self._is_user_confirming_option():
                return self._highlighted_option.return_value
            
            self._display_surf.fill(self._BG_COLOUR)
            self._draw_menu_items()

            pygame.display.update()
            self._fps_clock.tick(self._FPS)

    def _check_for_quit(self):
        """
        Check if the user wants to quit i.e. has clicked the cross or pressed
        Esc.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self._quit('Quit Event - Exiting')
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._quit('Escape Key pressed - Exiting')
            else:
                pygame.event.post(event)

    def _handle_selection_change(self):
        """
        Check if the user is trying to select a different option on the menu
        by using the arrow keys. Change the highlighted option.
        """
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_UP:
                    self._highlight_previous_option()
            elif event.type == KEYDOWN  and event.key == K_DOWN:
                    self._highlight_next_option()
            else:
                pygame.event.post(event)

    def _is_user_confirming_option(self):
        """
        Return True if the user has pressed return, indicating that he/she has chosen
        the currently highlighted option.
        """
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                return True
        return False
    
    def _draw_menu_items(self):
        """
        Draw all the possible menu items on the screen, showing the currently
        selected one as highlighted.
        """
        # Draw items above middle of screen
        above_middle_options = self._OPTIONS[len(self._OPTIONS) // 2 - 1::-1]
        y_coord_middle_screen = self._display_surf.get_height() // 2
        y_coord_item = y_coord_middle_screen - self._GAP_BETWEEN_OPTIONS // 2 \
                         - self._FONT_SIZE
        x_coord_item = self._calculate_x_for_centre(self._display_surf.get_width(),
                                                    above_middle_options[0])
        self._render_menu_item(above_middle_options[0], x_coord_item, y_coord_item)
        for option in above_middle_options[1:]:
            y_coord_item -= self._GAP_BETWEEN_OPTIONS + self._FONT_SIZE
            x_coord_item = self._calculate_x_for_centre(
                self._display_surf.get_width(),
                option
                )
            self._render_menu_item(option, x_coord_item, y_coord_item)

        # Draw items below middle of screen
        below_middle_options = self._OPTIONS[len(self._OPTIONS) // 2:]
        y_coord_item = y_coord_middle_screen + self._GAP_BETWEEN_OPTIONS // 2
        x_coord_item = self._calculate_x_for_centre(self._display_surf.get_width(),
                                                    below_middle_options[0])
        self._render_menu_item(below_middle_options[0], x_coord_item, y_coord_item)
        for option in below_middle_options[1:]:
            y_coord_item += self._GAP_BETWEEN_OPTIONS + self._FONT_SIZE
            x_coord_item = self._calculate_x_for_centre(
                self._display_surf.get_width(),
                option
                )
            self._render_menu_item(option, x_coord_item, y_coord_item)

    def _calculate_x_for_centre(self, screen_width, option):
        """
        Return the x coordinate to write the option text at so that it appears centrally
        for the given screen width.
        """
        centre_screen_x = screen_width // 2
        self._FONT.set_bold(option == self._highlighted_option)
        word_width, _ = self._FONT.size(option.text)
        return centre_screen_x - word_width / 2

    def _render_menu_item(self, menu_item, x_coord, y_coord):
        """
        Render a menu item at (x_coord, y_coord) on the screen. If the item is the
        currently selected, render it in bold.
        """
        menu_item_text = self._FONT.render(menu_item.text, True, self._TEXT_COLOUR)
        self._display_surf.blit(menu_item_text, (x_coord, y_coord))
        
    def _quit(self, log_message):
        """
        Log the log_message and quit the game. Shuts down Pygame before killing
        process.
        """
        self._logger.info(log_message)
        pygame.quit()
        sys.exit()

    def _highlight_next_option(self):
        """
        Change the highlighted (i.e. selected) option to be the next in self._OPTIONS.
        If the currently selected is last in the list, change the highlighted to be
        the first in the list.
        """
        self._selected_option_number = (self._selected_option_number + 1)\
                                       % len(self._OPTIONS)

    def _highlight_previous_option(self):
        """
        Change the highlighted (i.e. selected) option to be the previous one in
        self._OPTIONS. If the currently selected is the first in the list, change the
        highlighted to be the last in the list.
        """
        self._selected_option_number = (self._selected_option_number - 1)\
                                       % len(self._OPTIONS)

"""
The game menu.
"""
import collections
from enum import Enum

import pygame
import pygame.locals as pgLocals

from screens.abstractscreen import AbstractScreen

MenuItem = collections.namedtuple('MenuItem', ['text', 'return_value'])

class MenuReturnValue(Enum):
    """
    Enumerated type of the possible menu choices that could be returned to the
    caller by GameMenu. Could later have options like '1-player', '2-player' etc.
    """
    GAME = 1
    QUIT = 2


class GameMenu(AbstractScreen):
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
        # pylint: disable=bad-continuation
        # The auto-comment/uncoment feature in IDLE puts comments at start of line.
        # The convenience outweighs the code 'badness'
##        MenuItem('Bollocks1', MenuReturnValue.QUIT),
##        MenuItem('MORE BOLLOCKS', MenuReturnValue.QUIT),
##        MenuItem('B0110ck5', MenuReturnValue.QUIT),
##        MenuItem('twat', MenuReturnValue.QUIT),
        # pylint: enable=bad-continuation
        ]

    def __init__(self, display_surface):
        super(GameMenu, self).__init__(display_surface)
        self._selected_option_number = 0

    @property
    def _highlighted_option(self):
        """
        Return the hightlighted option in the menu
        """
        return self._OPTIONS[self._selected_option_number]

    def main_screen_loop(self):
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

    def _handle_selection_change(self):
        """
        Check if the user is trying to select a different option on the menu
        by using the arrow keys. Change the highlighted option.
        """
        for event in pygame.event.get():
            if event.type == pgLocals.KEYDOWN and event.key == pgLocals.K_UP:
                self._highlight_previous_option()
            elif event.type == pgLocals.KEYDOWN  and event.key == pgLocals.K_DOWN:
                self._highlight_next_option()
            else:
                pygame.event.post(event)

    @staticmethod
    def _is_user_confirming_option():
        """
        Return True if the user has pressed return, indicating that he/she has chosen
        the currently highlighted option.
        """
        for event in pygame.event.get():
            if event.type == pgLocals.KEYDOWN and event.key == pgLocals.K_RETURN:
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

"""
Bat code for ojrtennis
"""

import pygame
from utilities import LeftOrRight

class Bat:
    """
    A Bat in the ojrtennis game that can be controlled by the player
    """
    
    WIDTH = 20
    HEIGHT = 70
    COLOUR = (255, 255, 255)

    def __init__(self, up_key, down_key, board_height, is_right_hand_bat=False):
        """
        :param:up_key: the button that will cause the bat to move up
        :param:down_key: the button that will cause the bat to move down
        :param:board_height: the number of 'cells' tall the board is.
        Corresponds to the maximum value of the Bat's y coordinate.
        """
        self.up_key = up_key
        self.down_key = down_key
        self._maximum_y = board_height

        self.x_coord = 0
        self._y_coord = 0

        self._speed = 3

        if is_right_hand_bat:
            self.side_of_board = LeftOrRight.RIGHT
        else:
            self.side_of_board = LeftOrRight.LEFT

        self.surf = None # Set upon first draw

    @property
    def y_coord(self):
        """
        Get the current Y Coordinate of the Centre of Bat
        """
        return self._y_coord

    @y_coord.setter
    def y_coord(self, y):
        """
        Set the current Y Coordinate of the Centre of Bat
        """
        assert y <= self._maximum_y, "Setting y_coord outside maximum"
        assert y >= 0, "Setting y_coord less than 0"
        self._y_coord = y

    @property
    def top_left(self):
        """
        Get the current coordinates of the top left corner of the bat.
        """
        x_coord = self.x_coord - self.WIDTH / 2
        y_coord = self.y_coord - self.HEIGHT / 2
        return x_coord, y_coord

    def move_up(self):
        """
        Move the bat up. This should be called when the player has pressed the
        button to move the bat upwards.
        """
        if self.y_coord - self._speed >= 0:
            self.y_coord -= self._speed
        else: # Don't go off screen.
            self.y_coord = 0
        
    def move_down(self):
        """
        Move the bat down. This should be called when the player has pressed
        the button to move the bat downwards.
        """
        if self.y_coord + self._speed <= self._maximum_y:
            self.y_coord += self._speed
        else: # Don't go off screen
            self.y_coord = self._maximum_y

    def draw(self, surface):
        """
        Draw the bat on the surface.
        """
        top_left_x, top_left_y = self.top_left
        bat_rect = pygame.Rect(top_left_x, top_left_y, self.WIDTH, self.HEIGHT)
        self.surf = pygame.draw.rect(surface, self.COLOUR, bat_rect)

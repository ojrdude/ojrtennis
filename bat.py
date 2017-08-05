"""
Bat code for ojrtennis
"""

import pygame
from utilities import LeftOrRight
from math import radians

class Bat:
    """
    A Bat in the ojrtennis game that can be controlled by the player
    """
    
    WIDTH = 20
    HEIGHT = 70
    COLOUR = (255, 255, 255)
    _ANGLE_MODIFIER = 20

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

    def test_collision_with_ball(self, ball_rect):
        """
        Test for a collision with the ball. Return a tuple (is_collision, angle_modifier).
        The angle_modifier is determined by which part of the bat the collision is with.
        N.B. angle_modifier will be None when no collision.wwwws
        """
        top_left_x, top_left_y = self.top_left
        section_height = self.HEIGHT // 3
        top_section = pygame.Rect(top_left_x, top_left_y, self.WIDTH, section_height)
        if top_section.colliderect(ball_rect):
            angle_modifier = radians(-1 * self._ANGLE_MODIFIER)
            if self.side_of_board == LeftOrRight.RIGHT:
                angle_modifier *= -1
            return True, angle_modifier

        bottom_section_top_left_y = top_left_y + self.HEIGHT - section_height
        bottom_section = pygame.Rect(top_left_x, bottom_section_top_left_y,
                                     self.WIDTH, section_height)
        if bottom_section.colliderect(ball_rect):
            angle_modifier = radians(self._ANGLE_MODIFIER)
            if self.side_of_board == LeftOrRight.RIGHT:
                angle_modifier *= -1
            return True, angle_modifier

        middle_section = pygame.Rect(top_left_x, top_left_y + section_height,
                                     self.WIDTH, section_height)
        if middle_section.colliderect(ball_rect):
            return True, 0
        
        return False, None
        

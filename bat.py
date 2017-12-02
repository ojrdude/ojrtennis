"""
Bat code for ojrtennis
"""

from math import radians
import math
import random

import pygame

from utilities import LeftOrRight
from utilities import UpOrDown


class Bat:
    """
    A Bat in the ojrtennis game that can be controlled by the player
    """

    WIDTH = 20
    HEIGHT = 70
    COLOUR = (255, 255, 255)
    ANGLE_MODIFIER = 20
    SERVE_ANGLE_MODIFIER = 30

    def __init__(self, up_key, down_key, serve_key, board_width, board_height, is_right_hand_bat=False):
        """
        :param:up_key: the button that will cause the bat to move up
        :param:down_key: the button that will cause the bat to move down
        :param:serve_key: the button that will cause the bat to serve the ball.
        :param:board_width: the number of pixels wide the board is.
        :param:board_height: the number of pixels tall the board is.
        Corresponds to the maximum value of the Bat's y coordinate.
        """
        self.up_key = up_key
        self.down_key = down_key
        self.serve_key = serve_key
        self._maximum_y = board_height

        if is_right_hand_bat:
            self._x_coord = board_width - 3 - self.WIDTH // 2
        else:
            self._x_coord = 3 + self.WIDTH // 2

        self._y_coord = board_height // 2

        self._speed = 3

        if is_right_hand_bat:
            self.side_of_board = LeftOrRight.RIGHT
        else:
            self.side_of_board = LeftOrRight.LEFT

    @property
    def top_left(self):
        """
        Get the current coordinates of the top left corner of the bat.
        """
        x_coord = self._x_coord - self.WIDTH // 2
        y_coord = self._y_coord - self.HEIGHT // 2
        return x_coord, y_coord

    @property
    def front_centre(self):
        """
        Return the current coordinates of the front centre of the bat.
        """
        x_coord, y_coord = self.top_left
        y_coord += self.HEIGHT // 2

        if self.side_of_board == LeftOrRight.LEFT:
            x_coord += self.WIDTH

        return x_coord, y_coord

    def move_up(self):
        """
        Move the bat up. This should be called when the player has pressed the
        button to move the bat upwards.
        """
        if self._y_coord - self._speed >= 0:
            self._y_coord -= self._speed
        else:  # Don't go off screen.
            self._y_coord = 0

    def move_down(self):
        """
        Move the bat down. This should be called when the player has pressed
        the button to move the bat downwards.
        """
        if self._y_coord + self._speed <= self._maximum_y:
            self._y_coord += self._speed
        else:  # Don't go off screen
            self._y_coord = self._maximum_y

    def draw(self, surface):
        """
        Draw the bat on the surface.
        """
        top_left_x, top_left_y = self.top_left
        bat_rect = pygame.Rect(top_left_x, top_left_y, self.WIDTH, self.HEIGHT)
        pygame.draw.rect(surface, self.COLOUR, bat_rect)

    def test_collision_with_ball(self, ball_rect):
        """
        Test for a collision with the ball. Return a tuple (is_collision, angle_modifier).
        The angle_modifier is determined by which part of the bat the collision is with.
        N.B. angle_modifier will be None when no collision.wwwws
        """
        top_left_x, top_left_y = self.top_left
        section_height = self.HEIGHT // 3
        top_section = pygame.Rect(
            top_left_x, top_left_y, self.WIDTH, section_height)
        if top_section.colliderect(ball_rect):
            angle_modifier = radians(-1 * self.ANGLE_MODIFIER)
            if self.side_of_board == LeftOrRight.RIGHT:
                angle_modifier *= -1
            return True, angle_modifier

        bottom_section_top_left_y = top_left_y + self.HEIGHT - section_height
        bottom_section = pygame.Rect(top_left_x, bottom_section_top_left_y,
                                     self.WIDTH, section_height)
        if bottom_section.colliderect(ball_rect):
            angle_modifier = radians(self.ANGLE_MODIFIER)
            if self.side_of_board == LeftOrRight.RIGHT:
                angle_modifier *= -1
            return True, angle_modifier

        middle_section = pygame.Rect(top_left_x, top_left_y + section_height,
                                     self.WIDTH, section_height)
        if middle_section.colliderect(ball_rect):
            return True, 0

        return False, None


class AIBat(Bat):
    """
    A bat which is not human-controlled but rather controlled by artificial intelligence.
    """
    _SERVE_RATE = 0.01
    _SERVING_DIRECTION_CHANGE_RATE = 0.05

    def __init__(self, up_key, down_key, serve_key, board_width, board_height, is_right_hand_bat=False):
        super(AIBat, self).__init__(up_key, down_key, serve_key, board_width, board_height,
                                    is_right_hand_bat=False)
        self._last_move_direction = None

    def move(self, ball_y, serving=False):
        """
        Given the y coordinate of the ball, move the bat.
        """
        if not serving:
            if self._y_coord < ball_y:
                self.move_down()
            elif self._y_coord > ball_y:
                self.move_up()
        else:
            change_direction = random.random() < self._SERVING_DIRECTION_CHANGE_RATE
            if change_direction and self._last_move_direction == UpOrDown.UP:
                self._last_move_direction = UpOrDown.DOWN
                self.move_down()
            elif change_direction and self._last_move_direction == UpOrDown.DOWN:
                self._last_move_direction = UpOrDown.UP
                self.move_up()
            elif self._last_move_direction == UpOrDown.UP:
                self.move_up()
            else:
                self.move_down()

    def serve(self, ball_y):
        """
        Serving behaviour
        """
        is_serve = random.random() < self._SERVE_RATE
        if is_serve:
            if self._last_move_direction == UpOrDown.UP:
                ball_angle = math.radians(self.SERVE_ANGLE_MODIFIER)
            else:
                ball_angle = math.radians(-self.SERVE_ANGLE_MODIFIER)
            return True, ball_angle

        else:
            self.move(ball_y, serving=True)
            return False, None

    def move_down(self):
        super(AIBat, self).move_down()
        self._last_move_direction = UpOrDown.DOWN
        if self._y_coord == self._maximum_y:
            self._last_move_direction = UpOrDown.UP

    def move_up(self):
        super(AIBat, self).move_up()
        self._last_move_direction = UpOrDown.UP
        if self._y_coord == 0:
            self._last_move_direction = UpOrDown.DOWN

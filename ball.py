"""
The ball in ojrtennis
"""
import random
import math
import pygame
from utilities import LeftOrRight

class Ball:
    """
    Represents the ball in ojrtennis. The ball has x and y coordinates,
    speed and direction.
    """

    RADIUS = 3
    COLOUR = (255, 255, 255)
    _ACCEL_RATE = 1
    _MAX_ANGLE = math.radians(20)

    def __init__(self, start_x, start_y):
        self.x_coord = round(start_x)
        self.y_coord = round(start_y)

        self._direction = self._get_random_start_direction()
        # Radians anticlockwise from x axis

        self._speed = 3

        self._surf = None # Set upon first draw

    def move(self):
        """
        Move the ball in the direction it is travelling.
        """
        x_movement = self._speed * math.cos(self._direction)
        y_movement = self._speed * math.sin(self._direction)
        self.x_coord += round(x_movement)
        self.y_coord += round(y_movement)

    def draw(self, surface):
        """
        Draw the ball on the surface.
        """
        ball_pos = (self.x_coord, self.y_coord)
        self._surf = pygame.draw.circle(surface, self.COLOUR, ball_pos,
                                        self.RADIUS)

    @staticmethod
    def _get_random_start_direction():
        """
        Return a random direction to start the ball moving.
        The value will be in the range of +- 30 degrees from the x
        axis in either direction but the return balue will be in
        radians.
        """
        random_direction = random.random() * 30
        random_direction *= random.choice([1, -1])

        if random.choice([1, 2]) == 2:
            random_direction += 180

        return math.radians(random_direction)

    def test_collision_with_bat(self, bat):
        """
        Test for a collision with the bat. Handle the change
        to the ball's direction accordingly.

        In order to prevent the ball going through the bat, the maximum speed
        is the same number of pixels as the bat width.
        """
        collision, angle_modifier = bat.test_collision_with_ball(self._surf)

        if collision:
            if self._x_direction() == bat.side_of_board:
                self._direction = math.pi - self._direction
                self._direction += angle_modifier

                self._limit_angle(bat.side_of_board)

                self._speed += self._ACCEL_RATE
                if self._speed > bat.WIDTH:
                    self._speed = bat.WIDTH

    def _x_direction(self):
        """
        Return LeftOrRight.RIGHT if the ball is heading in a right-bound direction i.e. its x-axis
        direction is positive. Return LeftOrRight.LEFT otherwise
        """
        if math.cos(self._direction) > 0:
            return LeftOrRight.RIGHT
        return LeftOrRight.LEFT

    def test_collision_with_game_edge(self, board_surf):
        """
        Test for collisions with a vertical edge of the game board.
        If colliding with the top or bottom bounce.
        """
        board_height = board_surf.get_height()
        if self.y_coord <= 0 or self.y_coord >= board_height:
            self._direction *= -1

    def test_point_scored(self, board_surf):
        """
        Test for the ball colliding with either horizontal edge of the game
        board. Return a tuple of (is_score, scorer) where is_score will be True if
        a point is scored, False otherwise and scorer will be LeftOrRight.LEFT or
        LeftOrRight.RIGHT depending on who scored, None if not a score.
        """
        board_width = board_surf.get_width()
        if self.x_coord < 0:
            return True, LeftOrRight.RIGHT
        if self.x_coord > board_width:
            return True, LeftOrRight.LEFT
        return False, None

    def _limit_angle(self, side_of_board):
        """
        Limit the angle of the ball so that it doesn't start travelling too up & down
        or passes through the bat because the angle_modifier sends it that direction.
        """
        # 2 pi is a complete circle. Save memory thus (and simplify calculations):
        self._direction = self._direction % (2 * math.pi)
        if side_of_board == LeftOrRight.RIGHT:
            if self._direction < math.pi - math.radians(self._MAX_ANGLE):
                self._direction = math.pi - self._MAX_ANGLE
            elif self._direction > math.pi + math.radians(self._MAX_ANGLE):
                self._direction = math.pi + self._MAX_ANGLE
        else:
            if self._direction > math.radians(self._MAX_ANGLE) and \
                   self._direction < math.pi:
                self._direction = self._MAX_ANGLE
            elif self._direction < 2 * math.pi - math.radians(self._MAX_ANGLE) \
                    and self._direction > math.pi:
                self._direction = 2 * math.pi - self._MAX_ANGLE

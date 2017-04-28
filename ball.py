"""
The ball in ojrtennis
"""
import random
from math import sin, cos, radians

class Ball:
    """
    Represents the ball in ojrtennis. The ball has x and y coordinates,
    speed and direction.
    """

    RADIUS = 3
    COLOUR = (255, 255, 255)
    
    def __init__(self, start_x, start_y):
        self.x_coord = round(start_x)
        self.y_coord = round(start_y)

        self._direction = self._get_random_start_direction()
        # Radians anticlockwise from x axis

        self._speed = 5

    def move(self):
        """
        Move the ball in the direction it is travelling.
        """
        x_movement = self._speed * cos(self._direction)
        y_movement = self._speed * sin(self._direction)
        self.x_coord += round(x_movement)
        self.y_coord += round(y_movement)
        

    def _get_random_start_direction(self):
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

        return radians(random_direction)
        

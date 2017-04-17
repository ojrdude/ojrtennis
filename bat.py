"""
Bat code for ojrtennis
"""

class Bat:
    """
    A Bat in the ojrtennis game that can be controlled by the player
    """
    
    WIDTH = 20
    HEIGHT = 70
    COLOUR = (255, 255, 255)

    def __init__(self, up_key, down_key, board_height):
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

    @property
    def y_coord(self):
        """
        Get the current Y Coordinate of the Bat
        """
        return self._y_coord

    @y_coord.setter
    def y_coord(self, y):
        """
        Set the current Y Coordinate of the Bat
        """
        assert y <= self._maximum_y, "Setting y_coord outside maximum"
        self._y_coord = y
        

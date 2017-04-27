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
        if self.y_coord - 5 >= 0:
            self.y_coord -= 5
        else: # Don't go off screen.
            self.y_coord = 0
        
    def move_down(self):
        """
        Move the bat down. This should be called when the player has pressed
        the button to move the bat downwards.
        """
        if self.y_coord + 5 <= self._maximum_y:
            self.y_coord += 5
        else: # Don't go off screen
            self.y_coord = self._maximum_y

"""
ojrtennis scoring module.
"""

import logging
import pygame.font
from utilities import LeftOrRight

class Score:
    """
    Keeps track of the game score.
    """

    pygame.font.init()
    _FONT_SIZE = 50
    _FONT = pygame.font.Font('freesansbold.ttf', _FONT_SIZE)
    _COLOUR = (255, 255, 255)

    def __init__(self):
        self._left_score = 0
        self._right_score = 0
        self._logger = logging.getLogger(__name__)

    def draw(self, display_surf):
        """
        Draw the current score onto the display surface.
        """
        left_score_text = self._FONT.render(str(self._left_score), True, self._COLOUR)
        right_score_text = self._FONT.render(str(self._right_score), True,
                                             self._COLOUR)

        x_margin = 130
        y_margin = 100
        display_surf.blit(left_score_text, (x_margin, y_margin))
        right_x_margin = display_surf.get_width() - x_margin - self._FONT_SIZE
        display_surf.blit(right_score_text, (right_x_margin, y_margin))

    def point_scored(self, scored_by):
        """
        Increment the score of whoever scored. scored_by should be either
        LeftOrRight.LEFT or LeftOrRight.RIGHT.
        """
        assert isinstance(scored_by, LeftOrRight)

        if scored_by == LeftOrRight.LEFT:
            self._left_score += 1
            self._logger.info('Point scored by left bat. Score: %d', self._left_score)
        else:
            self._right_score += 1
            self._logger.info('Point scored by right bat. Score: %d', self._right_score)

    @property
    def score(self):
        """
        Return the score as a tuple of (left_score, right_score)
        """
        return (self._left_score, self._right_score)

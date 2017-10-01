"""
Main game screen module of ojrtennis.
"""

import pygame
import pygame.locals as pgLocals

from bat import Bat
from ball import Ball
from score import Score
from screens.abstractscreen import AbstractScreen

class Game(AbstractScreen):
    """
    Orchestrates the running of the main game screen with the bats and the balls.
    """
    _FPS = 50

    _BG_COLOUR = (0, 0, 0)

    _POINTS_TO_WIN = 5

    _FONT_SIZE = 50
    _FONT = pygame.font.Font('freesansbold.ttf', _FONT_SIZE)
    _TEXT_COLOUR = (255, 255, 255)
    _PLAY_AGAIN_LINE_1_LOCATION = (200, 200)
    _PLAY_AGAIN_LINE_2_LOCATION = (200, 200 + 1.1 * _FONT_SIZE)
    _VICTORY_TEXT_LOCATION = (200, 200)

    def __init__(self, display_surface):
        super(Game, self).__init__(display_surface)

        self._ball = None
        self._bat_1 = None
        self._bat_2 = None
        self._reset_game()

    def main_game_loop(self):
        """
        The main game-playing loop.
        """
        while True:
            self._check_for_quit()
            self._display_surf.fill(self._BG_COLOUR)
            self._do_all_movements()
            self._draw()
            self._test_collisions()
            self._test_point_scored()

            is_game_over = self._test_victory()
            if is_game_over:
                return

            pygame.display.update()
            self._fps_clock.tick(self._FPS)

    def _handle_bat_movement(self):
        """
        Check if the players are pressing the buttons to move the bats and
        move accordingly.
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[self._bat_1.up_key]:
            self._bat_1.move_up()
        if pressed_keys[self._bat_1.down_key]:
            self._bat_1.move_down()
        if pressed_keys[self._bat_2.up_key]:
            self._bat_2.move_up()
        if pressed_keys[self._bat_2.down_key]:
            self._bat_2.move_down()

    def _draw(self):
        """
        Draw the game in its current state.
        """
        self._bat_1.draw(self._display_surf)
        self._bat_2.draw(self._display_surf)
        self._ball.draw(self._display_surf)
        self._score.draw(self._display_surf)

    def _do_all_movements(self):
        """
        Work out all the movements that have occurred this cycle.
        """
        self._handle_bat_movement()
        self._ball.move()

    def _test_collisions(self):
        """
        Test for the occurrence of any collisions in the game. E.g. bat and ball
        or ball with edge of board.
        """
        self._ball.test_collision_with_bat(self._bat_1)
        self._ball.test_collision_with_bat(self._bat_2)
        self._ball.test_collision_with_game_edge(self._display_surf)

    def _test_point_scored(self):
        """
        Test for the ball going off either horizontal edge of the screen.
        If so, update score and reset the ball.
        """
        is_score, who_scored = self._ball.test_point_scored(self._display_surf)
        if is_score:
            self._score.point_scored(who_scored)
            self._reset_ball()

    def _reset_ball(self):
        """
        Get a new ball and put it in the middle of the board.
        """
        ball_x = self._display_surf.get_width() / 2
        ball_y = self._display_surf.get_height() / 2
        self._ball = Ball(ball_x, ball_y)

    def _test_victory(self):
        """
        Test for a player having won. If somebody has won, display the result,
        pause the game for a few seconds and then wait for a key input before
        starting a new game.
        """
        left_score, right_score = self._score.score
        if left_score == self._POINTS_TO_WIN:
            self._logger.info(f'Left Wins with score: {left_score}')
            victory_text = self._FONT.render('Left Wins!', True, self._TEXT_COLOUR)
        elif right_score == self._POINTS_TO_WIN:
            self._logger.info(f'Right Wins with score: {right_score}')
            victory_text = self._FONT.render('Right Wins!', True, self._TEXT_COLOUR)
        else:
            return False

        self._display_surf.blit(victory_text, self._VICTORY_TEXT_LOCATION)

        # Display the victory message for a few seconds before returning.
        pygame.display.update()
        pygame.time.delay(3 * 1000)

        return True

    def _reset_game(self):
        """
        Reset the game. Set the scores to 0 and re-centre the bats and the ball.
        """
        self._logger.info('Resetting game. '
                          'The bats are recentred a new ball created.')
        self._bat_1 = Bat(pgLocals.K_w, pgLocals.K_s,
                          self._display_surf.get_width(),
                          self._display_surf.get_height())
        self._bat_2 = Bat(pgLocals.K_UP, pgLocals.K_DOWN,
                          self._display_surf.get_width(),
                          self._display_surf.get_height(),
                          is_right_hand_bat=True)

        self._reset_ball()

        self._score = Score()

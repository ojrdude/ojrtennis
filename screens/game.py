"""
Main game screen module of ojrtennis.
"""


import math

import pygame

from ball import Ball
from ball import BallState
from bat import Bat
from score import Score
from screens.abstractscreen import AbstractScreen
from utilities import LeftOrRight


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
        self._serving_bat = None
        self._reset_game()

    def main_screen_loop(self):
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
        Check if the players are pressing the buttons to move the bats and move accordingly. Also handle serving if
        the ball is being served.
        """
        pressed_keys = pygame.key.get_pressed()

        def both_pressed_or_unpressed(button1, button2):
            "Return True if both buttons are pressed, or both are unpressed. Return False otherwise"
            return pressed_keys[button1] == pressed_keys[button2]

        angle_modifier = self._bat_1.SERVE_ANGLE_MODIFIER
        if both_pressed_or_unpressed(self._bat_1.up_key, self._bat_1.down_key):
            self._handle_serve(self._bat_1, 0, pressed_keys)
        elif pressed_keys[self._bat_1.up_key]:
            self._bat_1.move_up()
            self._handle_serve(self._bat_1, math.radians(-angle_modifier), pressed_keys)
        elif pressed_keys[self._bat_1.down_key]:
            self._bat_1.move_down()
            self._handle_serve(self._bat_1, math.radians(angle_modifier), pressed_keys)

        if both_pressed_or_unpressed(self._bat_2.up_key, self._bat_2.down_key):
            self._handle_serve(self._bat_2, math.pi, pressed_keys)
        elif pressed_keys[self._bat_2.up_key]:
            self._bat_2.move_up()
            self._handle_serve(self._bat_2, math.radians(angle_modifier) + math.pi, pressed_keys)
        elif pressed_keys[self._bat_2.down_key]:
            self._bat_2.move_down()
            self._handle_serve(self._bat_2, math.radians(-angle_modifier) + math.pi, pressed_keys)

    def _handle_serve(self, bat, ball_angle, pressed_keys):
        """
        Handle the serve if the ball is waiting to be served and the player has pressed the serve button.
        """
        is_serving_bat = bat is self._serving_bat
        if not self._ball.is_being_served or not is_serving_bat:
            self._logger.debug(f'Not serving because is_being_served={self._ball.is_being_served} or because '
                               f'is_serving_bat={is_serving_bat}')
            return

        if pressed_keys[bat.serve_key]:
            self._logger.info(f'Ball served by bat={bat.side_of_board} with ball_angle={ball_angle}')
            self._ball.start_moving(ball_angle)

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
        self._handle_ball_movement()

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
            serving = LeftOrRight.LEFT if who_scored == LeftOrRight.RIGHT else LeftOrRight.RIGHT
            self._start_new_point(serving)

    def _reset_ball(self):
        """
        Get a new ball and put it in the middle of the board.
        """
        ball_x = self._display_surf.get_width() // 2
        ball_y = self._display_surf.get_height() // 2
        self._ball = Ball(ball_x, ball_y, start_state=BallState.MOVING)

    def _test_victory(self):
        """
        Test for a player having won. If somebody has won, display the result,
        pause the game for a few seconds and then wait for a key input before
        starting a new game.
        """
        left_score, right_score = self._score.score
        if left_score == self._POINTS_TO_WIN:
            self._logger.info(f'Left Wins with score: {left_score}')
            victory_text = self._FONT.render(
                'Left Wins!', True, self._TEXT_COLOUR)
        elif right_score == self._POINTS_TO_WIN:
            self._logger.info(f'Right Wins with score: {right_score}')
            victory_text = self._FONT.render(
                'Right Wins!', True, self._TEXT_COLOUR)
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
                          'The bats are recentred a new ball created in the middle of the screen.')
        self._bat_1 = Bat(pygame.locals.K_w, pygame.locals.K_s, pygame.locals.K_SPACE,
                          self._display_surf.get_width(), self._display_surf.get_height())
        self._bat_2 = Bat(pygame.locals.K_UP, pygame.locals.K_DOWN, pygame.locals.K_RCTRL,
                          self._display_surf.get_width(), self._display_surf.get_height(),
                          is_right_hand_bat=True)

        self._reset_ball()

        self._score = Score()

    def _start_new_point(self, serving):
        """
        After a point has been scored, redraw the bats with the ball stuck to the bat of
        the player that just conceded.
        """
        assert isinstance(serving, LeftOrRight)

        self._logger.info('Starting new point. '
                          f'The bats are recentred and the ball is drawn on the loser={serving} bat')

        self._bat_1 = Bat(pygame.locals.K_w, pygame.locals.K_s, pygame.locals.K_SPACE,
                          self._display_surf.get_width(), self._display_surf.get_height())
        self._bat_2 = Bat(pygame.locals.K_UP, pygame.locals.K_DOWN, pygame.locals.K_RCTRL,
                          self._display_surf.get_width(), self._display_surf.get_height(),
                          is_right_hand_bat=True)

        if serving == LeftOrRight.LEFT:
            self._serving_bat = self._bat_1
        else:
            self._serving_bat = self._bat_2

        bat_x, bat_y = self._serving_bat.front_centre
        self._ball = Ball(bat_x, bat_y, start_state=BallState.SERVING)

    def _handle_ball_movement(self):
        """
        Move the ball. If the ball is being served, keep it attached to the front of the bat that is serving.
        If the ball is not being served, defer to the ball's own move logic.
        """
        if self._ball.is_moving:
            self._ball.move()
        else:
            self._ball.x_coord, self._ball.y_coord = self._serving_bat.front_centre

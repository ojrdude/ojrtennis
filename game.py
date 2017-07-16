"""
Base game module of ojrtennis.
"""
import pygame
import sys
from pygame.locals import *
from bat import Bat
from ball import Ball
from score import Score

class Game:

    _WINDOW_WIDTH = 640
    _WINDOW_HEIGHT = 480
    _FPS = 25

    _BG_COLOUR = (0, 0, 0)

    def __init__(self):
        self._display_surf = pygame.display.set_mode((self._WINDOW_WIDTH,
                                                      self._WINDOW_HEIGHT))
        self._fps_clock = pygame.time.Clock()
        
        self._bat_1 = Bat(K_w, K_s, self._WINDOW_HEIGHT)
        self._bat_1.x_coord = 3 + self._bat_1.WIDTH / 2
        self._bat_1.y_coord = self._WINDOW_HEIGHT / 2
        
        self._bat_2 = Bat(K_UP, K_DOWN, self._WINDOW_HEIGHT, is_right_hand_bat=True)
        self._bat_2.x_coord = self._WINDOW_WIDTH - 3 - self._bat_2.WIDTH / 2
        self._bat_2.y_coord = self._WINDOW_HEIGHT / 2

        ball_x = self._WINDOW_WIDTH / 2
        ball_y = self._WINDOW_HEIGHT / 2
        self._ball = Ball(ball_x, ball_y)

        self._score = Score()
        
    def main(self):
        """
        Main entry point for game
        """
        pygame.init()
        self._main_game_loop()

    def _main_game_loop(self):
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
            pygame.display.update()
            self._fps_clock.tick(self._FPS)

    def _check_for_quit(self):
        """
        Check if the user wants to quit.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

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
        ball_x = self._WINDOW_WIDTH / 2
        ball_y = self._WINDOW_HEIGHT / 2
        self._ball = Ball(ball_x, ball_y)
        

if __name__ == '__main__':
    game = Game()
    game.main()

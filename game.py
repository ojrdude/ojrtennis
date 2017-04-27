"""
Base game module of ojrtennis
"""
import pygame
import sys
from pygame.locals import *
from bat import Bat

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
        self._bat_2 = Bat(K_UP, K_DOWN, self._WINDOW_HEIGHT)
        self._bat_2.x_coord = self._WINDOW_WIDTH - 3 - self._bat_2.WIDTH / 2
        self._bat_2.y_coord = self._WINDOW_HEIGHT / 2
        

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
            self._handle_bat_movement()
            self._draw_bat(self._bat_1)
            self._draw_bat(self._bat_2)
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

    def _draw_bat(self, bat):
        """
        Draw the bat in its current position on the display surface
        """
        top_left_x, top_left_y = bat.top_left
        bat_rect = pygame.Rect(top_left_x, top_left_y, bat.WIDTH, bat.HEIGHT)
        pygame.draw.rect(self._display_surf, bat.COLOUR, bat_rect)

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
            
                           
       
if __name__ == '__main__':
    game = Game()
    game.main()

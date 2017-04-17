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
    _BOARD_WIDTH = 160 # Cells not pixels
    _BOARD_HEIGHT = 160 # Cells not pixels
    assert _WINDOW_WIDTH % _BOARD_WIDTH == 0, 'Board width not factor of '
    'window width'
    assert _WINDOW_HEIGHT % _BOARD_HEIGHT == 0, 'Board height not factor of '
    'window height'

    _BG_COLOUR = (0, 0, 0)

    def __init__(self):
        self._display_surf = pygame.display.set_mode((self._WINDOW_WIDTH,
                                                      self._WINDOW_HEIGHT))
        self._fps_clock = pygame.time.Clock()
        self._bat_1 = Bat(K_w, K_s, self._BOARD_HEIGHT)
        self._bat_1.x_coord = 3
        self._bat_1.y_coord = self._BOARD_HEIGHT / 2
        self._bat_2 = Bat(K_UP, K_DOWN, self._BOARD_HEIGHT)
        self._bat_2.x_coord = self._BOARD_WIDTH - 3
        self._bat_2.y_coord = self._BOARD_HEIGHT / 2
        

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
            else:
                pygame.event.post(event)

    def _draw_bat(self, bat):
        """
        Draw the bat in its current position on the display surface
        """
        bat_x_pixel = self._get_pixel_for_x_coord(bat.x_coord)
        bat_y_pixel = self._get_pixel_for_y_coord(bat.y_coord)
        bat_rect = pygame.Rect(bat_x_pixel, bat_y_pixel, bat.WIDTH, bat.HEIGHT)
        pygame.draw.rect(self._display_surf, bat.COLOUR, bat_rect)
        
    def _get_pixel_for_x_coord(self, x_coord):
        """
        Return the pixel number for the given x coordinate.
        """
        pixels_per_coord = self._WINDOW_WIDTH / self._BOARD_WIDTH
        return pixels_per_coord * x_coord

    def _get_pixel_for_y_coord(self, y_coord):
        """
        Return the pixel number for the given y coordinate.
        """
        pixels_per_coord = self._WINDOW_HEIGHT / self._BOARD_HEIGHT
        return pixels_per_coord * y_coord
    
if __name__ == '__main__':
    game = Game()
    game.main()

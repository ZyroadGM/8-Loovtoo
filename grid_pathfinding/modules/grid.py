import pygame

pygame.init()
from .tile import tile
from .constants import *


class grid:
    def __init__(self, density, tile_color=BLACK, tile_border_size=1, tile_transparency=50):
        self.density = density  # amount of tiles in 100px line
        self.rows = 0
        self.colons = 0
        self.matrix = [[]]
        self.tile_diameter = 0
        self.tile_transparency = tile_transparency
        self.tile_color = (tile_color[0], tile_color[1], tile_color[2], self.tile_transparency)
        self.tile_border_size = tile_border_size

    def find_boundaries(self, window):
        win_width, win_height = window.get_width(), window.get_height()
        self.colons = int(win_width / 100 * self.density)
        self.tile_diameter = int(win_width / self.colons)
        self.rows = win_height // self.tile_diameter

    def create_grid(self):
        self.matrix = [[tile(x * self.tile_diameter, y * self.tile_diameter, self.tile_diameter)
                 for x in range(self.colons)] for y in range(self.rows)]

    def make_not_obstacle_neutral(self):
        for list in self.matrix:
            for tile in list:
                if not any([tile.is_obstacle(), tile.is_end(), tile.is_start()]):
                    tile.make_neutral()

    def draw_grid(self, window):
        surface = window.convert_alpha()
        surface.fill([0, 0, 0, 0])
        for y, list in enumerate(self.matrix):
            for x, tile in enumerate(list):
                tile.draw(surface)
                pygame.draw.line(surface, self.tile_color, (x*self.tile_diameter, 0), (x*self.tile_diameter, window.get_height()), self.tile_border_size)
            pygame.draw.line(surface, self.tile_color, (0, y * self.tile_diameter),
                             (window.get_width(), y * self.tile_diameter), self.tile_border_size)
        window.blit(surface, (0, 0))



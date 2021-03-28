import pygame
pygame.init()
from .constants import *
import math
import random
class tile:
    def __init__(self, x, y, diameter):
        self.x, self.y, self.diameter = x, y, diameter
        self.rect = pygame.Rect(self.x, self.y, self.diameter, self.diameter)
        self.colon, self.row = math.floor(self.x/self.diameter), math.floor(self.y/self.diameter)
        """STATES"""
        self.neighbors = {}
        self.g_value = 0
        self.color = WHITE
        self.texture = None
        self.texture_rotation = 90*random.randint(1, 4)
        self.transparency = 150

    def draw(self, window):
        if self.texture is None:
            pygame.draw.rect(window, (self.color[0], self.color[1], self.color[2], self.transparency)
            if len(self.color) < 4 else (self.color[0], self.color[1], self.color[2], self.color[3]), self.rect)
        else:

            window.blit(pygame.transform.scale(self.texture,
                                               (self.diameter, self.diameter)), (self.x, self.y))

    """INFO"""
    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == RED

    def is_obstacle(self):
        return self.color == GRAY or self.color == LIGHT_GRAY

    def is_closed(self):
        return self.color == YELLOW

    def is_neutral(self):
        return self.color == WHITE

    def get_pos(self):
        return self.rect.x, self.rect.y
    """EEEEEEEE"""
    def get_colon_row(self):
        return self.colon, self.row

    def make_neutral(self):
        self.color = WHITE
        self.texture = None

    def make_start(self):
        self.color = BLUE
        self.texture = WAYPOINT_GREEN

    def make_end(self):
        self.color = RED
        self.texture = WAYPOINT_RED

    def make_obstacle(self):
        self.color = GRAY
        self.texture = pygame.transform.rotate(OBSTACLE, self.texture_rotation)

    def make_invisible_obstacle(self):
        self.color = LIGHT_GRAY
        self.texture = None

    def make_path(self):
        self.color = MAGENTA
        self.texture = None

    def make_open(self):
        self.color = GREEN
        self.texture = None

    def make_closed(self):
        self.color = ORANGE
        self.texture = None

    def add_invisible_obstacles(self, grid):
        self.neighbors = {}
        if self.row > 0 and self.colon > 0 and \
                grid.matrix[self.row - 1][self.colon - 1].is_neutral():  # UP/LEFT
            grid.matrix[self.row - 1][self.colon - 1].make_invisible_obstacle()

        if self.row > 0 and self.colon < grid.colons - 1 and \
                grid.matrix[self.row - 1][self.colon + 1].is_neutral():  # UP/RIGHT
            grid.matrix[self.row - 1][self.colon + 1].make_invisible_obstacle()

        if self.row < grid.rows - 1 and self.colon > 0 and \
                grid.matrix[self.row + 1][self.colon - 1].is_neutral():  # DOWN/LEFT
            grid.matrix[self.row + 1][self.colon - 1].make_invisible_obstacle()

        if self.row < grid.rows - 1 and self.colon < grid.colons - 1 and \
                grid.matrix[self.row + 1][self.colon + 1].is_neutral():  # DOWN/RIGHT
            grid.matrix[self.row + 1][self.colon + 1].make_invisible_obstacle()

        if self.row < grid.rows - 1 and\
                grid.matrix[self.row + 1][self.colon].is_neutral():  # DOWN
            grid.matrix[self.row + 1][self.colon].make_invisible_obstacle()

        if self.row > 0 and\
                grid.matrix[self.row - 1][self.colon].is_neutral():  # UP
            grid.matrix[self.row - 1][self.colon].make_invisible_obstacle()

        if self.colon < grid.colons - 1 and\
                grid.matrix[self.row][self.colon + 1].is_neutral():  # RIGHT
            grid.matrix[self.row][self.colon + 1].make_invisible_obstacle()

        if self.colon > 0 and\
                grid.matrix[self.row][self.colon - 1].is_neutral():  # LEFT
            grid.matrix[self.row][self.colon - 1].make_invisible_obstacle()

    def get_neighbors(self, grid):
        if self.row > 0 and self.colon > 0 and\
                not grid.matrix[self.row - 1][self.colon - 1].is_obstacle():  # UP/LEFT
            self.neighbors.update({grid.matrix[self.row - 1][self.colon - 1]: '↖'})

        if self.row > 0 and self.colon < grid.colons - 1 and\
                not grid.matrix[self.row - 1][self.colon + 1].is_obstacle():  # UP/RIGHT
            self.neighbors.update({grid.matrix[self.row - 1][self.colon + 1]: '↗'})

        if self.row < grid.rows - 1 and self.colon > 0 and\
                not grid.matrix[self.row + 1][self.colon - 1].is_obstacle():  # DOWN/LEFT
            self.neighbors.update({grid.matrix[self.row + 1][self.colon - 1]: '↙'})

        if self.row < grid.rows - 1 and self.colon < grid.colons - 1 and\
                not grid.matrix[self.row + 1][self.colon + 1].is_obstacle():  # DOWN/RIGHT
            self.neighbors.update({grid.matrix[self.row + 1][self.colon + 1]: '↘'})

        if self.row < grid.rows - 1 and not grid.matrix[self.row + 1][self.colon].is_obstacle():  # DOWN
            self.neighbors.update({grid.matrix[self.row + 1][self.colon]: '↓'})

        if self.row > 0 and not grid.matrix[self.row - 1][self.colon].is_obstacle():  # UP
            self.neighbors.update({grid.matrix[self.row - 1][self.colon]: '↑'})

        if self.colon < grid.colons - 1 and not grid.matrix[self.row][self.colon + 1].is_obstacle():  # RIGHT
            self.neighbors.update({grid.matrix[self.row][self.colon + 1]: '→'})

        if self.colon > 0 and not grid.matrix[self.row][self.colon - 1].is_obstacle():  # LEFT
            self.neighbors.update({grid.matrix[self.row][self.colon - 1]: '←'})
        return self.neighbors









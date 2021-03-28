import pygame
pygame.init()
import queue
import math
from .tile import tile
from .constants import *
import asyncio

class algorithm:
    def __init__(self):
        self.start_x, self.start_y = None, None

    def intelligize_start(self, start, grid):
        self.start_x, self.start_y = start.get_pos()[0] // grid.tile_diameter, \
               start.get_pos()[1] // grid.tile_diameter

    def is_valid(self, grid, path):
        x, y = self.start_x, self.start_y
        for index, action in enumerate(path):
            if action == '←':
                x -= 1
            elif action == '→':
                x += 1
            elif action == '↑':
                y -= 1
            elif action == '↓':
                y += 1
            elif action == '↖':
                x -= 1
                y -= 1
            elif action == '↙':
                x -= 1
                y += 1
            elif action == '↗':
                x += 1
                y -= 1
            elif action == '↘':
                x += 1
                y += 1
            if not (0 <= x < len(grid.matrix[0]) and 0 <= y < len(grid.matrix)):
                return False
            if action == '→' and index != 0:
                if path[index - 1] == '←':
                    return False
            if action == '←' and index != 0:
                if path[index - 1] == '→':
                    return False
            if action == '↑' and index != 0:
                if path[index - 1] == '↓':
                    return False
            if action == '↓' and index != 0:
                if path[index - 1] == '↑':
                    return False
            elif grid.matrix[y][x].is_obstacle() is True:
                return False
        return True

    def is_finished(self, grid, path):
        x, y = self.start_x, self.start_y
        for number_of_actions, action in enumerate(path):
            if action == '←':
                x -= 1
            elif action == '→':
                x += 1
            elif action == '↑':
                y -= 1
            elif action == '↓':
                y += 1
            if grid.matrix[y][x].is_end() is True:
                print('Moves = {}'.format(number_of_actions))
                return True
        return False

    def get_route(self, grid):
        paths = queue.Queue()
        paths.put('')
        path = ''
        while not (self.is_finished(grid, path)):
            path = paths.get()
            for possibility in ['←', '→', '↑', '↓', '↖', '↙', '↗', '↘']:
                possibility = path + possibility
                if self.is_valid(grid, possibility):
                    paths.put(possibility)
        self.draw(grid, path)

    def draw(self, grid, path):
        x, y = self.start_x, self.start_y
        for action in path[:-1]:
            if action == '←':
                x -= 1
            elif action == '→':
                x += 1
            elif action == '↑':
                y -= 1
            elif action == '↓':
                y += 1
            grid.matrix[y][x].make_path()



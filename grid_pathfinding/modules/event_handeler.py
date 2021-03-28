import pygame
pygame.init()
import math


class event_handeler:
    def __init__(self, **mapped_keys):
        self.running = True
        self.pathfinding = False
        self.calculating = False
        self.mapped_keys = mapped_keys
        self.start = None
        self.end = None
        self.start_update = ()

    def calculate(self, grid, algorithm):
        self.calculating = True
        grid.make_not_obstacle_neutral()
        algorithm.calculate(grid, self.start, self.end)

    def handle_event(self, grid=None, algorithm=None):
        if algorithm is not None and grid is not None:
            if self.calculating:
                if self.start is not None and self.end is not None:
                    self.calculate(grid, algorithm)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.pathfinding = True
                if event.key == pygame.K_d:
                    self.pathfinding = False
                if algorithm is not None and grid is not None:
                    if event.key == pygame.K_c:
                        grid.create_grid()
                        self.start = None
                        self.end = None
                    elif event.key == pygame.K_SPACE:
                        if self.start is not None and self.end is not None:
                            self.calculate(grid, algorithm)
            if self.pathfinding:
                new_start = self.start_update
                if new_start:
                    if grid is not None and self.start is not None:
                        grid.make_not_obstacle_neutral()
                        x, y = math.floor(new_start[0]/grid.tile_diameter), math.floor(new_start[1]/grid.tile_diameter)
                        tile = grid.matrix[y][x]
                        self.start.make_neutral()
                        self.start = tile
                        tile.make_start()
                    self.start_update = ()
                elif pygame.mouse.get_pressed(3)[0]:
                    if grid is not None:
                        try:
                            x, y = math.floor(event.pos[0]/grid.tile_diameter), math.floor(event.pos[1]/grid.tile_diameter)
                            tile = grid.matrix[y][x]
                            if self.start is None:
                                self.start = tile
                                tile.make_start()
                            elif self.end is None and tile != self.start:
                                self.end = tile
                                tile.make_end()
                            elif tile != self.start and tile != self.end:
                                tile.make_obstacle()
                                tile.add_invisible_obstacles(grid)
                        except:
                            print('Mouse out of range')

                elif pygame.mouse.get_pressed(5)[2]:
                    try:
                        x, y = math.floor(event.pos[0] / grid.tile_diameter), math.floor(event.pos[1] / grid.tile_diameter)
                        tile = grid.matrix[y][x]
                        if tile == self.start:
                            self.start = None
                            tile.make_neutral()
                        elif tile == self.end:
                            self.end = None
                            tile.make_neutral()
                        elif tile != self.start and tile != self.end:
                            tile.make_neutral()
                    except:
                        print('Mouse out of range')
                if self.end is None:
                    self.calculating = False
                if self.end is None:
                    grid.make_not_obstacle_neutral()

    def make_start_update(self, x, y):
        self.start_update = (x, y)

    def is_running(self):
        return self.running

    def is_pathfinding(self):
        return self.pathfinding

    def is_calculating(self):
        return self.calculating

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end



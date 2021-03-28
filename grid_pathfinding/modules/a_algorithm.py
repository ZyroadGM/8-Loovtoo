import pygame
pygame.init()
import queue
import math


class algorithm:
    def __init__(self, turning_weight):
        self.turning_weight = turning_weight
        self.corners = []

    def update(self, grid):
        for list in grid.matrix:
            for element in list:
                element.update_neighbors(grid)

    def get_corners(self):
        corners = self.corners
        self.corners = []
        return corners

    @staticmethod
    def distance_between_2points(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x1 - x2) ** 2
                         + (y1 - y2) ** 2)

    @staticmethod
    def reconstruct_path(grid, came_from, current, start, end):
        rotations = []
        while current in came_from:
            new_current = came_from[current]
            if current != end and new_current != start:
                if new_current.get_neighbors(grid)[current] != \
                        came_from[new_current].get_neighbors(grid)[new_current]:
                    rotations.append(new_current.get_colon_row())
            else:
                rotations.append(current.get_colon_row())

            new_current.make_path()
            current = new_current
        return rotations

    def calculate(self, grid, start, end):
        count = 0
        open_set = queue.PriorityQueue()  # Smallest f_score first
        came_from = {}
        open_set_hash = {start}
        g_score = {spot: float("inf") for row in grid.matrix for spot in row}
        f_score = {spot: float("inf") for row in grid.matrix for spot in row}
        open_set.put((0, count, start))

        g_score[start] = 0
        f_score[start] = self.distance_between_2points(
            (element + grid.tile_diameter / 2 for element in start.get_pos()),
            (element + grid.tile_diameter / 2 for element in end.get_pos()))

        while not open_set.empty():
            current = open_set.get()[2]  # Get first element in queue and assign the tile to current
            open_set_hash.remove(current)

            if current == end:
                self.corners = self.reconstruct_path(grid, came_from, end, start, end)
                end.make_end()
                start.make_start()
                return True

            for neighbor in current.get_neighbors(grid).keys():
                temp_g_score = self.distance_between_2points(
                    (element + grid.tile_diameter / 2 for element in start.get_pos()),
                    (element + grid.tile_diameter / 2 for element in neighbor.get_pos()))
                # Set g_score as distance between start tile and the neighbor
                # print(current.get_neighbors(grid))

                if temp_g_score < g_score[neighbor]:  # if item has not been updated by other current (is neutral)
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score

                    f_score[neighbor] = temp_g_score + \
                                        self.distance_between_2points(
                                            (element + grid.tile_diameter / 2 for element in neighbor.get_pos()),
                                            (element + grid.tile_diameter / 2 for element in end.get_pos()))

                    if current != start and \
                            came_from[current].get_neighbors(grid)[current] != current.get_neighbors(grid)[neighbor]:
                        f_score[neighbor] = temp_g_score + \
                                            self.distance_between_2points(
                                                (element + grid.tile_diameter / 2 for element in neighbor.get_pos()),
                                                (element + grid.tile_diameter / 2 for element in end.get_pos())) + \
                                            10 * self.turning_weight

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            if current != start and not current.is_obstacle():
                current.make_closed()
        return False

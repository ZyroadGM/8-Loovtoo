import pygame
"""
Here in this file are all of the constant variables
"""
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255, 0)
GRAY = (100, 100, 100, 200)
LIGHT_GRAY = (200, 200, 200, 50)
RED = (255, 0, 0, 200)
YELLOW = (255, 255, 0, 50)
ORANGE = (255, 100, 0, 50)
GREEN = (0, 255, 0, 50)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255, 200)
CYAN = (0, 255, 255)
LIGHT_CYAN = (0, 255, 208)

WAYPOINT_GREEN = pygame.image.load(".\grid_pathfinding\sprites\waypoint_green.png")
WAYPOINT_RED = pygame.image.load(".\grid_pathfinding\sprites\waypoint_red.png")
OBSTACLE = pygame.image.load(".\grid_pathfinding\sprites\obstacle.png")
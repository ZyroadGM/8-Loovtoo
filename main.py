import pygame
pygame.init()
import threading
import time

from detection.modules import video
from grid_pathfinding.modules.constants import *
from grid_pathfinding.modules.event_handeler import event_handeler
from grid_pathfinding.modules.grid import grid
from grid_pathfinding.modules import a_algorithm
from detection.modules.video import video
from detection.modules.simple_functions import *


def main():
    pygame.display.set_caption('test')
    events = event_handeler()

    source = video_inputs.webcam_as_input(1)
    dslr = video(source, output_as_pygame, window_name='test3')
    corners = []

    GRID = grid(3)
    A = a_algorithm.algorithm(1)

    threading.Thread(target=dslr.main).start()

    while dslr.get_window_size() is None:
        time.sleep(0.0001)
    WIN = pygame.display.set_mode(dslr.get_window_size())
    dslr.update_window(WIN)

    GRID.find_boundaries(WIN)
    GRID.create_grid()

    while events.is_running():
        events.handle_event(GRID, algorithm=A)

        if events.is_pathfinding():
            if events.is_calculating():
                distance_pos = dslr.get_distance_from_waypoint_and_pos()
                if distance_pos is not None:
                    if distance_pos[0] > 1000000:
                        events.make_start_update(distance_pos[1], distance_pos[2])

            if dslr.get_state():
                GRID.draw_grid(WIN)
                old_corners = corners
                corners = [(int(corner[0] * GRID.tile_diameter + GRID.tile_diameter / 2),
                            int(corner[1] * GRID.tile_diameter + GRID.tile_diameter / 2)) for corner in A.get_corners()]
                if corners and old_corners != corners:
                    dslr.assign_path_of_waypoints(corners)

        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
    with open('./detection/data/{}_data.txt', 'w') as w:
        w.write('0 0 0')
        w.close()
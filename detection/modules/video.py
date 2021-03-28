import cv2 as cv
import numpy as np
import math
import threading
from .simple_functions import *
from .inrange_calibrater import range_calibrater
from .detection_color import detection
from .waypoint import waypoint
from .detection_aruco import detections
import pygame


class video:
    def __init__(self, input_video, output_func, magnifier=None, x_offset=0, y_offset=0, window_name='default', key_close='q'):
        self.name = window_name
        self.key_close = key_close
        self.window_size = None
        self.window = None
        self.output_func = output_func

        self.input_video = input_video
        self.magnifier = magnifier
        self.x_offset, self.y_offset = x_offset, y_offset

        self.waypoints = []
        self.distance_in_cm = None
        self.lowest_green_calibrater = range_calibrater('lowest_green_calibrater')
        self.highest_green_calibrater = range_calibrater('highest_green_calibrater')
        self.lowest_blue_calibrater = range_calibrater('lowest_blue_calibrater')
        self.highest_blue_calibrater = range_calibrater('highest_blue_calibrater')

        self.state = False
        self.robot_detection = detection(self.lowest_green_calibrater, self.highest_green_calibrater,
                                         contour_size_lower_limit=100)
        self.robot_detection.run()
        self.robot_orientation_detection = detection(self.lowest_blue_calibrater, self.highest_blue_calibrater,
                                                     contour_size_lower_limit=100, contour_highlight_color=(0, 255, 0))
        self.robot_orientation_detection.run()
        modified_parameters = cv.aruco.DetectorParameters_create()
        """modified_parameters.minDistanceToBorder = 3
        modified_parameters.adaptiveThreshWinSizeMin = 3
        modified_parameters.adaptiveThreshConstant = 0
        modified_parameters.minMarkerPerimeterRate = 4"""
        modified_parameters.cornerRefinementMethod = cv.aruco.CORNER_REFINE_SUBPIX
        #modified_parameters.adaptiveThreshWinSizeMax = 0
        self.aruco_detections = detections(aruco_parameters=modified_parameters)

        self.box_x = self.box_y = None
        # ugly one but still functions
        self.done = False

    def on_click(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            new_waypoint = waypoint(x, y)
            self.waypoints.append(new_waypoint)

    def assign_path_of_waypoints(self, corners):
        self.waypoints = []
        for corner in corners:
            new_waypoint = waypoint(corner[0], corner[1])
            self.waypoints.insert(0, new_waypoint)

    def get_distance_from_waypoint_and_pos(self):
        return (self.distance_in_cm, self.box_x, self.box_y) if self.distance_in_cm is not None else None

    def update_window(self, window):
        self.window = window

    def get_state(self):
        return self.state

    def get_window_size(self):
        return self.window_size

    def colour_detection(self, frame):
        orientation_frame = frame.copy()
        orientation_boxes = self.robot_orientation_detection.main(orientation_frame)
        if orientation_boxes:
            orientation_box = orientation_boxes[0]
            (orientation_box_x, orientation_box_y), \
            (orientation_box_w, orientation_box_h), orientation_box_angle = orientation_box
        robot_frame = frame.copy()
        boxes = self.robot_detection.main(robot_frame)

        if boxes and orientation_boxes:
            box = boxes[0]
            (x, y), (w, h), angle = box
            box_width = min([w, h])
            box_height = max([w, h])
            self.box_x, self.box_y, box_angle = int(x), int(y), int(angle)
            if self.done is not True:
                aspect_height = box_height
                self.done = True
            if orientation_box_y <= y:
                if box_angle < -45:  # 0- 45
                    box_angle = 90 + box_angle
                if h < w and box_angle > 0:  # 46 - 90
                    box_angle = -(90 - box_angle)
                if h > w and box_angle < 0:  # -90 - 0
                    box_angle = 90 + box_angle
            else:
                if box_angle < -45:
                    box_angle = box_angle
                if h < w and box_angle < 0:
                    box_angle = 180 + box_angle
                if h > w and box_angle < 0:
                    box_angle = -90 + box_angle
                if box_angle == 0:
                    pass
            return 10, box_height, box_angle, cv.bitwise_and(robot_frame, orientation_frame)
        return None, None, None, frame

    def aruco_detection(self, frame):
        markers = self.aruco_detections.main(frame)
        if markers:
            print(markers)
        marker_10_pos = markers.get(10)
        marker_11_pos = markers.get(11)
        if marker_10_pos is not None and marker_11_pos is not None:
            self.box_x, self.box_y = int(marker_10_pos[0]), int(marker_11_pos[1])
            cv.circle(frame, (self.box_x, self.box_y), 2, (100, 255, 0), -1)
            print(marker_10_pos)
            box_angle = line_angle(self.box_x, self.box_y, marker_11_pos[0], marker_11_pos[1])
            return 10, 10, box_angle, frame
        return None, None, None, frame

    def main(self, detection_method_index=0):
        detection_methods = [self.colour_detection,
                             self.aruco_detection]

        while self.input_video.isOpened():
            self.state = False
            _, frame = self.input_video.read()
            if self.magnifier is not None:
                frame = modifiers.resize_src(frame, self.magnifier, method=cv.INTER_LINEAR)

            if not self.x_offset == 0 & self.y_offset == 0:
                frame = modifiers.crop_src(frame,
                                           self.x_offset, self.y_offset,
                                           magnifier=self.magnifier if self.magnifier is not None else 1)
            cv.resizeWindow(self.name, frame.shape[1], frame.shape[0])
            self.window_size = (frame.shape[1], frame.shape[0])
            cv.setMouseCallback(self.name, self.on_click)
            frame = modifiers.blur_src(frame)

            aspect_height, box_height, box_angle, frame = detection_methods[detection_method_index](frame)

            if box_height is not None:
                cv.circle(frame, (self.box_x, self.box_y), 3, (0, 255, 0), -1)
                with open('detection/data/robot_x_y.txt', 'w') as w:
                    w.write('{} {} {}'.format(int(self.box_x * (83 / aspect_height)),
                                              int(frame.shape[0] * (83 / aspect_height)) - int(
                                                  self.box_y * (83 / box_height)), box_angle))
                    w.close()
                if len(self.waypoints)>1:
                    distance = distance_between_2points(self.box_x, self.box_y,
                                                        self.waypoints[0].x, self.waypoints[0].y)
                    self.distance_in_cm = int(distance * (83 / aspect_height)) / 10

                    first_line_angle = line_angle(self.waypoints[1].x, self.waypoints[1].y, self.waypoints[0].x, self.waypoints[0].y)

                    angle_to_first_waypoint = int(difference_between_two_angles(box_angle, first_line_angle))

                    intersection_x, intersection_y, distance_from_first_line = distance_from_line(self.waypoints[0].x, self.waypoints[0].y, self.waypoints[1].x,
                                       self.waypoints[1].y, first_line_angle, self.box_x, self.box_y, angle_to_first_waypoint)
                    cv.line(frame, (self.box_x, self.box_y), (intersection_x, intersection_y), (255, 255, 200), 3)
                    #print(distance_from_first_line)
                    with open('detection/data/error.txt', 'w') as w:
                        w.write('{}'.format(str('{} {}'.format(angle_to_first_waypoint, self.distance_in_cm))))
                    cv.putText(frame, '{}'.format(str(angle_to_first_waypoint)), (self.box_x - 5, self.box_y + 10),
                               cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
                    cv.putText(frame, '{}deg'.format(int(first_line_angle)),
                               (self.waypoints[0].x - 20, self.waypoints[0].y - 20),
                               cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
                    cv.putText(frame, '{}degs '.format(int(box_angle)),
                               (self.waypoints[0].x - 20, self.waypoints[0].y - 60),
                               cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
                    cv.putText(frame, '{}cm'.format(self.distance_in_cm),
                               (self.waypoints[0].x - 20, self.waypoints[0].y - 40),
                               cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
                    if self.distance_in_cm < 10:
                        del self.waypoints[0]
                else:
                    cv.putText(frame, '{}'.format(str(box_angle)), (self.box_x - 5, self.box_y + 10),
                               cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
                    with open('detection/data/error.txt', 'w') as w:
                        w.write('0 0 0')
                        w.close()
            if len(self.waypoints) > 1:
                for index, waypoint in enumerate(self.waypoints):
                    if index == 0:
                        cv.line(frame, (waypoint.x, waypoint.y),
                                (self.waypoints[index + 1].x, self.waypoints[index + 1].y), (0, 0, 255), 1)
                    if index < len(self.waypoints) - 2:
                        cv.line(frame, (self.waypoints[index + 1].x, self.waypoints[index + 1].y),
                                (self.waypoints[index + 2].x, self.waypoints[index + 2].y), (0, 0, 255), 1)
                    waypoint.draw(frame)
                if self.waypoints:
                    first_line_angle = line_angle(self.waypoints[1].x, self.waypoints[1].y,
                                                      self.waypoints[0].x, self.waypoints[0].y)
                    print(first_line_angle)

            if self.window is not None:
                self.output_func(self.window, frame)
                self.state = True

            if cv.waitKey(1) and 0xFF == ord(self.key_close):
                break



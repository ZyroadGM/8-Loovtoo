import cv2 as cv
import numpy as np
from .simple_functions import *


class transformation_value_calibrater:
    def __init__(self, window_name):
        self.window_name = window_name


    def run(self):
        cv.namedWindow(self.window_name)
        # cv.createTrackbar('Erosion', self.window_name, 0, 25, function_filler)
        # cv.createTrackbar('Dilation', self.window_name, 0, 25, function_filler)
        cv.createTrackbar('Opening', self.window_name, 0, 25, function_filler)
        cv.createTrackbar('Closing', self.window_name, 0, 25, function_filler)
        with open('data/{}_data.txt'.format(self.window_name), 'r') as r:
            saved_pos = r.readline().split(' ')
            cv.setTrackbarPos('Opening', self.window_name, saved_pos[0])
            cv.setTrackbarPos('Closing', self.window_name, saved_pos[1])

    def get_info(self):
        opening = cv.getTrackbarPos('Opening', self.window_name)
        closing = cv.getTrackbarPos('Closing', self.window_name)
        return opening, closing

    def on_change(self, opening, closing):
        new_opening = cv.getTrackbarPos('Opening', self.window_name)
        new_closing = cv.getTrackbarPos('Closing', self.window_name)
        if [opening, closing] != [new_opening, new_closing]:
            with open('data/{}_data.txt'.format(self.window_name), 'w') as w:
                w.write('{} {}'.format(new_opening, new_closing))
                w.close()
        else:
            pass



import cv2 as cv
import numpy as np
from .simple_functions import *


class range_calibrater:
    def __init__(self, window_name, trackbar_hue_name='H', trackbar_saturation_name='S', trackbar_value_name='V'):
        self.window_name = window_name
        self.trackbar_hue_name = trackbar_hue_name
        self.trackbar_saturation_name = trackbar_saturation_name
        self.trackbar_value_name = trackbar_value_name

    def run(self):
        cv.namedWindow(self.window_name)
        cv.resizeWindow(winname=self.window_name, height=150, width=400)
        cv.createTrackbar(self.trackbar_hue_name, self.window_name, 0, 170, function_filler)
        cv.createTrackbar(self.trackbar_saturation_name, self.window_name, 0, 255, function_filler)
        cv.createTrackbar(self.trackbar_value_name, self.window_name, 0, 255, function_filler)
        with open('./detection/data/{}_data.txt'.format(self.window_name), 'r') as r:
            saved_pos = r.readline().split(' ')
            cv.setTrackbarPos(self.trackbar_hue_name, self.window_name, int(saved_pos[0]))
            cv.setTrackbarPos(self.trackbar_saturation_name, self.window_name, int(saved_pos[1]))
            cv.setTrackbarPos(self.trackbar_value_name, self.window_name, int(saved_pos[2]))

    def get_info(self):
        h = cv.getTrackbarPos(self.trackbar_hue_name, self.window_name)
        s = cv.getTrackbarPos(self.trackbar_saturation_name, self.window_name)
        v = cv.getTrackbarPos(self.trackbar_value_name, self.window_name)
        return h, s, v

    def on_change(self, h, s, v):
        new_h, new_s, new_v = cv.getTrackbarPos(self.trackbar_hue_name, self.window_name), \
                              cv.getTrackbarPos(self.trackbar_saturation_name, self.window_name), \
                              cv.getTrackbarPos(self.trackbar_value_name, self.window_name)
        if [h, s, v] != [new_h, new_s, new_v] and new_h != -1:
            with open('./detection/data/{}_data.txt'.format(self.window_name), 'w') as w:
                w.write('{} {} {}'.format(new_h, new_s, new_v))
                w.close()
        else:
            pass

import cv2 as cv
import numpy as np
from .simple_functions import *


class detection:
    def __init__(self, lowest_range_calibrater, highest_range_calibrater, contour_highlight_color=(255, 0, 0), contour_highlight_thickness=3, contour_size_lower_limit=1000):
        self.lowest_range_calibrater = lowest_range_calibrater
        self.highest_range_calibrater = highest_range_calibrater
        self.lowest_h, self.lowest_s, self.lowest_v = 0, 0, 0
        self.highest_h, self.highest_s, self.highest_v = 0, 0, 0
        self.contour_highlight_color = contour_highlight_color  # BGR
        self.contour_highlight_thickness = contour_highlight_thickness
        self.contour_size_lower_limit = contour_size_lower_limit
        self.run()

    def run(self):
        self.lowest_range_calibrater.run()
        self.highest_range_calibrater.run()

    def draw_box(self, src, points):
        points = [[int(float(i)) for i in corners] for corners in points]
        for index, point in enumerate(points):
            cv.line(src, tuple(point), tuple(points[index-1]), self.contour_highlight_color, 2)

    def main(self, src):
        if cv.getWindowProperty(self.lowest_range_calibrater.window_name, cv.WND_PROP_AUTOSIZE) != -1:
            self.lowest_range_calibrater.on_change(self.lowest_h, self.lowest_s, self.lowest_v)
            self.lowest_h, self.lowest_s, self.lowest_v = self.lowest_range_calibrater.get_info()
        if cv.getWindowProperty(self.highest_range_calibrater.window_name, cv.WND_PROP_AUTOSIZE) != -1:
            self.highest_range_calibrater.on_change(self.highest_h, self.highest_s, self.highest_v)
            self.highest_h, self.highest_s, self.highest_v = self.highest_range_calibrater.get_info()
        hsv_mask = modifiers.hsv_to_mask(cv.cvtColor(src, cv.COLOR_BGR2HSV),
                                         [self.lowest_h, self.lowest_s, self.lowest_v],
                                         [self.highest_h, self.highest_s, self.highest_v])
        contours, hierarchy = cv.findContours(hsv_mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        boxes = []
        for contour in contours:
            if cv.contourArea(contour) >= self.contour_size_lower_limit:
                rect = cv.minAreaRect(contour)
                boxes.append(rect)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                self.draw_box(src, box)
        cv.imshow('{}_mask'.format(self.highest_range_calibrater.window_name), hsv_mask)
        return boxes
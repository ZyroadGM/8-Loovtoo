import cv2 as cv
import numpy as np
from .simple_functions import *

class waypoint:
    def __init__(self, x, y, color=(0, 0, 255), radius=5):
        self.color = color
        self.x, self.y = x, y
        self.radius = radius

    def draw(self, src):
        cv.circle(src, (self.x, self.y), self.radius, self.color, -1)
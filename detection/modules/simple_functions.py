import cv2 as cv
import numpy as np
import math
import pygame


def function_filler(x):
    """This is just a filler function"""
    pass


def output_as_pygame(pygame_window, frame):
    frame = opencv_frame_to_pygame(frame)
    pygame_window.blit(frame, (0, 0))


def opencv_frame_to_pygame(frame):
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame = cv.flip(frame, 1)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame


def line_angle(x1, y1, x2, y2):
    dif_x = x2 - x1
    dif_y = y2 - y1
    theta = math.atan2(dif_y, dif_x)
    result = theta * (180 / math.pi) - 90  # returns range (-90 0 90, -90 - -270)
    if result <= -180:
        result = 360 + result
    return result


def distance_between_2points(x1, y1, x2, y2) -> float:
    return math.sqrt((x1 - x2) ** 2
                     + (y1 - y2) ** 2)


def difference_between_two_angles(a1, a2):
    if a1 > 0 and a2 <= -180 + a1:
        result = 180 + a2 + 180 - a1
    elif a1 < 0 and a2 >= 180 + a1:
        result = a2 - 180 + -180 - a1
    else:
        result = a2 - a1

    return result


def distance_from_line(x1, y1, x2, y2, al, x, y, a):
    al_ = al + 90 if a < 0 else -90 if a != 0 else 0
    #print(al)
    #print(al*0.011111, al*-0.011111 + 1)
    # *(al * 0.011111) *(al*-0.011111 + 1)
    determine_second_point = (math.cos(al_) + x, math.sin(al_) + y)
    # inspired by https://github.com/bit101/CodingMath/blob/master/episode32/main.js
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1

    A2 = determine_second_point[1] - y
    B2 = x - determine_second_point[0]
    C2 = A2 * x + B2 * y
    denominator = A1 * B2 - A2 * B1
    intersection_x, intersection_y = int((B2 * C1 - B1 * C2) / denominator), int((A1 * C2 - A2 * C1) / denominator)
    #
    return intersection_x, intersection_y, distance_between_2points(x, y,
                                    intersection_x, intersection_y)

class video_inputs:
    @staticmethod
    def website_as_input(link):
        return cv.VideoCapture(link)

    @staticmethod
    def webcam_as_input(channel):
        return cv.VideoCapture(channel if isinstance(channel, int) & channel >= 0 else 0)


class modifiers:
    @staticmethod
    def resize_src(src, magnifier, method=cv.INTER_BITS):
        return cv.resize(src,
                         (int(src.shape[1] * magnifier), int(src.shape[0] * magnifier)),
                         interpolation=method)

    @staticmethod
    def crop_src(src, x_offset, y_offset, magnifier=1):
        return src[int(y_offset * magnifier): int((src.shape[0] - y_offset) * magnifier),
               int(x_offset * magnifier): int((src.shape[1] - x_offset) * magnifier)]

    @staticmethod
    def blur_src(src, diameter=20, sigmaColor=30, sigmaSpace=30):
        return cv.bilateralFilter(src, diameter, sigmaColor, sigmaSpace)

    @staticmethod
    def hsv_to_mask(src, lowest_hsv, highest_hsv):
        lowest_hsv = np.array([lowest_hsv[0], lowest_hsv[1], lowest_hsv[2]])
        highest_hsv = np.array([highest_hsv[0], highest_hsv[1], highest_hsv[2]])
        return cv.inRange(src, lowest_hsv, highest_hsv)

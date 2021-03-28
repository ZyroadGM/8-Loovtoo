import cv2 as cv
from detection_aruco import detections
import time
markers = detections()
import numpy as np
camera = cv.VideoCapture(1)
while True:
    _, frame = camera.read()
    cv.imshow("sd", frame)
    """markers.main(frame)"""
    if cv.waitKey(1) and 0xFF == ord("t"):
        break


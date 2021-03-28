import cv2 as cv


class detections:
    def __init__(self, aruco_dictionary=cv.aruco.DICT_ARUCO_ORIGINAL, aruco_parameters=cv.aruco.DetectorParameters_create()):
        self.aruco_dictionary = cv.aruco.Dictionary_get(aruco_dictionary)
        self.aruco_parameters = aruco_parameters

    def main(self, src):
        result = {}
        src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        src = cv.resize(src, (int(src.shape[1] * 0.3), int(src.shape[0] * 0.3)), interpolation=cv.INTER_LINEAR)
        (corners, ids, rejected) = cv.aruco.detectMarkers(src, self.aruco_dictionary, parameters=self.aruco_parameters)
        if ids is None:
            return result
        for i in range(len(ids)):
            c = corners[i][0]
            result.update({ids[i][0]: (c[:, 0].mean(), c[:, 1].mean())})
        return result




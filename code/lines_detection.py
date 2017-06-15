import numpy as np
import cv2
import lines_sorting


def getEdges(image, low_threshold=50, high_threshold=150):
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges


def getLaneLines(edges):
    deg = np.pi/180
    lines = cv2.HoughLines(edges, 1, 1*deg, 40)

    if lines is None:
        return np.array([])

    points_array = list()
    for line in lines:
        for rho, theta in line:
            points_array.append((rho, theta))

    points_array = lines_sorting.CoordinateSorter(40, np.radians(4), 3).sort(points_array)

    return np.array(points_array)

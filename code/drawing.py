import cv2
import numpy as np


def convert(rho, theta, y_min, y_max):

    def create_point(y):
        x = (rho - y*np.sin(theta))/np.cos(theta)
        return int(x), int(y)

    d1 = create_point(y_max)
    d2 = create_point(y_min)

    return d1, d2


def drawLines(polar_coordinates_array, image, color, line_weight = 10):

    y_max = image.shape[0]
    y_min = int(y_max * 2 / 3)

    lines = [convert(rho, theta, y_min, y_max) for rho, theta in polar_coordinates_array]

    for d1, d2 in lines:
        cv2.line(image, d1, d2, color, line_weight)

import cv2
import numpy as np


def convert_polar_to_line(rho, theta, y_length):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 2000 * (-b))
    y1 = int(y0 + 2000 * (a))
    x2 = int(x0 - 2000 * (-b))
    y2 = int(y0 - 2000 * (a))
    d1 = (x1, y1)
    d2 = (x2, y2)

    return d1, d2


def draw_lines_from_bottom_to(y_length, pole_coordinates_array, image_shape):

    line_image = np.zeros(image_shape, dtype=np.uint8)
    lines = [convert_polar_to_line(pole_coordinates,y_length) for pole_coordinates in pole_coordinates_array]

    for point_1, point_2 in lines:
        cv2.line(line_image, point_1, point_2, (0, 0, 255), 10)

    return line_image
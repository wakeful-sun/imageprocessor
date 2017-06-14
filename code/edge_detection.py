import matplotlib.pyplot as plt
import numpy as np
import cv2
import lanes_area
import line_sorting


def applyGaussianBlur(image):
    kernel_size = 3
    blur_gray = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blur_gray


def getEdges(image, low_threshold=50, high_threshold=150):
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges


def detectLaneLines(edges):
    line_image = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)
    print(line_image.shape)
    deg = np.pi/180
    lines = cv2.HoughLines(edges, 1, 1*deg, 40)

    if lines is None:
        return line_image

    points_array = list()
    for line in lines:
        for rho,theta in line:
            points_array.append((rho, theta))

    points_array = line_sorting.CoordinateSorter(40, np.radians(4), 3).sort(points_array)

    lines_array = list()
    for rho, theta in points_array:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 2000*(-b))
        y1 = int(y0 + 2000*(a))
        x2 = int(x0 - 2000*(-b))
        y2 = int(y0 - 2000*(a))
        d1 = (x1,y1)
        d2 = (x2,y2)

        lines_array.append((d1,d2))
        cv2.line(line_image, d1, d2, (0, 0, 255), 10)
    print(lines_array)
    return line_image
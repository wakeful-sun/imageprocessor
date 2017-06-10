import matplotlib.pyplot as plt
import numpy as np
import cv2
import lanes_area

def applyGaussianBlur(image):
    kernel_size = 9
    blur_gray = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blur_gray


def getEdges(image, low_threshold = 50, high_threshold = 150):
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges


def detectLanes(edges_image, image_shape):
    rho = 2
    theta = (np.pi / 180) * 1

    min_intersection_amount = 50
    min_line_length = 15
    max_line_gap = 10

    lines = cv2.HoughLinesP(edges_image, rho, theta, min_intersection_amount, np.array([]),
                            min_line_length, max_line_gap)
    line_image = np.zeros(image_shape, dtype=np.uint8)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 5)

    return line_image
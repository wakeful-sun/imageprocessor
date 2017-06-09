import matplotlib.pyplot as plt
import numpy as np
import cv2
import lanes_area

DOT_TYPE = np.uint8

def getGrayImage(image):
    kernel_size = 5

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    return blur_gray


def getEdges(image):
    low_threshold = 50
    high_threshold = 150
    grey_image = getGrayImage(image)

    edges = cv2.Canny(grey_image, low_threshold, high_threshold)
    return edges


def detectLanes(edges_image, image_shape):
    rho = 2
    theta = (np.pi / 180) * 1

    min_intersection_amount = 15
    min_line_length = 40
    max_line_gap = 20

    lines = cv2.HoughLinesP(edges_image, rho, theta, min_intersection_amount, np.array([]),
                            min_line_length, max_line_gap)

    line_image = np.zeros(image_shape, dtype=DOT_TYPE)
    for line in lines:
        for x1, y1, x2, y2 in line:
            # cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 10)

    return line_image


def drawLaneEdges(image):
    edges_im = getEdges(image)
    area = lanes_area.applyDetectionArea(edges_im)
    line_image = detectLanes(area, image.shape)

    return line_image
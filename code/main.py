import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os

image_path = "../input/test_images/solidWhiteCurve.jpg"
current_directory = os.path.dirname(__file__)

initial_image_path = os.path.join(current_directory, image_path)
initial_image = mpimg.imread(initial_image_path)


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


def apply_detection_area(image, area_width_adjustment=15, area_height_adjustment=40):
    ignore_mask_color = 255

    im_height = image.shape[0]
    im_half_height = im_height // 2
    im_width = image.shape[1]
    im_half_width = im_width // 2

    area_left_bottom = (0, im_height)
    area_left_top = (im_half_width - area_width_adjustment,
                     im_half_height + area_height_adjustment)
    area_right_top = (im_half_width + area_width_adjustment,
                      im_half_height + area_height_adjustment)
    area_right_bottom = (im_width, im_height)

    detection_area = [area_left_bottom, area_left_top,
                      area_right_top, area_right_bottom]
    vertices = np.array([detection_area], dtype=np.int32)

    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def detect_lines(edges_image):
    rho = 2
    theta = (np.pi / 180) * 1

    min_intersection_amount = 15
    min_line_length = 40
    max_line_gap = 20

    line_image = np.copy(edges_image) * 0

    lines = cv2.HoughLinesP(edges_image, rho, theta, min_intersection_amount, np.array([]),
                            min_line_length, max_line_gap)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

    return line_image


def draw_lane_edges(image):

    color_edges = np.dstack((edges, edges, edges))
    # lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0)


grey_im = getGrayImage(initial_image)
edges_im = getEdges(initial_image)
area = apply_detection_area(initial_image)
l = detect_lines(edges_im)

plt.imshow(l)
plt.show()

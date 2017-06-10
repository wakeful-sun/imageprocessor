import matplotlib.pyplot as plt
import numpy as np
import cv2


def getColorMask(hsv_frame):
    lower_yellow = np.array([20, 0, 170], dtype=np.uint8)
    upper_yellow = np.array([55, 255, 255], dtype=np.uint8)
    mask_yellow = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    lower_white = np.array([0, 0, 220], dtype=np.uint8)
    upper_white = np.array([255, 25, 255], dtype=np.uint8)
    mask_white = cv2.inRange(hsv_frame, lower_white, upper_white)

    mask = cv2.add(mask_white, mask_yellow)
    return mask


def applyDetectionArea(image, area_width_adjustment=60, area_height_adjustment=65):
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

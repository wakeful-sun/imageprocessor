import matplotlib.pyplot as plt
import numpy as np
import cv2

def applyDetectionArea(image, area_width_adjustment=15, area_height_adjustment=50):
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
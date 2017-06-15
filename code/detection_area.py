import numpy as np
import cv2


class DetectionAreaFilter:

    def __init__(self):
        self._lower_yellow = np.array([20, 0, 170], dtype=np.uint8)
        self._upper_yellow = np.array([55, 255, 255], dtype=np.uint8)

        self._lower_white = np.array([0, 0, 220], dtype=np.uint8)
        self._upper_white = np.array([255, 25, 255], dtype=np.uint8)

        self._ignore_mask_color = 255

    def getColorMask(self, hsv_image):
        mask_yellow = cv2.inRange(hsv_image, self._lower_yellow, self._upper_yellow)
        mask_white = cv2.inRange(hsv_image, self._lower_white, self._upper_white)

        mask = cv2.add(mask_white, mask_yellow)
        return mask

    def applyDetectionArea(self, bw_image, width_adjustment=60, height_adjustment=65):
        im_height = bw_image.shape[0]
        im_half_height = im_height // 2
        im_width = bw_image.shape[1]
        im_half_width = im_width // 2

        area_left_bottom = (0, im_height)
        area_left_top = (im_half_width - width_adjustment, im_half_height + height_adjustment)
        area_right_top = (im_half_width + width_adjustment, im_half_height + height_adjustment)
        area_right_bottom = (im_width, im_height)

        detection_area = [area_left_bottom, area_left_top, area_right_top, area_right_bottom]
        vertices = np.array([detection_area], dtype=np.int32)

        mask = np.zeros_like(bw_image)
        cv2.fillPoly(mask, vertices, self._ignore_mask_color)

        masked_image = cv2.bitwise_and(bw_image, mask)
        return masked_image

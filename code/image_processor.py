import numpy as np
import cv2
from detection_area import DetectionAreaFilter
import lines_detection
import drawing


class ImageProcessor:

    def __init__(self):
        self._bgr_line_color = (0, 0, 255)
        self._detection_area_filter = DetectionAreaFilter()

    def processFrame(self, bgr_frame):
        frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)

        bw_color_mask = self._detection_area_filter.getColorMask(frame)
        bw_area = self._detection_area_filter.applyDetectionArea(bw_color_mask)

        bw_edges = lines_detection.getEdges(bw_area)
        polar_lane_coordinates = lines_detection.getLaneLines(bw_edges)

        lines_image = np.zeros_like(bgr_frame)
        drawing.drawLines(polar_lane_coordinates, lines_image, self._bgr_line_color)

        result_image = cv2.addWeighted(lines_image, 0.9, bgr_frame, 1, 0)

        # next line is used for testing purposes
        return self._convert_bw_2_color(bw_color_mask)
        #return result_image

    def _convert_bw_2_color(self, bw_image):
        return np.dstack((bw_image, bw_image, bw_image))
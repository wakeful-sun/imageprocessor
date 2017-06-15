import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import os
import numpy as np
from detection_area import DetectionAreaFilter
from lines_sorting import CoordinateSorter
from image_processor import ImageProcessor

image1 = "../input/test_images/solidWhiteCurve.jpg"
image2 = "../input/test_images/solidWhiteRight.jpg"
image3 = "../input/test_images/solidYellowCurve.jpg"
image4 = "../input/test_images/solidYellowCurve2.jpg"
image5 = "../input/test_images/solidYellowLeft.jpg"
image6 = "../input/test_images/whiteCarLaneSwitch.jpg"

video1 = "../input/test_videos/challenge.mp4"
video2 = "../input/test_videos/solidYellowLeft.mp4"
video3 = "../input/test_videos/solidWhiteRight.mp4"

detection_area_filter = DetectionAreaFilter()

max_distance_delta = 40  # max distance between lines (rho1 - rho2) in polar coordinate system
max_angle_delta = np.radians(4)  # max angle between lines (theta1 - theta2) in polar coordinate system
threshold = 3  # min amount of lines in set filter
coordinate_sorter = CoordinateSorter(max_distance_delta, max_angle_delta, threshold)

img_processor = ImageProcessor(detection_area_filter, coordinate_sorter)


def getPathFor(file_path):
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory, file_path)


def playVideo(file_path):
    video_path = getPathFor(file_path)
    video = cv2.VideoCapture(video_path)

    while video.isOpened():
        _, bgr_frame = video.read()

        if not isinstance(bgr_frame, np.ndarray):
            # workaround to handle end of video stream.
            break

        frame = img_processor.processFrame(bgr_frame)
        cv2.imshow("output", frame)

        key = cv2.waitKey(1) & 0xFF
        # stop video on ESC key pressed
        if key == 27:
            break

    video.release()
    cv2.destroyAllWindows()


def showImage(file_path):
    def convert(image):
        return image[..., [2, 1, 0]]

    image_path = getPathFor(file_path)
    rgb_image = mpimg.imread(image_path)

    bgr_frame = convert(rgb_image)
    frame = img_processor.processFrame(bgr_frame)
    rgb_frame = convert(frame)

    plt.imshow(rgb_frame)
    plt.show()


showImage(image3)
#playVideo(video1)

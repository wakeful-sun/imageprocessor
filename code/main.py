import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
import lanes_area
import edge_detection

image1 = "../input/test_images/solidWhiteCurve.jpg"
image2 = "../input/test_images/solidWhiteRight.jpg"
image3 = "../input/test_images/solidYellowCurve.jpg"
image4 = "../input/test_images/solidYellowCurve2.jpg"
image5 = "../input/test_images/solidYellowLeft.jpg"
image6 = "../input/test_images/whiteCarLaneSwitch.jpg"

video1 = "../input/test_videos/challenge.mp4"
video2 = "../input/test_videos/solidYellowLeft.mp4"
video3 = "../input/test_videos/solidWhiteRight.mp4"


def getPathFor(file_path):
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory, file_path)


def processFrame(bgr_frame):
    frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)

    color_mask = lanes_area.getColorMask(frame)
    area = lanes_area.applyDetectionArea(color_mask)
    blur = edge_detection.applyGaussianBlur(area)

    edges = edge_detection.getEdges(blur, 50, 150)
    result = edge_detection.detectLanes(edges, frame.shape)

    result_image = cv2.addWeighted(result, 0.9, bgr_frame, 1, 0)
    return result_image


def playVideo(file_path):
    video_path = getPathFor(file_path)
    video = cv2.VideoCapture(video_path)

    while(video.isOpened()):
        _, bgr_frame = video.read()

        frame = processFrame(bgr_frame)
        cv2.imshow("output", frame)

        key = cv2.waitKey(1) & 0xFF
        # stop video on ESC key pressed
        if key == 27:
            break

    video.release()
    cv2.destroyAllWindows()


def showImage(file_path):
    def flipColors(image):
        return image[..., [2, 1, 0]]

    image_path = getPathFor(file_path)
    rgb_image = mpimg.imread(image_path)
    bgr_frame = flipColors(rgb_image)

    brg_frame = processFrame(bgr_frame)

    rgb_frame = flipColors(brg_frame)
    plt.imshow(rgb_frame)
    plt.show()


showImage(image5)
# playVideo(video1)

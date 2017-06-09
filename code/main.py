import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
import lanes_area
import edge_detection


current_directory = os.path.dirname(__file__)
# image_path = "../input/test_images/solidYellowLeft.jpg"
# frame_path = os.path.join(current_directory, image_path)
# frame = mpimg.imread(frame_path)

video_path = "../input/test_videos/challenge.mp4"
# video_path = "../input/test_videos/solidYellowLeft.mp4"
video = cv2.VideoCapture(os.path.join(current_directory, video_path))


def applyColorFilters(image):
    white_threshold = [220, 220, 220]
    yellow_threshold = [220, 190, 100]

    # yellow_dot = (image[:, :, 0] > 220) | (image[:, :, 1] > 190) | (image[:, :, 2] < 100)
    yellow_dot = (image[:, :, 0] < 100) | (image[:, :, 1] > 190) | (image[:, :, 2] > 220)
    white_dot = (image[:, :, 0] > 220) | (image[:, :, 1] > 220) | (image[:, :, 2] > 220)

    filtered_image = np.copy(image)
    filtered_image[yellow_dot | white_dot] = [255, 255, 255]

    return filtered_image


def composeFrame(image):
    edges = edge_detection.drawLaneEdges(image)
    # line_image = applyColorFilters(image)
    # pure_white = (line_image[:, :, 0] == 255) | (line_image[:, :, 1] == 255) | (line_image[:, :, 2] == 255)
    # edges[~pure_white] = [0, 0, 0]
    result_image = cv2.addWeighted(edges, 0.8, image, 1, 0)

    return result_image


while(video.isOpened()):
    ret, frame = video.read()

    processedFrame = composeFrame(frame)

    cv2.imshow("lanes", processedFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()


# edges = edge_detection.drawLaneEdges(frame)
# line_image = applyColorFilters(frame)
# pure_white = (line_image[:, :, 0] == 255) | (line_image[:, :, 1] == 255) | (line_image[:, :, 2] == 255)
# edges[~pure_white] = [0, 0, 0]
# result_image = cv2.addWeighted(edges, 0.8, frame, 1, 0)

# plt.imshow(edges)
# plt.show()

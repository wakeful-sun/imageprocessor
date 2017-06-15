#**Finding Lane Lines on the Road**

<img src="input/examples/laneLines_thirdPass.jpg" width="480" alt="Combined Image" />

Overview
---

When we drive, we use our eyes to decide where to go.  The lines on the road that show us where the lanes are act as our constant reference for where to steer the vehicle.  Naturally, one of the first things we would like to do in developing a self-driving car is to automatically detect lane lines using an algorithm.

Project Writeup
---

Programm has image processing pipeline that support both RGB images and BGR video input.

    RGB image processing consists of next steps:
        - image file reading. File expected to exist on disk
        - RGB to BGR conversion
        - common image processing pipeline
        - processing result conversion (BGR to RGB)
        - result image output
    BGR video processing consists of next steps:
        - video file capturing. File expected to exist on disk
        - video frame processing loop:
            * common image processing pipeline
            * result frame output
        - resources release

    Image processing pipeline does:
        - BGR to HSV conversion
        - white and yellow colors filter, creates b/w image. Makes other colored objects black
        - detection area filter. Creates new b/w image output of color filter result
        - edge detection
        - lines detection with help of Hough transform method (cv2.HoughLines tool)
        - lanes detection with help of custom algorithm that does line groups detection and median line
          calculation for each found group
        - lane lines Polar coortinate to Cartesian coordinate conversion, drawing lane lines
        - result image composition from initial frame and detected lane lines images
        - result image returned to program for output/further operations

Colors detection on HSV image allows efficientely get rid of noise coused by shadows and road surface color artifacts. Further b/w image processing might save processor time.

Image processing pipeline in pictures:


<ul>
    <li>
        <div>White and yellow colors filter resul</div>
        <div><img src="results/01_white_and_yello_color_filter_output.png" width="560" alt="Color filter result" /></div>
    </li>
    <li>
        <div>Detection area filter result</div>
        <div><img src="results/02_detection_area.png" width="560" alt="Detection area filter result" /></div>
    </li>
    <li>
        <div>Edge detection result</div>
        <div><img src="results/03_edge_detection.png" width="560" alt="Edge detection" /></div>
    </li>
    <li>
        <div>Transformed into image cv2.HoughLines output</div>
        <div><img src="results/04_cv2.HoughLines_result.png" width="560" alt="Hough transformation" /></div>
    </li>
    <li>
        <div>Transformed into image lines filtering and grouping with resulting line algorithm output</div>
        <div><img src="results/05_lines_grouping_result.png" width="560" alt="Lines groupting" /></div>
    </li>
    <li>
        <div>Polar coortinate to Cartesian coordinate conversion, drawing</div>
        <div><img src="results/06_drawing_result.png" width="560" alt="Lanes drawing" /></div>
    </li>
    <li>
        <div>Program output</div>
        <div><img src="results/07_program_result.png" width="560" alt="Program output result" /></div>
    </li>
</ul>

As the next improvement I would extract configuration parametes into separate entity. And would use same instance of it for on-flight configuration/adjustment. It can become an interface for another system :)


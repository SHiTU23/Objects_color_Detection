import cv2
from MyObjectDetector import *
import numpy as np
from color_detection import color


def img_show(img):
    cv2.imshow("win", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


AROCU_LENGTH = 145
NUMBER_OF_AROCU_SIDES = 4

# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

# Load your Object Detector
obj_detector = NewObjectDetector()
# Load Cap
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
_,img = cap.read() 

corners, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

if corners:
    # Draw polygon around the marker
    int_corners = np.int0(corners) #convert to ints since polylines does not accept array
    cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
    aruco_perimeter = cv2.arcLength(corners[0], True)
    
    pixel_mm_ratio = aruco_perimeter / (AROCU_LENGTH*NUMBER_OF_AROCU_SIDES) ### 145 is the len
    contours = obj_detector.My_detector(img)

    for cnt in contours:
        # Get bounding rectangel of objects found
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect

        box = cv2.boxPoints(rect)
        # Get Width and Height of the Objects by applying the Ratio pixel to cm
        object_width = w / pixel_mm_ratio
        object_height = h / pixel_mm_ratio
        box = np.int0(box)
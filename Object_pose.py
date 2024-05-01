###############################################
###  FINDING POSITION OF CENTER OF OBJECTS  ###
###  AUTHOR : Shiva - shiva.tutunchi23@gmail.com


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
objs_position = []

# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

obj_detector = NewObjectDetector()
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
        object_x = x / pixel_mm_ratio
        object_y = y / pixel_mm_ratio
        box = np.int0(box)

        (b,g,r) = img[int(y), int(x)]
        object_color = color(r, g, b)

        ### BRIK DIMENSSIONS
        if ((object_width < 150 and object_width > 70) and  (object_height<30 and object_height > 20)) or  ((object_height < 150 and object_height > 70) and  (object_width<30 and object_width > 20)) :
            objs_position.append([object_color,f"{float(object_x):.2f},{float(object_y):.2f},{float(angle):.2f}"])

            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(img, [box], True, (255, 0, 0), 2)
            cv2.putText(img, f"h:{int(object_height)}, w:{int(object_width)}", (int(x-100), int(y + 30)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)            cv2.putText(img, f"color: {object_color}", (int(x ), int(y-50)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            cv2.putText(img, f"Position {x}, {y} mm", (int(x - 500), int(y)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            cv2.putText(img, f"Orientation is {angle} degrees", (int(x - 100), int(y + 10)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            cv2.circle(img,(int(x), int(y)),1,(255,255,0),1)

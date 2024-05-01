###############################################
###  FINDING POSITION OF CENTER OF OBJECTS  ###
###  AUTHOR : Shiva - shiva.tutunchi23@gmail.com


import cv2
from MyObjectDetector import *
import numpy as np
from color_detection import color



cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
_,img = cap.read() 

def obj_pose(mode: str, obj_dimension_range, image, Aruco_dimensions):
    """
    mode : '' /'color_order' / 'red' / 'green' / 'blue' 
    Aruco_dimensions : DICT_5X5_50
    """
    
    AROCU_LENGTH = 145
    NUMBER_OF_AROCU_SIDES = 4
    objs_position = []

    # Load Aruco detector
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.Aruco_dimensions)

    obj_detector = NewObjectDetector()
    

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


    number_obj = len(objs_position)
    obj_colors = ''
    for i in range(number_obj):
        if objs_position[i][0] not in obj_colors:
            obj_colors = obj_colors + ', ' + objs_position[i][0]


    choose_black = "choose 'k' for black" if 'Black' in obj_colors else ''

    ### requesting ordering the colors of detected objects
    order_colors = input(f'we\'ve got {number_obj} with colors of "{obj_colors}", please choose your order {choose_black} >>')
    print(order_colors)

    output = f'{number_obj};'

    for col in range(len(order_colors)):
        for obj in range(number_obj):
            if order_colors[col] == 'K':
                if 'Black' == objs_position[obj][0]:
                    output = output + objs_position[obj][1] + ';'
            else:
                if order_colors[col] == objs_position[obj][0][0]:
                    output = output + objs_position[obj][1] + ';'

    print(output)

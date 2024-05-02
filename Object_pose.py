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

# cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
# _,image = cap.read() 

def obj_pose(hight_range_in_mm, width_range_in_mm, image, Aruco_type, Aruco_length_in_mm, image_show='all'):
    """
    mode : '' /'color_order' / 'red' / 'green' / 'blue' 
    hight_range_in_mm : (hight_lowerband, hight_upperBand) = (10,20)
    width_range_in_mm : (width_lowerband, width_upperBand) = (10,20)
    Aruco_code : cv2.aruco.DICT_5X5_50
    Aruco_length : the length of each side of the arocu marker
    image_show : 'all' / 'center_point' / 'dimensions' / 'angle' / 'color'
    """

    NUMBER_OF_AROCU_SIDES = 4
    HIGHT_LOWER_BAND, HIGHT_UPPER_BAND = hight_range_in_mm
    WIDTH_LOWER_BAND, WIDTH_UPPER_BAND = width_range_in_mm
    BLACK_FONT = (0,0,0)
    objs_position = []

    # Load Aruco detector
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(Aruco_type)

    obj_detector = NewObjectDetector()
    

    corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)

    if corners:
        # Draw polygon around the marker
        int_corners = np.int0(corners) #convert to ints since polylines does not accept array
        cv2.polylines(image, int_corners, True, (0, 255, 0), 5)
        aruco_perimeter = cv2.arcLength(corners[0], True)
        
        pixel_mm_ratio = aruco_perimeter / (Aruco_length_in_mm*NUMBER_OF_AROCU_SIDES) ### 145 is the len
        contours = obj_detector.My_detector(image)

        

        for cnt in contours:
            # Get bounding rectangel of objects found
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect
            x, y, angle = int(x), int(y), int(angle)

            box = cv2.boxPoints(rect)
            # Get Width and Height of the Objects by applying the Ratio pixel to cm
            object_width = int(w / pixel_mm_ratio)
            object_height = int(h / pixel_mm_ratio)
            object_x = int(x / pixel_mm_ratio)
            object_y = int(y / pixel_mm_ratio)
            box = np.int0(box)

            (b,g,r) = image[int(y), int(x)]
            object_color = color(r, g, b)

            ### BRIK DIMENSSIONS
            if (((object_width  < WIDTH_UPPER_BAND and object_width  > WIDTH_LOWER_BAND) and 
                 (object_height < HIGHT_UPPER_BAND and object_height > HIGHT_LOWER_BAND)) or 
                ((object_height < WIDTH_UPPER_BAND and object_height > WIDTH_LOWER_BAND) and 
                 (object_width  < HIGHT_UPPER_BAND and object_width  > HIGHT_LOWER_BAND))):
                objs_position.append([object_color,f"{object_x},{object_y},{angle}"])

                cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
                cv2.polylines(image, [box], True, (255, 0, 0), 2)
                cv2.circle(image,(x, y),1,(255,255,0),1)
                
                match image_show: 
                    case 'all':
                        cv2.putText(image, f"color: {object_color}", (x-100 , y-50), cv2.FONT_HERSHEY_PLAIN, 1, BLACK_FONT, 2)
                        cv2.putText(image, f"angle: {angle}", (x-100, y-25), cv2.FONT_HERSHEY_PLAIN, 1, BLACK_FONT, 2)
                        cv2.putText(image, f"center pose: {x}, {y} mm", (x-100, y), cv2.FONT_HERSHEY_PLAIN, 1, BLACK_FONT, 2)
                        cv2.putText(image, f"h:{object_height}, w:{object_width}", (x-100, y+25), cv2.FONT_HERSHEY_PLAIN, 1, BLACK_FONT, 2)            
                    case 'center_point':
                        cv2.putText(image, f"center pose: {x}, {y} mm", (x-100, y), cv2.FONT_HERSHEY_PLAIN, 1, BLACK_FONT, 2)
                    case 'dimensions':
                        cv2.putText(image, f"h:{object_height}, w:{object_width}", (x-40, y), cv2.FONT_HERSHEY_PLAIN, 1, BLACK_FONT, 2)            
                    case 'angle':
                        cv2.putText(image, f"angle: {angle}", (x-50, y), cv2.FONT_HERSHEY_PLAIN, 1, BLACK_FONT, 2)
                    case 'color':
                        cv2.putText(image, f"color: {object_color}", (x-50 , y), cv2.FONT_HERSHEY_PLAIN, 1, BLACK_FONT, 2)
                        
        img_show(image)

    # number_obj = len(objs_position)
    # obj_colors = ''
    # for i in range(number_obj):
    #     if objs_position[i][0] not in obj_colors:
    #         obj_colors = obj_colors + ', ' + objs_position[i][0]


    # choose_black = "choose 'k' for black" if 'Black' in obj_colors else ''

    # ### requesting ordering the colors of detected objects
    # order_colors = input(f'we\'ve got {number_obj} with colors of "{obj_colors}", please choose your order {choose_black} >>')
    # print(order_colors)

    # output = f'{number_obj};'

    # for col in range(len(order_colors)):
    #     for obj in range(number_obj):
    #         if order_colors[col] == 'K':
    #             if 'Black' == objs_position[obj][0]:
    #                 output = output + objs_position[obj][1] + ';'
    #         else:
    #             if order_colors[col] == objs_position[obj][0][0]:
    #                 output = output + objs_position[obj][1] + ';'

    return (objs_position)

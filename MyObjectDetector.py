import cv2

class NewObjectDetector():
    def __init__(self):
        pass

    def My_detector(self, img):
        
        
         # Convert Image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #blurred = cv2.GaussianBlur(gray, (11,11), 0)
        # Create a Mask         
        Binarized=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)     
        # Find contours
        contours ,_ = cv2.findContours(Binarized.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        
        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            #Filter out the smallest stuff
            if area > 200:                
                objects_contours.append(cnt)

        return objects_contours
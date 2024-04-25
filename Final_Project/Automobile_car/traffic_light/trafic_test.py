#-*- coding:utf-8 -*-
import cv2
import numpy as np
from pymycobot.myagv import MyAgv

# mc = MyAgv('/dev/ttyAMA2', 115200)
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
cx = 0
cy = 0
i, j = 0, 0

while True:
    ret, img  = cap.read()
    if not ret:
        break
    
    # 1. ROI ?? ??
    height, width, _ = img.shape
    roi_height = height // 10 * 5
    roi_width = 0
    roi = img[roi_height:, roi_width:(width - roi_width)]

    # 2. Masking
    img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Red color mask
    # img_mask_red2 = cv2.inRange(img_cvt, np.array([160, 120, 80]), np.array([180, 255, 255]))
    img_mask_red2 = cv2.inRange(img_cvt, np.array([170, 200, 200]), np.array([180, 255, 255]))

    # Green color mask
    img_mask_green = cv2.inRange(img_cvt, np.array([45, 100, 150]), np.array([75, 255, 255]))

    cont_list_red, _ = cv2.findContours(img_mask_red2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cont_list_green, _ = cv2.findContours(img_mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    try: 
        # Check for the presence of red or green color in the image
        if cv2.countNonZero(img_mask_red2) > 0:
            print(f"Red light detected {i}")
            i += 1
        elif cv2.countNonZero(img_mask_green) > 0:
            print(f"Green light detected {j}")
            j += 1

        # Show the masks
        # cv2.imshow('Red Mask', img_mask_red2)
        # cv2.imshow('Green Mask', img_mask_green)
        
    except:
        pass

    # cv2.imshow('Red Mask', img_mask_red2)
    # cv2.imshow('Green Mask', img_mask_green)
    key = cv2.waitKey(1)
    if key&0xff == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
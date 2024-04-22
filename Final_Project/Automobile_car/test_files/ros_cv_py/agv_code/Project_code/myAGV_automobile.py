#-*- coding:utf-8 -*-
import cv2
import numpy as np
from pymycobot.myagv import MyAgv

mc = MyAgv('/dev/ttyAMA2', 115200)
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
cx = 0
cy = 0

while True:
    ret, img  = cap.read()
    if not ret:
        break
    
    # 1. ROI 범위 한정
    height, width, _ = img.shape
    roi_height = height // 10 * 9
    roi_width = 100
    roi = img[roi_height:, roi_width:(width - roi_width)]

    # 2. Masking
    img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Red
    # img_mask1 = cv2.inRange(img_cvt, np.array([0, 100, 100]), np.array([20, 255, 255]))
    # img_mask2 = cv2.inRange(img_cvt, np.array([160, 100, 100]), np.array([180, 255, 255]))
    # img_mask = img_mask1 + img_mask2

    # Yellow
    img_mask1 = cv2.inRange(img_cvt, np.array([22, 100, 100]), np.array([35, 255, 255]))
    cont_list, hierachy = cv2.findContours(img_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # 3. Find center of the contour
    offset = 100
    try: # if only detect yellow
        c = max(cont_list, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(cx)
        cv2.drawContours(roi, c, -1, (0,0,255), 1)
        cv2.circle(roi, (cx,cy), 5, (0,255,0), -1)

        # 4. Control the motors
        mid = (width - 2*roi_width) // 2
        if mid-offset <= cx <= mid+offset:
            mc.go_ahead(1)
            print("GO")
        elif cx < mid-offset:
            mc.counterclockwise_rotation(1)
            print("Left")
        else:
            mc.clockwise_rotation(1)
            print("Right")
        
    except:
        pass

    # 5. (Optional) Check with reference line
    wmid = width//2
    cv2.line(img, (wmid-offset, height), (wmid-offset, roi_height), (0,255,0), 1)
    cv2.line(img, (wmid+offset, height), (wmid+offset, roi_height), (0,255,0), 1)
    cv2.imshow('mask', img)
    key = cv2.waitKey(1)
    if key&0xff == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
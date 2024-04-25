#-*- coding:utf-8 -*-
import cv2
import numpy as np
import rospy
from std_msgs.msg import Int32
import time

def publish_message():
    pub_motor = rospy.Publisher('control_motor', Int32, queue_size=10)
    rospy.init_node('motor_control_pub', anonymous=True)
    rate = rospy.Rate(10)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    rospy.loginfo('Publishing video signal')

    cx = 0
    cy = 0
    dir_not_detected = 0
    while not rospy.is_shutdown():
        ret, img  = cap.read()
        if not ret:
            break

        # 1. ROI 범위 한정
        height, width, _ = img.shape
        # print(f"width height : {width}, {height}")
        roi_height = height // 100 * 90
        roi_width = 0
        roi = img[roi_height:, roi_width:(width - roi_width)]
        # print(f"test1 : {roi_width, width-roi_width}")
        # print(f"roi shape {roi.shape[0], roi.shape[1]}")

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
        offset = width//2.25
        try: # if only detect yellow
            c = max(cont_list, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print(cx)
            # cv2.drawContours(roi, c, -1, (0,0,255), 1)
            # cv2.circle(roi, (cx,cy), 5, (0,255,0), -1)

            # 4. Control the motors
            # Go 0, (Except)Left -1, (Except)Right 1, Stop 10
            mid = (width - 2*roi_width) // 2
            if mid-offset <= cx <= mid+offset:
                dir_not_detected = cx
                print("Cam Pub node : GO")
                pub_motor.publish(0)
            elif cx < mid-offset:
                dir_not_detected = cx
                print("Cam Pub node : Left")
                pub_motor.publish(-1)
            elif cx > mid+offset:
                dir_not_detected = cx
                print("Cam Pub node : Right")
                pub_motor.publish(1)
                # print(f"dnd : {dir_not_detected}, {width-roi_width}")

        except:
            # if cannot detect
            not_offset = width//4
            if 0 < dir_not_detected <= not_offset:
                print("Cam Pub node : Except Left")
                pub_motor.publish(-1)
            elif (width-roi_width)-not_offset <= dir_not_detected < width-roi_width:
                print("Cam Pub node : Except Right")
                pub_motor.publish(1)
            else:
                print("Cam Pub node : Except Go")
                pub_motor.publish(0)

        rate.sleep()
        # 5. (Optional) Check with reference line
        wmid = width//2
        # cv2.line(img, (wmid-offset, height), (wmid-offset, roi_height), (0,255,0), 1)
        # cv2.line(img, (wmid+offset, height), (wmid+offset, roi_height), (0,255,0), 1)
        # cv2.imshow('mask', img)
        key = cv2.waitKey(1)
        # if key&0xff == ord('q'):
        #     break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    publish_message()
    
        
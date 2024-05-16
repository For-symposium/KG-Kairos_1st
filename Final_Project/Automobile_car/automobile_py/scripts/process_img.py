#-*- coding:utf-8 -*-
import cv2
import numpy as np
import rospy
from std_msgs.msg import Int32
# import time

def publish_message():
    pub_motor = rospy.Publisher('control_motor', Int32, queue_size=10)
    pub_traffic = rospy.Publisher('control_traffic', Int32, queue_size=10)
    rospy.init_node('motor_control_pub', anonymous=True)
    rate = rospy.Rate(10)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    rospy.loginfo('Publishing video signal with traffic light')

    cx = 0
    cy = 0
    dir_not_detected = 0
    i, j = 0, 0
    while not rospy.is_shutdown():
        ret, img  = cap.read()
        if not ret:
            break

        # 1. ROI 범위 한정
        height, width, _ = img.shape
        # print(f"width height : {width}, {height}")
        # For Line tracing
        roi_height = height // 100 * 90
        roi_width = 0
        roi = img[roi_height:, roi_width:(width - roi_width)]

        # For traffic light
        roi_height_traffic = 180
        roi_width_traffic = width // 6
        roi_traffic = img[roi_height_traffic:roi_height_traffic*2, roi_width_traffic:(width - roi_width_traffic)]

        # 2. Masking
        img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        img_cvt_traffic = cv2.cvtColor(roi_traffic, cv2.COLOR_BGR2HSV)

        # Yellow line tracing
        img_mask1 = cv2.inRange(img_cvt, np.array([22, 100, 100]), np.array([35, 255, 255]))
        cont_list, _ = cv2.findContours(img_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        # Red Traffic light
        img_mask_red2 = cv2.inRange(img_cvt_traffic, np.array([160, 150, 150]), np.array([180, 255, 255]))

        # Traffic light : Stop 200, Pass 210
        try:
            if cv2.countNonZero(img_mask_red2) > 0:
                print(f"Traffic Pub : Red light detected {i}")
                i += 1
                pub_traffic.publish(200) # Stop
            else:
                print(f"Traffic Pub : Pass {j}")
                j += 1
                pub_traffic.publish(210) # Pass
        except:
            print("Traffic Pub : Exception")

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
        key = cv2.waitKey(1)

        ### In case I need to check
        # cv2.line(img, (wmid-offset, height), (wmid-offset, roi_height), (0,255,0), 1)
        # cv2.line(img, (wmid+offset, height), (wmid+offset, roi_height), (0,255,0), 1)
        cv2.imshow('mask', img)
        if key&0xff == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    try:
        publish_message()
    except rospy.ROSInterruptException:
        print("Motor control Pub node : Finish Publishing")
    
        
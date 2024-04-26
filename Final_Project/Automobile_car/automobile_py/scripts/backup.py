# process_img.py 24.04.26 09:20
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
    
        
# control_motor.py 24.04.26 09.33
import rospy
from std_msgs.msg import Int32
from pymycobot.myagv import MyAgv

'''
< Data signals >

1. OpenCV Line-tracing
    - 0 : GO
    - -1 : Left
    - 1 : Right
    - 10 : STOP

2. Lidar Obstacle
    - 100 : STOP
    - 110 : Allow to move

3. Traffic light
    - 200 : STOP
    - 210 : Allowed
'''

mc = MyAgv('/dev/ttyAMA2', 115200)
lidar2motor_control = True # bridge from lidar to motor_control
traffic2motor_control = True # bridge from traffic to motor_control

def motor_control_callback(data):
    global lidar2motor_control, traffic2motor_control
    if lidar2motor_control == True and traffic2motor_control == True:
        if data.data == 0:
            print("Cam Sub : GO")
            mc.go_ahead(1)
        elif data.data == 1:
            print("Cam Sub : Right")
            mc.clockwise_rotation(1)
        elif data.data == -1:
            print("Cam Sub : Left")
            mc.counterclockwise_rotation(1)
        elif data.data == 10:
            print("Cam Sub : STOP")
            mc.stop()

def lidar_check_callback(ldata):
    global lidar2motor_control
    if ldata.data == 100:
        print("Lidar Sub : STOP")
        mc.stop()
        lidar2motor_control = False
    elif ldata.data == 110:
        print("Lidar Sub : Pass")
        # mc.go_ahead(1)
        lidar2motor_control = True

def traffic_check_callback(tdata):
    global traffic2motor_control
    if tdata.data == 200:
        print("Traffic Sub : STOP")
        mc.stop()
        traffic2motor_control = False
    else:
        print("Traffic Sub : Pass")
        traffic2motor_control = True

def clean_up():
    rospy.loginfo("Sub node: Cleaning up...")
    mc.stop()

def listener():
    rospy.init_node('motor_control_sub', anonymous=True)
    rospy.Subscriber('control_motor', Int32, motor_control_callback)
    rospy.Subscriber('lidar_obstacle', Int32, lidar_check_callback)
    # rospy.Subscriber('traffic_light', Int32, traffic_check_callback)
    rospy.on_shutdown(clean_up)
    rospy.spin()  # Keep away from exiting

if __name__ == '__main__':
    listener()
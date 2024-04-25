#-*- coding:utf-8 -*-
import cv2
import numpy as np
import rospy
from std_msgs.msg import Int32
from pymycobot.myagv import MyAgv

# Reduce ROI MORE!!!!
# mc = MyAgv('/dev/ttyAMA2', 115200)
def publish_message_traffic():
    pub_traffic = rospy.Publisher('traffic_light', Int32, queue_size=10)
    rospy.init_node('traffic_pub_node', anonymous=True)
    rate = rospy.Rate(10)
    rospy.loginfo('Publishing traffic signal')

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    i, j = 0, 0

    while not rospy.is_shutdown():
        ret, img  = cap.read()
        if not ret:
            break
        
        # 1. ROI ?? ??
        height, width, _ = img.shape
        roi_height = 180
        roi_width = width // 4
        roi = img[roi_height:roi_height*2, roi_width:(width - roi_width)]

        # 2. Masking
        img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Red color mask
        # img_mask_red2 = cv2.inRange(img_cvt, np.array([160, 120, 80]), np.array([180, 255, 255]))
        img_mask_red2 = cv2.inRange(img_cvt, np.array([170, 200, 200]), np.array([180, 255, 255]))

        # Green color mask
        # img_mask_green = cv2.inRange(img_cvt, np.array([45, 100, 150]), np.array([75, 255, 255]))

        try: 
            # Check for the presence of red or green color in the image
            if cv2.countNonZero(img_mask_red2) > 0:
                print(f"Traffic Pub : Red light detected {i}")
                i += 1
                pub_traffic.publish(200) # Stop
            else:
                print(f"Traffic Pub : Pass {j}")
                j += 1
                pub_traffic.publish(210) # Pass

            # elif cv2.countNonZero(img_mask_green) > 0:
            #     print(f"Traffic : Green light detected {j}")
            #     j += 1
            #     pub_traffic.publish(210) # Go

            # Show the masks
            # cv2.imshow('Red Mask', img_mask_red2)
            # cv2.imshow('Green Mask', img_mask_green)
            
        except:
            pass

        rate.sleep()

        cv2.imshow('Red Mask', img)
        # cv2.imshow('Green Mask', img_mask_green)
        key = cv2.waitKey(1)
        if key&0xff == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    try:
        publish_message_traffic()
    except rospy.ROSInterruptException:
        print("Traffic Pub node : Finish Publishing")
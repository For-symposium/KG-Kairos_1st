'''
[-1, 0, 0, -1, 1, 1, 0, 0, 1, 1]

available_switch_to_ir : True, len of approx : 4
Zero turn array: [0, 0, -1, 1, 1, 0, 0, 1, 1], count : 1
Center point (Normal) : 349
available_switch_to_ir : True, len of approx : 6
Zero turn array: [1, 1, 0, 0, 1, 1], count : 1
Center point (Normal) : 350
Cam pub : Switch to IR sensor mode and Zero turn Right 595
CAM MODE FALSE 596
CAM MODE FALSE 597
CAM MODE FALSE 598
Control cam mode Function : Cam mode OFF 599
CAM MODE FALSE 600
CAM MODE FALSE 601

'''

import cv2
import numpy as np
import time
# import rospy
# from std_msgs.msg import Int32

path_to_subfile = "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/src/elec_charge/src/IR_mode_pub.py"

def publish_message():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    cx = 0
    cy = 0
    dir_not_detected = 0
    i = 0
    previous_x_distance = None
    # previous_message = None
    # current_message = 10

    while True:
        # print("check 1")
        ret, img = cap.read()
        if not ret:
            break

        height, width, _ = img.shape
        # For Line tracing
        roi_height = round(height * 0.95)
        roi_width = 0
        roi = img[roi_height:, roi_width:(width - roi_width)]

        # 2. Masking
        img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Yellow line tracing
        img_mask1 = cv2.inRange(img_cvt, np.array([22, 100, 100]), np.array([35, 255, 255]))
        # Black line
        # img_mask1 = cv2.inRange(img_cvt, np.array([0, 0, 0]), np.array([200, 120, 50]))
        
        cont_list, _ = cv2.findContours(img_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        # 3. Find center of the contour
        try:
            if cont_list:
                # print("check 2")
                c = max(cont_list, key=cv2.contourArea)
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                print(f"Center point : {cx} {i}")
                i += 1
                cv2.drawContours(roi, c, -1, (0, 0, 255), 1)
                cv2.circle(roi, (cx, cy), 5, (0, 255, 0), -1)

                # Approximate contour to a polygon
                epsilon = 0.025 * cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, epsilon, True)
                print(f"approxes: {len(approx)}")

                # Find the top two points
                sorted_points = sorted(approx, key=lambda point: point[0][1])  # Sort by y-coordinate

                for point in sorted_points:
                    x, y = point[0]
                    cv2.circle(roi, (x, y), 5, (255, 0, 0), -1)  # Blue circles

                # 4. Control the motors
                offset = width * 0.2
                if offset <= cx <= width - offset:
                    # if current_message != previous_message:
                    print(f"Cam Pub node : GO {i}")
                    i += 1
                    # pub_motor.publish(10)
                    # previous_message = current_message
                else:
                    print(f"Cam Pub node : Not Center {i}")
                    i += 1   
            else:
                # if current_message != previous_message:
                print(f"No contours detected: {i}")
                # pub_motor.publish(0)  # Stop if no contours are found
                # previous_message = current_message
                i += 1

        except Exception as e:
            print(f"Exception STOP: {e} {i}")
            # pub_motor.publish(0)
        
        key = cv2.waitKey(1)
        cv2.imshow('mask', img)
        if key & 0xff == ord('q'):
            break

        # rate.sleep()
    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    try:
        # rospy.init_node('cam_motor_control_pubnode', anonymous=True)
        # rospy.loginfo("Cam pub node : Start publishing")
        # pub_motor = rospy.Publisher('control_cam', Int32, queue_size=10)
        # rate = rospy.Rate(10)
        publish_message()
    except:
        print("Cam pub node : Stop publishing")

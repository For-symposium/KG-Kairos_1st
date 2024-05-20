import cv2
import numpy as np
import time
import subprocess
import rospy
from std_msgs.msg import Int32

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

    while not rospy.is_shutdown():
        # print("check 1")
        ret, img = cap.read()
        if not ret:
            break

        height, width, _ = img.shape
        # For Line tracing
        roi_height = height // 100 * 90
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
        offset = width // 4
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
                epsilon = 0.05 * cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, epsilon, True)

                # Find the top two points
                sorted_points = sorted(approx, key=lambda point: point[0][1])  # Sort by y-coordinate
                top_two_points = sorted_points[:2]  # Top two points

                for point in sorted_points:
                    x, y = point[0]
                    cv2.circle(roi, (x, y), 5, (255, 0, 0), -1)  # Blue circles

                # Calculate and print the distance along the x-axis
                if len(top_two_points) == 2:
                    x_distance = (top_two_points[0][0][0] - top_two_points[1][0][0])
                    # print(f"Distance: {top_two_points[0][0][0]} - {top_two_points[1][0][0]} = {x_distance}")

                    if len(approx) > 4 and abs(x_distance) > 20:
                        print("#####Switch to IR sensor mode#####")
                        # subprocess.run(["python3", path_to_subfile])
                        if x_distance > 0:
                            print("Cam pub : Zero turn dir Right")
                            pub_motor.publish(-117)
                            continue
                        else:
                            print("Cam pub : Zero turn dir : Left")
                            pub_motor.publish(-113)
                            continue
                    
                    # Update previous_x_distance
                    print(f"prev_dist = {previous_x_distance}, x_dist = {x_distance}")
                    previous_x_distance = x_distance

                # 4. Control the motors
                mid = (width - 2 * roi_width) // 2
                if mid - offset <= cx <= mid + offset:
                    dir_not_detected = cx
                    print(f"Cam Pub node : GO {i}")
                    i += 1
                    pub_motor.publish(10)
                elif cx < mid - offset:
                    dir_not_detected = cx
                    print(f"Cam Pub node : Left {i}")
                    i += 1
                    pub_motor.publish(-1)
                elif cx > mid + offset:
                    dir_not_detected = cx
                    print(f"Cam Pub node : Right {i}")
                    i += 1
                    pub_motor.publish(1)
            else:
                print(f"No contours detected: {i}")
                pub_motor.publish(0)  # Stop if no contours are found
                i += 1

        except Exception as e:
            print(f"Exception STOP: {e} {i}")
            pub_motor.publish(0)
        
        key = cv2.waitKey(1)
        cv2.imshow('mask', img)
        if key & 0xff == ord('q'):
            break
        rate.sleep()
    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    try:
        rospy.init_node('cam_motor_control_pubnode', anonymous=True)
        rospy.loginfo("Cam pub node : Start publishing")
        pub_motor = rospy.Publisher('control_cam', Int32, queue_size=10)
        rate = rospy.Rate(10)
        publish_message()
    except rospy.ROSInterruptException:
        print("Cam pub node : Stop publishing")

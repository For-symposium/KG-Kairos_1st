import cv2
import numpy as np
import time
import rospy
import threading
from std_msgs.msg import Int32

i = 0
switching_threshold = 0
Done_subscribed = False  # 상태 변수 추가
zero_turn_arr = []
back_zero_turn_arr = []
normal_pub_cam_mode = True
zero_turn_cam_mode = False
no_contour_stop_cnt = 0
no_contour_stop_threshold = 0

def publish_message():
    global switching_threshold, Done_subscribed, i, normal_pub_cam_mode, zero_turn_arr, zero_turn_cam_mode, no_contour_stop_cnt, no_contour_stop_threshold
    # start_point_IR = True
    
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return
    
    # cap = cv2.VideoCapture('/dev/video0')
    cap.set(3, 640)
    cap.set(4, 480)

    cx = 0
    cy = 0
    # switch_to_ir_count = 1
    available_switch_to_ir = True

    while not rospy.is_shutdown():
        if not Done_subscribed:
            print(f"Waiting for Website signal {i}")
            i += 1
            time.sleep(1)
            continue  # 구독 완료 전까지 퍼블리싱 루프를 대기
        
        ret, img = cap.read()
        if not ret:
            break

        height, width, _ = img.shape
        roi_height = height // 100 * 90
        roi_width = 0
        roi = img[roi_height:, roi_width:(width - roi_width)]

        img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        img_mask1 = cv2.inRange(img_cvt, np.array([22, 100, 100]), np.array([35, 255, 255]))
        cont_list, _ = cv2.findContours(img_mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        offset = width // 4
        try:
            if cont_list:
                c = max(cont_list, key=cv2.contourArea)
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                if normal_pub_cam_mode: # if only normal driving mode
                    print(f"Center point (Normal) : {cx}")
                    i += 1
                    cv2.drawContours(roi, c, -1, (0, 0, 255), 1)
                    cv2.circle(roi, (cx, cy), 5, (0, 255, 0), -1)

                    epsilon = 0.05 * cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, epsilon, True)

                    sorted_points = sorted(approx, key=lambda point: point[0][1])
                    top_two_points = sorted_points[:2]

                    for point in sorted_points:
                        x, y = point[0]
                        cv2.circle(roi, (x, y), 5, (255, 0, 0), -1)

                    ########## IR, Zero-turn mode ##########
                    if len(top_two_points) == 2:
                        # x_distance = (top_two_points[0][0][0] - top_two_points[1][0][0])
                        # print(f"previous : {previous_x_distance}, present : {x_distance}")
                        # previous_x_distance = x_distance

                        if len(approx) > 4 and available_switch_to_ir and len(zero_turn_arr) > 0: # State 1 : T-course OK + Check the zero turn
                            if zero_turn_arr.pop(0) == -1: # if zero turn timing
                                print(f"Cam pub : Switch to IR sensor mode and Zero turn Left {i}")
                                i += 1
                                # start_point_IR = False
                                pub_motor.publish(-109) # Go into IR mode and Zero turn Left
                                normal_pub_cam_mode = False # Stop Cam
                                available_switch_to_ir = False # Prevent from publishing multiple times
                                no_contour_stop_cnt += 1
                                time.sleep(2)
                                continue
                            elif zero_turn_arr.pop(0) == 1: # if zero turn timing
                                print(f"Cam pub : Switch to IR sensor mode and Zero turn Right {i}")
                                i += 1
                                # start_point_IR = False
                                pub_motor.publish(-111) # Go into IR mode and Zero turn Right
                                normal_pub_cam_mode = False # Stop Cam
                                available_switch_to_ir = False # Prevent from publishing multiple times
                                no_contour_stop_cnt += 1
                                time.sleep(2)
                                continue
                            elif zero_turn_arr.pop(0) == 0: # Pass -> Go straight to State 2
                                print(f"Cam pub : Pass T-course {i}")
                                i += 1
                                available_switch_to_ir = False # Prevent from publishing multiple times
                                no_contour_stop_cnt += 1
                        elif len(zero_turn_arr) == 0:
                            print(f"Cam pub : NO Zero turn array {i}")
                            i += 1
                            continue

                        elif len(approx) > 4 and available_switch_to_ir == False: # State 2 : T-course OK + Pass
                            sorted_points = sorted(approx, key=lambda point: point[0][1], reverse=True)
                            bottom_two_points = sorted_points[:2]
                            if len(bottom_two_points) == 2:
                                bottom_mid_x = (bottom_two_points[0][0][0] + bottom_two_points[1][0][0]) // 2
                                bottom_mid_y = (bottom_two_points[0][0][1] + bottom_two_points[1][0][1]) // 2
                                cv2.circle(roi, (bottom_mid_x, bottom_mid_y), 5, (0, 255, 255), -1)
                                # print(f"Bottom mid point: ({bottom_mid_x}, {bottom_mid_y})")
                                mid = (width - 2 * roi_width) // 2
                                center_x = (bottom_two_points[0][0][0] + bottom_two_points[1][0][0]) // 2
                                if mid - offset <= center_x <= mid + offset:
                                    print(f"Cam Pub node in PASS : GO {i}")
                                    i += 1
                                    pub_motor.publish(10)
                                elif center_x < mid - offset:
                                    print(f"Cam Pub node in PASS : Left {i}")
                                    i += 1
                                    pub_motor.publish(-1)
                                elif center_x > mid + offset:
                                    print(f"Cam Pub node in PASS : Right {i}")
                                    i += 1
                                    pub_motor.publish(1)

                        elif len(approx) == 4 and available_switch_to_ir == False: # State 0 : Normal driving case
                            mid = (width - 2 * roi_width) // 2
                            if mid - offset <= cx <= mid + offset:
                                print(f"Cam Pub node : GO {i}")
                                i += 1
                                available_switch_to_ir = True # Allow the possibility of switching IR
                                pub_motor.publish(10)
                            elif cx < mid - offset:
                                print(f"Cam Pub node : Left {i}")
                                i += 1
                                available_switch_to_ir = True # Allow the possibility of switching IR
                                pub_motor.publish(-1)
                            elif cx > mid + offset:
                                print(f"Cam Pub node : Right {i}")
                                i += 1
                                available_switch_to_ir = True # Allow the possibility of switching IR
                                pub_motor.publish(1)
                        print(f"available_switch_to_ir : {available_switch_to_ir}, len of approx : {len(approx)}")
                
                elif zero_turn_cam_mode: # Zero turn cam mode
                    print(f"Center point (Zero turn) : {cx}")
                    i += 1
                    cv2.drawContours(roi, c, -1, (0, 0, 255), 1)
                    cv2.circle(roi, (cx, cy), 5, (0, 255, 0), -1)

                    epsilon = 0.05 * cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, epsilon, True)
                    sorted_points = sorted(approx, key=lambda point: point[0][1])

                    for point in sorted_points:
                        x, y = point[0]
                        cv2.circle(roi, (x, y), 5, (255, 0, 0), -1)
                    
                    zero_turn_offset = width * 0.48 # if cam cannot detect it, reduce value
                    if len(approx) == 4:
                        if zero_turn_offset <= cx <= width - zero_turn_offset:
                            print(f"Cam Pub node : Zero turn STOP {i}")
                            i += 1
                            pub_motor.publish(-200) # Stop zero turn
                            zero_turn_cam_mode = False
                            normal_pub_cam_mode = True
                        else:
                            print(f"Cam Pub node : Do Zero turn until stop signal {i}")
                            i += 1

                else: # Neither normal driving mode and zero turn mode
                    print(f"CAM MODE FALSE {i}")
                    i += 1
            elif no_contour_stop_cnt == no_contour_stop_threshold: # No contour and Stop in front of the EV car
                pub_motor.publish(0)
                print(f"Stop in front of the EV car. Stop count: {no_contour_stop_cnt} / Stop threshold: {no_contour_stop_threshold} {i}")
                i += 1
                normal_pub_cam_mode = False
                ########## Change state to TOF sensor part ##########
                print(f"Change state to TOF sensor part {i}")
                i += 1
            else:
                pub_motor.publish(0)
                print(f"No contours detected: {i}")
                i += 1

        except Exception as e:
            print(f"Exception STOP: {e} {i}")
            pub_motor.publish(0)

        key = cv2.waitKey(5)
        cv2.imshow('mask', img)
        if key & 0xff == ord('q'):
            rospy.loginfo("Cam pub node : Finish subscribing")
            break
        rate.sleep()
    cv2.destroyAllWindows()
    cap.release()

def generate_zero_turn(data):
    global Done_subscribed, i, zero_turn_arr, back_zero_turn_arr, no_contour_stop_cnt, no_contour_stop_threshold
    # switching_threshold = data.data
    rospy.Subscriber('vehicle_position', Int32, generate_zero_turn).unregister() # Stop subscribing
    Done_subscribed = True  # Done subscribe from website
    if data.data == 13:
        zero_turn_arr = [-1, 0, 0, -1, 1, 1, 0, 0, 1, 1] # L P P L R R P P R R
        no_contour_stop_cnt = 0
        no_contour_stop_threshold = 4
    elif data.data == 22:
        zero_turn_arr = [1, 0, 1, -1, -1, 0, -1, -1] # R P R L L P L L
        no_contour_stop_cnt = 0
        no_contour_stop_threshold = 3
    else:
        print(f"Error! Generate zero turn! {i}")
        i += 1
    print(f"Receive from website, Zero turn array : {zero_turn_arr} {i}")
    i += 1
    time.sleep(1)

def control_cam_mode(data):
    global i, normal_pub_cam_mode, zero_turn_cam_mode
    if data.data == -1000:
        print(f"Control cam mode Function : Cam mode OFF {i}")
        i += 1
        normal_pub_cam_mode = False
    elif data.data == 1000:
        print(f"Control cam mode Function : Cam mode ON {i}")
        i += 1
        normal_pub_cam_mode = True
    elif data.data == 2000:
        print(f"Control cam mode Function : Zero turn Cam mode ON {i}")
        i += 1
        normal_pub_cam_mode = False
        zero_turn_cam_mode = True

def listener():
    global Done_subscribed
    rospy.loginfo("Cam pub node : Start subscribing")
    if not Done_subscribed:
        rospy.Subscriber('vehicle_position', Int32, generate_zero_turn) # Generate Zero turn array
    rospy.Subscriber('pub_control_cam', Int32, control_cam_mode) # Control cam mode
    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('cam_motor_control_pubnode', anonymous=True)
        rospy.loginfo("Cam pub node : Start publishing")
        # rospy.Subscriber('t_course_cnt', Int32, t_course_cnt) # line tracing 
        pub_motor = rospy.Publisher('control_cam', Int32, queue_size=10)
        rate = rospy.Rate(10)
        threading.Thread(target=listener).start()
        publish_message()

    except rospy.ROSInterruptException:
        print("Cam pub node : Stop publishing")


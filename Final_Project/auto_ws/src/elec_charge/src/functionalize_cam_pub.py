import cv2
import numpy as np
import time
import rospy
import threading
from std_msgs.msg import Int32

class CamMotorControl:
    def __init__(self):
        self.i = 0
        self.switching_threshold = 0
        self.Done_subscribed = False
        self.zero_turn_arr = []
        self.back_zero_turn_arr = []
        self.driving_cam_mode = True
        self.ir_mode = False
        self.zero_turn_cam_mode = False
        self.T_course_count = 0
        self.T_course_stop_threshold_departure = None
        self.T_course_stop_threshold_goback = None
        self.TOF_mode = False
        self.TOF_mode_pub = True
        self.epsilon_offset = 0.035
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.pub_motor = rospy.Publisher('control_cam', Int32, queue_size=1)
        self.pub_client = rospy.Publisher('client_message', Int32, queue_size=1)
        self.rate = rospy.Rate(10)
        self.roi_height = 0
        self.roi_width = 0
        self.available_switch_to_ir = True # Prevent from publishing multiple times
        self.all_false_mode = False
        self.after_charging_zero_turn_cam_mode = False
        
    def switching_modes(self, target_mode):
        if target_mode == 1:
            print("\ttarget_mode == self.driving_cam_mode")
            self.driving_cam_mode = True
            self.ir_mode = False
            self.zero_turn_cam_mode = False
            self.TOF_mode = False
            self.after_charging_zero_turn_cam_mode = False
        elif target_mode == 2:
            print("\ttarget_mode == self.ir_mode")
            self.driving_cam_mode = False
            self.ir_mode = True
            self.zero_turn_cam_mode = False
            self.TOF_mode = False
            self.after_charging_zero_turn_cam_mode = False
        elif target_mode == 3:
            print("\ttarget_mode == self.Start_zero_turn_cam_mode")
            self.driving_cam_mode = False
            self.ir_mode = False
            self.zero_turn_cam_mode = True
            self.TOF_mode = False
            self.after_charging_zero_turn_cam_mode = False
        elif target_mode == 4:
            print("\ttarget_mode == self.TOF_mode")
            self.driving_cam_mode = False
            self.ir_mode = False
            self.zero_turn_cam_mode = False
            self.TOF_mode = True
            self.after_charging_zero_turn_cam_mode = False
        elif target_mode == "after_charging_zero_turn_cam_mode":
            print("\ttarget_mode == self.End_zero_turn_cam_mode")
            self.driving_cam_mode = False
            self.ir_mode = False
            self.zero_turn_cam_mode = True
            self.TOF_mode = False
            self.after_charging_zero_turn_cam_mode = True
        elif target_mode == 0:
            print("\ttarget_mode == Waiting for another signal")
            self.driving_cam_mode = True
            self.ir_mode = False
            self.zero_turn_cam_mode = False
            self.TOF_mode = False
            self.after_charging_zero_turn_cam_mode = False

    def initialize_camera(self):
        if not self.cap.isOpened():
            print("Error: Unable to open camera")
            return False
        
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        return True

    def subscribe_topics(self):
        rospy.Subscriber('vehicle_position', Int32, self.from_web_signal)
        rospy.Subscriber('pub_control_cam', Int32, self.control_cam_mode)
        rospy.spin()
    
    def from_web_signal(self, data):
        if not self.Done_subscribed:
            rospy.Subscriber('vehicle_position', Int32, self.from_web_signal).unregister()
            self.Done_subscribed = True
            if data.data == 13:
                self.pub_client.publish(2)
                self.zero_turn_arr = [-1, 0, 0, -1, 1, 0, 0, 1, 1]
                # self.T_course_stop_threshold_departure = len(self.zero_turn_arr)
                self.T_course_stop_threshold_departure = 4
                self.T_course_stop_threshold_goback = len(self.zero_turn_arr)
            elif data.data == 22:
                self.pub_client.publish(2)
                # self.zero_turn_arr = [1, 0, 1, -1, 0, -1, -1]
                # self.T_course_stop_threshold_departure = 3
                self.zero_turn_arr = [0, -1]
                self.T_course_stop_threshold_departure = 3
                self.T_course_stop_threshold_goback = len(self.zero_turn_arr)
            else:
                print(f"Error! Generate zero turn! {self.i}")
                self.i += 1
            print(f"Receive from website, Start Zero turn array : {self.zero_turn_arr} {self.i}")
            self.i += 1

    def control_cam_mode(self, data):
        if data.data == 2000: # Start Zero turn cam
            print(f"Control cam mode Function : Zero turn Cam mode ON {self.i}")
            self.i += 1
            self.switching_modes(3) # Zero turn cam mode
        elif data.data == 2100:
            print(f"Control cam mode Function : After charging Zero turn Cam mode ON {self.i}")
            self.i += 1
            self.switching_modes("after_charging_zero_turn_cam_mode")

    def process_contours_0(self, cont_list, img, width, roi):
        # Control overall offset
        offset = width // 4
        c = max(cont_list, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        if self.driving_cam_mode:
            self.process_switch_mode_1(c, cx, cy, roi, width, offset)
        elif self.zero_turn_cam_mode:
            self.process_start_zero_turn_mode_2(c, cx, cy, roi, width, offset)
        elif self.ir_mode:
            print(f"IR_mode {self.i}")
            self.i += 1
        else:
            self.pub_motor.publish(3000)
            print(f"Nothing mode {self.i}")
            self.i += 1

    def process_switch_mode_1(self, c, cx, cy, roi, width, offset):
        print(f"Center point (Normal) : {cx}")
        self.i += 1
        cv2.drawContours(roi, c, -1, (0, 0, 255), 1)
        cv2.circle(roi, (cx, cy), 5, (0, 255, 0), -1)

        epsilon = self.epsilon_offset * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        sorted_points = sorted(approx, key=lambda point: point[0][1])
        top_two_points = sorted_points[:2]
        top_x_distance = abs(top_two_points[0][0][0] - top_two_points[1][0][0])

        sorted_points_reverse = sorted(approx, key=lambda point: point[0][1], reverse=True)
        bottom_two_points = sorted_points_reverse[:2]
        bottom_x_distance = abs(bottom_two_points[0][0][0] - bottom_two_points[1][0][0])

        if len(approx) <= 4:
            for point in sorted_points:
                x, y = point[0]
                cv2.circle(roi, (x, y), 5, (255, 0, 0), -1)
        else:
            for point in sorted_points:
                x, y = point[0]
                cv2.circle(roi, (x, y), 5, (0, 0, 255), -1)

        self.Switching_Normal_IR_Zeroturn_mode_1(roi, cx, approx, width, offset, top_x_distance, bottom_x_distance, top_two_points, bottom_two_points)

    def Switching_Normal_IR_Zeroturn_mode_1(self, roi, cx, approx, width, offset, top_x_distance, bottom_x_distance, top_two_points, bottom_two_points):
        if len(top_two_points) == 2:
            print(f"len of approx : {len(approx)}")
            print(f"Zero turn array: {self.zero_turn_arr}, count : {self.T_course_count}")

            # State 0 : Normal driving mode
            # Problem : after T-course, it detects only 4 approx. So it consider this situation as normal mode.
            # >> available_switch = True >> When it goes out, it consider this as the new T-course.
            if len(approx) == 4:
                self.normal_driving_case_1_0(cx, width, offset)

            # State 1 : T-course + Check the zero turn array
            elif (len(approx) > 5) and self.available_switch_to_ir:
                next_turn = self.zero_turn_arr.pop(0)
                print(f"\nNext turn value: {next_turn}")
                # Switch to IR mode and Zero turn : Left
                if next_turn == -1: 
                    self.execute_zero_turn_1_1(-109)
                # Switch to IR mode and Zero turn : Right
                elif next_turn == 1:
                    self.execute_zero_turn_1_1(-111)
                # Pass_1_2
                elif next_turn == 0:
                    print(f"Pass T-course {self.i}")
                    self.i += 1
                    self.T_course_count += 1
                    self.available_switch_to_ir = False
            
            # State 2 : While in the T-course
            elif len(approx) > 4 and self.available_switch_to_ir == False:
                self.pass_t_course_1_2(roi, cx, approx, width, offset, bottom_two_points)

            # For debugging
            # elif top_x_distance <= bottom_x_distance:
            #     self.Should_not_pop_array()

            # There is no zero turn case
            # elif len(self.zero_turn_arr) == 0:
            #     print(f"Cam pub : NO Zero turn array {self.i}")
            #     self.i += 1

    def normal_driving_case_1_0(self, cx, width, offset):
        mid = (width - 2 * self.roi_width) // 2
        if mid - offset <= cx <= mid + offset:
            print(f"Cam Pub node : GO {self.i}")
            self.i += 1
            self.pub_motor.publish(10)
            self.available_switch_to_ir = True
        elif cx < mid - offset:
            print(f"Cam Pub node : Left {self.i}")
            self.i += 1
            self.pub_motor.publish(-1)
            self.available_switch_to_ir = True
        elif cx > mid + offset:
            print(f"Cam Pub node : Right {self.i}")
            self.i += 1
            self.pub_motor.publish(1)
            self.available_switch_to_ir = True

    def execute_zero_turn_1_1(self, turn_command):
        print(f"Cam pub : Switch to IR sensor mode {self.i}")
        self.i += 1
        self.pub_motor.publish(turn_command)
        self.switching_modes(2) # IR mode
        self.available_switch_to_ir = False
        self.T_course_count += 1
        time.sleep(2)

    def pass_t_course_1_2(self, roi, cx, approx, width, offset, bottom_two_points):
        print(f"State 2 : T-course + Pass {self.i}")
        self.i += 1
        sorted_points = sorted(approx, key=lambda point: point[0][1], reverse=True)
        bottom_two_points = sorted_points[:2]
        if len(bottom_two_points) == 2:
            bottom_mid_x = (bottom_two_points[0][0][0] + bottom_two_points[1][0][0]) // 2
            bottom_mid_y = (bottom_two_points[0][0][1] + bottom_two_points[1][0][1]) // 2
            cv2.circle(roi, (bottom_mid_x, bottom_mid_y), 5, (255, 255, 0), -1)
            center_x = bottom_mid_x
            mid = (width - 2 * self.roi_width) // 2
            if mid - offset <= center_x <= mid + offset:
                print(f"Cam Pub node in PASS : GO {self.i}")
                self.i += 1
                self.pub_motor.publish(10)
            elif center_x < mid - offset:
                print(f"Cam Pub node in PASS : Left {self.i}")
                self.i += 1
                self.pub_motor.publish(-1)
            elif center_x > mid + offset:
                print(f"Cam Pub node in PASS : Right {self.i}")
                self.i += 1
                self.pub_motor.publish(1)

    def process_start_zero_turn_mode_2(self, c, cx, cy, roi, width, offset):
        zero_turn_offset = width * 0.48
        print(f"{zero_turn_offset} <= {cx} <= {width-zero_turn_offset}")
        print(f"Center point (Zero turn) : {cx}")
        self.i += 1
        cv2.drawContours(roi, c, -1, (0, 0, 255), 1)
        cv2.circle(roi, (cx, cy), 5, (0, 0, 255), -1)

        epsilon = self.epsilon_offset * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        sorted_points = sorted(approx, key=lambda point: point[0][1])

        for point in sorted_points:
            x, y = point[0]
            cv2.circle(roi, (x, y), 5, (255, 0, 0), -1)

        if len(approx) == 4:
            if zero_turn_offset <= cx <= width-zero_turn_offset:
                print(f"Cam Pub node : Zero turn STOP {self.i}")
                self.i += 1
                '''
                Additional func
                - Go back zero turn movement -> driving mode(-200), Stop at the starting point(all stop)
                '''
                if self.after_charging_zero_turn_cam_mode:
                    self.pub_motor.publish(-200) # Zero turn stop
                    self.switching_modes(1) # driving mode
                    print(f"\tAfter charging zero turn cam mode -> driving mode {self.i}")
                    self.i += 1
                    time.sleep(1)
                elif (self.T_course_count == self.T_course_stop_threshold_departure): # time to TOF
                    print(f"\tIn front of the EV. Now TOF part. {self.i}")
                    self.i += 1
                    self.switching_modes(4) # TOF mode
                    self.pub_motor.publish(-300) # TOF mode
                    time.sleep(1)
                elif self.T_course_count == self.T_course_stop_threshold_goback: # Stop at start point
                    print(f"\tI'm in the start point. Finished whole charging scenario.")
                    self.i += 1
                    self.Done_subscribed = False
                    self.T_course_count = 0
                    self.switching_modes(0) # Waiting for website signal
                    self.pub_motor.publish(3000) # All stop motor
                else:
                    self.pub_motor.publish(-200) # driving mode
                    self.switching_modes(1) # driving mode
                    print(f"\tReturn to normal driving mode")
                    time.sleep(1)
            else:
                print(f"Cam Pub node : Do Zero turn until stop signal {self.i}")
                self.i += 1

    def publish_message(self):
        if not self.cap.isOpened():
            print("Error: Unable to open camera")
            return False
        
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        offset1 = 0.57
        offset2 = 0.67

        while not rospy.is_shutdown():
            if not self.Done_subscribed:
                print(f"Waiting for Website signal {self.i}")
                self.i += 1
                time.sleep(1)
                continue

            ret, img = self.cap.read()
            if not ret:
                break

            height, width, _ = img.shape
            self.roi_height = round(height * 0.95)
            self.roi_width = 0
            # Change roi in order to apply the new position
            roi = img[height*offset1:height*offset2, self.roi_width:(width - self.roi_width)]
            img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            # Yellow line
            img_mask = cv2.inRange(img_cvt, np.array([22, 100, 100]), np.array([35, 255, 255]))
            # Black line
            # img_mask = cv2.inRange(img_cvt, np.array([0, 0, 0]), np.array([200, 120, 50]))
            cont_list, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            try:
                if self.TOF_mode:
                    print(f"Change State to TOF mode {self.i}")
                    self.i += 1
                elif cont_list:
                    self.process_contours_0(cont_list, img, width, roi)
                else:
                    self.pub_motor.publish(1)
                    print(f"No contours detected: {self.i}")
                    self.i += 1

            except Exception as e:
                print(f"Exception STOP: {e} {self.i}")
                self.pub_motor.publish(1)
                
            finally:
                key = cv2.waitKey(5)
                # cv2.imshow('mask', img)
                if key & 0xff == ord('q'):
                    rospy.loginfo("Cam pub node : Finish subscribing")
                    break
                self.rate.sleep()

        cv2.destroyAllWindows()
        self.cap.release()

if __name__ == '__main__':
    rospy.init_node('cam_motor_control_pubnode', anonymous=True)
    rospy.loginfo("Cam pub node : Start publishing")
    cam_motor_control = CamMotorControl()
    threading.Thread(target=cam_motor_control.subscribe_topics).start()
    cam_motor_control.publish_message()

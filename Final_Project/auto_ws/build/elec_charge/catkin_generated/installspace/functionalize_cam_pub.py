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
        self.zero_turn_cam_mode = False
        self.T_course_count = 0
        self.T_course_stop_threshold = 0
        self.TOF_mode = False
        self.epsilon_offset = 0.03
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.pub_motor = rospy.Publisher('control_cam', Int32, queue_size=10)
        self.rate = rospy.Rate(10)
        self.roi_height = 0
        self.roi_width = 0
        self.available_switch_to_ir = True # Prevent from publishing multiple times

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
                self.zero_turn_arr = [-1, 0, 0, -1, 1, 1, 0, 0, 1, 1]
                self.T_course_stop_threshold = 4
            elif data.data == 22:
                self.zero_turn_arr = [1, 0, 1, -1, -1, 0, -1, -1]
                self.T_course_stop_threshold = 3
            else:
                print(f"Error! Generate zero turn! {self.i}")
                self.i += 1
            print(f"Receive from website, Zero turn array : {self.zero_turn_arr} {self.i}")
            self.i += 1
            time.sleep(1)

    def control_cam_mode(self, data):
        if data.data == -1000:
            print(f"Control cam mode Function : Cam mode OFF {self.i}")
            self.i += 1
            self.driving_cam_mode = False
        elif data.data == 1000:
            print(f"Control cam mode Function : Cam mode ON {self.i}")
            self.i += 1
            self.driving_cam_mode = True
        elif data.data == 2000:
            print(f"Control cam mode Function : Zero turn Cam mode ON {self.i}")
            self.i += 1
            self.driving_cam_mode = False
            self.zero_turn_cam_mode = True

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
            self.process_zero_turn_mode_2(c, cx, cy, roi, width, offset)
        else:
            self.pub_motor.publish(0)
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
            elif top_x_distance <= bottom_x_distance:
                self.Should_not_pop_array()

            # There is no zero turn case
            elif len(self.zero_turn_arr) == 0:
                print(f"Cam pub : NO Zero turn array {self.i}")
                self.i += 1
                return

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
        self.driving_cam_mode = False
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

    def Should_not_pop_array(self):
        print(f"Should not pop zero turn array!! Just Go. {self.i}")
        self.i += 1
        self.pub_motor.publish(10)

    def process_zero_turn_mode_2(self, c, cx, cy, roi, width, offset):
        zero_turn_offset = width * 0.49
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
                self.pub_motor.publish(-200)
                self.zero_turn_cam_mode = False
                self.driving_cam_mode = True
                if self.T_course_count == self.T_course_stop_threshold:
                    print(f"\nIn front of the EV. Now TOF part. {self.i}")
                    self.TOF_mode = True
                    time.sleep(2)
            else:
                print(f"Cam Pub node : Do Zero turn until stop signal {self.i}")
                self.i += 1

    def publish_message(self):
        if not self.cap.isOpened():
            print("Error: Unable to open camera")
            return False
        
        self.cap.set(3, 640)
        self.cap.set(4, 480)

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
            roi = img[self.roi_height:, self.roi_width:(width - self.roi_width)]
            img_cvt = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            # Yellow line
            # img_mask = cv2.inRange(img_cvt, np.array([22, 100, 100]), np.array([35, 255, 255]))
            # Black line
            img_mask = cv2.inRange(img_cvt, np.array([0, 0, 0]), np.array([200, 120, 50]))
            cont_list, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            try:
                if self.TOF_mode:
                    print(f"Change State to TOF mode {self.i}")
                    self.i += 1
                    self.pub_motor.publish(-300)
                elif cont_list:
                    self.process_contours_0(cont_list, img, width, roi)
                else:
                    self.pub_motor.publish(0)
                    print(f"No contours detected: {self.i}")
                    self.i += 1

            except Exception as e:
                print(f"Exception STOP: {e} {self.i}")
                self.pub_motor.publish(0)
                
            finally:
                key = cv2.waitKey(5)
                cv2.imshow('mask', img)
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

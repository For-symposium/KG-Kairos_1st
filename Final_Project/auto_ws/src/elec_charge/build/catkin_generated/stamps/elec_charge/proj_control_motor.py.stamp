'''
< Data signals >

1. OpenCV Line-tracing
    - 10 : GO
    - -1 : Left
    - 1 : Right
    - 0 : STOP

2. IR sensor
    - 10 : GO
    - 0 : STOP

3. IR sensor to Zero turn
    - 101 : Right
    - 99 : Left

4. TOF mode
    - 10 : GO
    - -1 : Left
    - 1 : Right
    - 0 : STOP

- -100 : Cam mode ON
- -109 : IR mode ON -> Zero-turn Left signal
- -111 : IR mode ON -> Zero-turn Right signal
- -120 : Zero turn mode ON using signal
- -200 : Zero turn STOP
- -300 : TOF mode ON
- 400 : Robotarm ON
- -400 : Robotarm OFF -> Zero-turn on

- 2000 : Zero turn Cam mode ON
'''
'''
Normally
    - Cam mode ON
When encountered T-course
    - Cam mode OFF
    - Store the zero-turn direction
Zero-turn
    - Should not Distracked by any command
    - If done, go back to Cam mode

Enable T-course to Zero-turn
'''
import rospy
import time
from std_msgs.msg import Int32

class MainControlMotor:
    def __init__(self):
        self.i = 0
        self.cam_mode = True
        self.ir_mode = False
        self.zero_turn_mode = False
        self.zero_turn_dir = 0  # Left(-1), Right(1)
        self.zero_turn_stop = False
        self.tof_mode = False
        self.robotarm_mode = False
        self.tof_cnt = 0
        self.manual_mode = False

        self.pub_control_cam = rospy.Publisher('pub_control_cam', Int32, queue_size=1)  # Control Cam mode
        self.pub_robotarm = rospy.Publisher('pub_robotarm', Int32, queue_size=1)  # Enable robotarm

    def set_modes(self, select_mode):
        if select_mode == 1:
            self.cam_mode = True
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = False
        elif select_mode == 2:
            self.cam_mode = False
            self.ir_mode = True
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = False
        elif select_mode == 3:
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = True
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = False
        elif select_mode == 4:
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = True
            self.robotarm_mode = False
            self.manual_mode = False
        elif select_mode == 5:
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = True
            self.manual_mode = False
        else:
            print("No selected set modes")
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = True

    def cam_mode_control(self, cam_data):
        if cam_data == 10:
            self.log("Cam Sub : GO")
            # STM32 motor control
        elif cam_data == 1:
            self.log("Cam Sub : Right")
            # STM32 motor control
        elif cam_data == -1:
            self.log("Cam Sub : Left")
            # STM32 motor control
        elif cam_data == 0:
            self.log("Cam Sub : STOP")
            # STM32 motor control

        if cam_data == -109:
            self.zero_turn_dir = -1  # Zero turn Left
            self.set_modes(2)  # ir_mode
            self.log("Cam Sub : Switch to IR mode and Zero turn dir is Left")
        elif cam_data == -111:
            self.zero_turn_dir = 1  # Zero turn Right
            self.set_modes(2)  # ir_mode
            self.log("Cam Sub : Switch to IR mode and Zero turn dir is Right")

    def cam_motor_control_callback(self, data):
        if self.cam_mode:
            self.cam_mode_control(data.data)
        elif data.data == -200:  # Zero turn stop
            self.zero_turn_stop = True
            self.set_modes(1)  # cam_mode
        elif data.data == -300:  # go to TOF mode
            self.zero_turn_stop = True
            self.set_modes(4)  # tof_mode

    def IR_motor_control_callback(self, data):
        if self.ir_mode:
            if data.data == 10:
                self.log("IR Sub : GO")
                # STM32 motor control
            elif data.data == -120:
                self.log("IR Sub : Do Zero turn")
                self.pub_control_cam.publish(2000)  # Zero turn cam mode ON
                self.set_modes(3)  # zero_turn_mode
        elif self.zero_turn_mode:
            self.Zero_turn_control(self.zero_turn_dir)

    def Zero_turn_control(self, dir):
        if dir == -1:
            self.log("Zero turn Sub : Turn Left")
            # STM32 motor control
        elif dir == 1:
            self.log("Zero turn Sub : Turn Right")
            # STM32 motor control
        if self.zero_turn_stop: # if come to center
            if self.tof_mode:
                self.zero_turn_mode = False
                self.log("Zero turn Sub : TOF mode ON")
            elif self.cam_mode: # Again to Normal mode
                self.zero_turn_mode = False
                self.log("Zero turn Sub : Zero turn STOP // Normal Cam Mode ON")

    def TOF_control_callback(self, data):
        if self.tof_mode:
            if data.data == 10:
                # STM32 motor control
                self.log("TOF Sub : GO")
            # elif data.data == -1:
            #     # STM32 motor control
            #     self.log("TOF Sub : Left")
            # elif data.data == 1:
            #     # STM32 motor control
            #     self.log("TOF Sub : Right")
            # elif data.data == 0:
            #     # STM32 motor control
            #     self.log("TOF Sub : STOP")
                self.tof_cnt += 1
            if self.tof_cnt == 5:
                self.pub_robotarm.publish(400)
                self.set_modes(5)  # robotarm_mode
                self.log("Robotarm mode ON")

    def robotarm_callback(self, data):
        if self.robotarm_mode:
            if data.data == -400:  # Done Charging from robotarm 
                self.log("Robotarm mode OFF")
                self.robotarm_mode = False
                self.tof_mode = False

    def listener(self):
        rospy.loginfo("Sub node : Start Subscribing")
        rospy.Subscriber('control_cam', Int32, self.cam_motor_control_callback)
        rospy.Subscriber('control_IR', Int32, self.IR_motor_control_callback)
        rospy.Subscriber('control_TOF', Int32, self.TOF_control_callback)
        rospy.Subscriber('control_robotarm', Int32, self.robotarm_callback)
        rospy.on_shutdown(self.clean_up)
        rospy.spin()

    def clean_up(self):
        rospy.loginfo("Sub node: Cleaning up...")

    def log(self, message):
        self.i += 1
        print(f"{message} {self.i}")

if __name__ == '__main__':
    try:
        rospy.init_node('motor_control_sub_node', anonymous=True)
        main_control_motor = MainControlMotor()
        main_control_motor.listener()
    except rospy.ROSInterruptException:
        print("ROSInterruptException")

import rospy
import time
from std_msgs.msg import Int32, String
import serial
import threading

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
        self.after_charging_zero_turn_mode = False

        self.pub_control_cam = rospy.Publisher('pub_control_cam', Int32, queue_size=1)  # Control Cam mode
        self.pub_robotarm = rospy.Publisher('pub_robotarm', Int32, queue_size=1)  # Enable robotarm

        self.serial_thread = threading.Thread(target=self.read_serial_data)
        self.serial_thread.daemon = True
        self.serial_thread.start()

    def set_modes(self, select_mode):
        if select_mode == 1:
            print("\tSet_modes : Cam_mode ON")
            self.cam_mode = True
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = False
            self.after_charging_zero_turn_mode = False
        elif select_mode == 2:
            print("\tSet_modes : IR_mode ON")
            self.cam_mode = False
            self.ir_mode = True
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = False
            self.after_charging_zero_turn_mode = False
        elif select_mode == 3:
            print("\tSet_modes : Zero_turn_mode ON")
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = True
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = False
            self.after_charging_zero_turn_mode = False
        elif select_mode == 4:
            print("\tSet_modes : TOF_mode ON")
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = True
            self.robotarm_mode = False
            self.manual_mode = False
            self.after_charging_zero_turn_mode = False
        elif select_mode == 5:
            print("\tSet_modes : Robotarm_mode ON")
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = True
            self.manual_mode = False
            self.after_charging_zero_turn_mode = False
        elif select_mode == "after_charging_zero_turn_mode":
            print("\tSet_modes : After Charging zero turn ON")
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = False
            self.after_charging_zero_turn_mode = True
        elif select_mode == "manual_mode":
            print("\tSet_modes : Manual mode")
            self.cam_mode = False
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = True
            self.after_charging_zero_turn_mode = False
        elif select_mode == 3000:
            print("\tSet_modes : Arrive at the starting point!")
            self.cam_mode = True
            self.ir_mode = False
            self.zero_turn_mode = False
            self.tof_mode = False
            self.robotarm_mode = False
            self.manual_mode = False
            self.after_charging_zero_turn_mode = False

    def cam_mode_control(self, cam_data):
        if cam_data == 10:
            self.log("Cam Sub : GO")
            # STM32 motor control
            self.send_data(11)
        elif cam_data == 1:
            self.log("Cam Sub : Right")
            # STM32 motor control
            self.send_data(14)
        elif cam_data == -1:
            self.log("Cam Sub : Left")
            # STM32 motor control
            self.send_data(13)
        elif cam_data == 0:
            self.log("Cam Sub : STOP")
            # STM32 motor control
            self.send_data(2)

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
        elif data.data == 3000: # All stop
            self.set_modes(3000)
            self.send_data(1) # All motor initialize

    def IR_motor_control_callback(self, data):
        if self.ir_mode:
            if data.data == 10:
                self.log("IR Sub : GO")
                # STM32 motor control
                self.send_data(11)
            elif data.data == -120:
                self.log("IR Sub : Do Zero turn")
                self.pub_control_cam.publish(2000)  # Zero turn cam mode ON
                self.set_modes(3)  # Zero_turn_mode
        elif self.zero_turn_mode:
            self.Zero_turn_control(self.zero_turn_dir)

    def Zero_turn_control(self, dir):
        if dir == -1:
            self.log("Zero_turn_control : Zero turn Sub : Turn Left")
            # STM32 motor control
            self.send_data(9)
        elif dir == 1:
            self.log("Zero_turn_control : Zero turn Sub : Turn Right")
            # STM32 motor control
            self.send_data(10)
        elif dir == 0: # after charging
            self.log("Zero_turn_control : After charge Zero turn")
            # STM32 motor control
            self.send_data(9)
        if self.zero_turn_stop: # if come to center
            if self.tof_mode:
                self.zero_turn_mode = False
                self.zero_turn_stop = False # Initialize zero_turn_stop
                self.log("Zero_turn_control : TOF mode ON")
            elif self.cam_mode: # Again to Normal mode
                self.zero_turn_mode = False
                self.zero_turn_stop = False # Initialize zero_turn_stop
                self.log("Zero_turn_control : Zero turn STOP // Normal Cam Mode ON")

    def TOF_control_callback(self, data):
        if self.tof_mode:
            if data.data == 10:
                self.send_data(11)
                self.log("TOF Sub : GO")
            elif data.data == -1:
                self.send_data(13)
                self.log("TOF Sub : Left")
            elif data.data == 1:
                self.send_data(14)
                self.log("TOF Sub : Right")
            elif data.data == 0:
                self.send_data(1)
                self.set_modes(5)  # robotarm_mode
                self.log("TOF Sub : STOP and Robotarm mode ON")
                self.pub_robotarm.publish(400) # send robotarm to Run
                self.tof_cnt += 1
            if self.tof_cnt == 20:
                self.send_data(1)  # Align motors before changing mode
                self.pub_robotarm.publish(400)
                self.set_modes(5)  # robotarm_mode
                self.log("Robotarm mode ON")

    def robotarm_callback(self, data):
        if self.robotarm_mode:
            if data.data == -400:  # Done Charging from robotarm 
                self.log("Robotarm mode OFF")
                time.sleep(2)
                self.pub_control_cam.publish(2100)  # Just Zero turn cam mode ON
                self.set_modes("after_charging_zero_turn_mode")
                self.send_data(1) # Align motors before changing mode
                self.after_charging()

    def after_charging(self): # for only one zero turn after charging
        while self.after_charging_zero_turn_mode:
            self.Zero_turn_control(0)
            self.log("After charge zero turn while find line")
            if self.zero_turn_stop: # Q. Can it receive the subscriber when in while sentence?
                self.log("\tComplete after charging zero turn")
                self.set_modes(1) # Go to normal mode
                break
    
    def manual_control_callback(self, data):
        manual_control_mode = int(data.data[0])
        if manual_control_mode == 1:
            control_code = int(data.data[1:])
            self.log("Manual mode")
            self.set_modes("manual_mode")
            self.send_data(control_code)
        else:
            self.log("Quit manual mode")
            self.set_modes(1)
    
    def send_data(self, data):
        byte_code = data.to_bytes(1, byteorder='big')
        ser.write(byte_code)
        self.log(f"Send data {data}")
        pass

    def read_serial_data(self):
        while not rospy.is_shutdown():
            if ser.in_waiting > 0:
                serial_data = ser.read().decode('utf-8', errors='ignore')
                if serial_data:
                    print(f"Received serial data: {serial_data}")

    def listener(self):
        rospy.loginfo("Sub node : Start Subscribing")
        rospy.Subscriber('control_cam', Int32, self.cam_motor_control_callback)
        rospy.Subscriber('control_IR', Int32, self.IR_motor_control_callback)
        rospy.Subscriber('control_TOF', Int32, self.TOF_control_callback)
        rospy.Subscriber('control_robotarm', Int32, self.robotarm_callback)
        rospy.Subscriber('control_manual', String, self.manual_control_callback)
        rospy.on_shutdown(self.clean_up)
        rospy.spin()

    def clean_up(self):
        self.send_data(1)
        rospy.loginfo("Sub node: Cleaning up...")

    def log(self, message):
        self.i += 1
        print(f"{message} {self.i}")

if __name__ == '__main__':
    try:
        rospy.init_node('motor_control_sub_node', anonymous=True)
        port = "/dev/ttyUSB1"
        baudrate = 9600
        ser = serial.Serial(port, baudrate, timeout=1)
        main_control_motor = MainControlMotor()
        main_control_motor.listener()
    except rospy.ROSInterruptException:
        print("ROSInterruptException")
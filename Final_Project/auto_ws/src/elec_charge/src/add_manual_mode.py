#!/usr/bin/env python3
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

- -100 : Cam mode ON, Others OFF
- -113 : IR mode ON, Others OFF, Zero-turn Left
- -117 : IR mode ON, Others OFF, Zero-turn Right
- -120 : Zero-turn mode ON, Others OFF
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
'''
import rospy
import time
from std_msgs.msg import Int32, String
import serial
import threading

i = 0
cam_mode = True
zero_turn_mode = False
zero_turn_dir = 0 # Left(-1), Right(1)
IR_mode = False
manual_control_mode = False
ser = None
control_code = 1  # Initialize control bit
rate = None  # Define rate globally to use in callbacks

def cam_motor_control_callback(data):
    global i, cam_mode, zero_turn_dir, zero_turn_mode, control_code, IR_mode
    if cam_mode == True:
        if data.data == 10:
            print(f"Cam Sub : GO {i}")
            i += 1
            # mc.go_ahead(1)
            control_code = 11
            send_data(control_code)
        elif data.data == 1:
            print(f"Cam Sub : Right {i}")
            i += 1
            # mc.clockwise_rotation(1)
            control_code = 14
            send_data(control_code)
        elif data.data == -1:
            print(f"Cam Sub : Left {i}")
            i += 1
            # mc.counterclockwise_rotation(1)
            control_code = 13
            send_data(control_code)
        elif data.data == 0:
            print(f"Cam Sub : STOP {i}")
            i += 1
            # mc.stop()
            control_code = 2
            send_data(control_code)
        rate.sleep()
        if data.data == -113:
            print(f"Cam Sub : Switch to IR mode && Zero-turn Left {i}")
            i += 1
            cam_mode = False
            IR_mode = True
            zero_turn_dir = -1
        elif data.data == -117:
            print(f"Cam Sub : Switch to IR mode && Zero-turn Right {i}")
            i += 1
            cam_mode = False
            IR_mode = True
            zero_turn_dir = 1
        # rate.sleep()


def IR_motor_control_callback(data):
    global i, cam_mode, zero_turn_dir, zero_turn_mode, control_code, rate, IR_mode
    if cam_mode == False and IR_mode == True and zero_turn_mode == False:
        if data.data == 10:
            print(f"IR Sub : GO {i}")
            i += 1
            # mc.go_ahead(1)
            control_code = 11
            send_data(control_code)
        elif data.data == 0:
            print(f"IR Sub : All white. STOP {i}")
            i += 1
            zero_turn_mode = True
            # mc.stop()
            control_code = 2
            send_data(control_code)
        # rate.sleep()
    if cam_mode == False and IR_mode == True and zero_turn_mode == True:
        ##### Zero-turn by hard-coding #####
        if zero_turn_dir == -1:
            print(f"Zero turn Sub : Turn Left {i}")
            i += 1
            control_code = 9 ###counterclockwise
            send_data(control_code)
            time.sleep(5)
            IR_mode, zero_turn_mode, cam_mode = False, False, True
        elif zero_turn_dir == 1:
            print(f"Zero turn Sub : Turn Right {i}")
            i += 1
            control_code = 10 ###clockwise
            send_data(control_code)
            time.sleep(5)
            IR_mode, zero_turn_mode, cam_mode = False, False, True
        # rate.sleep()

def manual_control_callback(data):
    global i, cam_mode, IR_mode, manual_control_mode, control_code
    manual_control_mode = int(data.data[0])

    if manual_control_mode == 1:
        cam_mode, IR_mode = False, False

        control_code = int(data.data[1:])
        rospy.loginfo(f"manual mode sub: {control_code}")
        i += 1
        
        send_data(control_code)
    else :
        cam_mode, IR_mode = True, False
        rospy.loginfo("Quit manual control mode")
        control_code = 1
        send_data(control_code)


def t_callback(data):
    rospy.loginfo(f"t_count: {data.data}")


def clean_up():
    rospy.loginfo("Sub node: Cleaning up...")
    # mc.stop()

def listener():
    # rospy.init_node('motor_control_sub_node', anonymous=True)
    rospy.loginfo("Sub node : Start Subscribing")
    rospy.Subscriber('control_cam', Int32, cam_motor_control_callback, queue_size=10) # line tracing
    rospy.Subscriber('control_IR', Int32, IR_motor_control_callback) # line tracing
    rospy.Subscriber('control_mode', String, manual_control_callback)
    rospy.Subscriber('t_count', Int32, t_callback)
    rospy.on_shutdown(clean_up)
    # rospy.spin()  # Keep away from exiting

def send_data(control_code):
    ser.write(control_code)
    rospy.loginfo(f"Sending: {control_code}")

if __name__ == '__main__':
    try:
        rospy.init_node('motor_control_sub_node', anonymous=True)
        rospy.loginfo(f"serial connetected")

        rate = rospy.Rate(10)
        port = "/dev/ttyUSB1"
        baudrate = 9600
        ser = serial.Serial(port, baudrate, timeout=1)
        thread = threading.Thread(target=send_data(control_code))
        thread.start()
        listener()

        rospy.spin()

    except rospy.ROSInterruptException:
        print("Sub motor node : STOP")


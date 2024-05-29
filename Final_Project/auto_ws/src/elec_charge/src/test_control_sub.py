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
- -110 : IR mode ON
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

Enable T-course to Zero-turn
'''
import rospy
import time
from std_msgs.msg import Int32
import serial
import threading

i = 0
cam_mode = True
zero_turn_mode = False
zero_turn_dir = 0 # Left(-1), Right(1)
zero_turn_arr = []
t_course_cnt = 0
ser = None
control_bit = "00000000"  # Initialize control bit
rate = None  # Define rate globally to use in callbacks

def cam_motor_control_callback(data):
    global i, cam_mode, zero_turn_dir, zero_turn_mode, control_bit
    if cam_mode == True:
        if data.data == 10:
            print(f"Cam Sub : GO {i}")
            i += 1
            control_bit = "11110001"
            # send_data(control_bit)
        elif data.data == 1:
            print(f"Cam Sub : Right {i}")
            i += 1
            control_bit = "11100000"
            # send_data(control_bit)
        elif data.data == -1:
            print(f"Cam Sub : Left {i}")
            i += 1
            control_bit = "01010001"
            # send_data(control_bit)
        elif data.data == 0:
            print(f"Cam Sub : STOP {i}")
            i += 1
            control_bit = "00110001"
            # send_data(control_bit)
        rate.sleep()
        if data.data == -110:
            print(f"Cam Sub : Switch to IR mode {i}")
            i += 1
            cam_mode = False
        rate.sleep()


def IR_motor_control_callback(data):
    global i, cam_mode, zero_turn_dir, zero_turn_mode, control_bit, rate
    if cam_mode == False and zero_turn_mode == False:
        if data.data == 10:
            print(f"IR Sub : GO {i}")
            i += 1
            control_bit = "11110001"
            # send_data(control_bit)
        elif data.data == 0:
            print(f"IR Sub : All white. STOP {i}")
            i += 1
            zero_turn_mode = True
            control_bit = "00110001"
            # send_data(control_bit)
        rate.sleep()
    if cam_mode == False and zero_turn_mode == True:
        ##### Zero-turn by hard-coding #####
        if zero_turn_dir == -1:
            print(f"Zero turn Sub : Turn Left {i}")
            i += 1
            control_bit = "10010001"
            # send_data(control_bit)
            time.sleep(5)
            zero_turn_mode, cam_mode = False, True
        elif zero_turn_dir == 1:
            print(f"Zero turn Sub : Turn Right {i}")
            i += 1
            control_bit = "10100001"
            # send_data(control_bit)
            time.sleep(5)
            zero_turn_mode, cam_mode = False, True
        rate.sleep()

def generate_zeroturn_arr(data):
    global zero_turn_arr, t_course_cnt
    # Zero turn direction
    if data.data // 10 == 1: # Left 11, 12, 13
        zero_turn_arr = [-1, -1, 1, 1] # LLRR
    elif data.data // 10 == 2: # Right 21, 22
        zero_turn_arr = [1, 1, -1, -1] # RRLL
    # T-course count
    t_course_cnt = data.data % 10
    pub_t_course_cnt.publish(t_course_cnt)

def clean_up():
    rospy.loginfo("Sub node: Cleaning up...")

def listener():
    rospy.init_node('motor_control_node', anonymous=True)
    rospy.loginfo("Sub node : Start Subscribing")
    rospy.Subscriber('control_cam', Int32, cam_motor_control_callback, queue_size=10) # line tracing
    rospy.Subscriber('control_IR', Int32, IR_motor_control_callback) # line tracing
    rospy.Subscriber('vehicle_position', Int32, generate_zeroturn_arr) # receive EV position
    rospy.on_shutdown(clean_up)
    rospy.spin()  # Keep away from exiting

def send_data(control_bit):
    int_data = int(control_bit, 2)
    byte_data = int_data.to_bytes(1, byteorder='big')
    # ser.write(byte_data)
    rospy.loginfo(f"Sending: {bin(int_data)[2:].zfill(8)}")

if __name__ == '__main__':
    try:
        rospy.init_node('motor_control_sub_node', anonymous=True)
        rospy.loginfo(f"serial connetected")
        rate = rospy.Rate(10)
        # port = "/dev/ttyUSB0"
        # baudrate = 9600
        # ser = serial.Serial(port, baudrate, timeout=1)
        # threading.Thread(target=send_data(control_bit)).start()
        pub_t_course_cnt = rospy.Publisher('t_course_cnt', Int32, queue_size=10) # T-course count
        listener()
        rospy.spin()

    except rospy.ROSInterruptException:
        print("Sub motor node : STOP")
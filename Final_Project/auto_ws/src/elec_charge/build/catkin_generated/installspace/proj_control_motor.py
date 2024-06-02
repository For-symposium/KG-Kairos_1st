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

- -1000 : Stop publishing signal to cam_pub
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

i = 0
cam_mode = True
zero_turn_mode = False
zero_turn_dir = 0 # Left(-1), Right(1)
zero_turn_stop = False
# ser = None
control_bit = "00000000"  # Initialize control bit
rate = None  # Define rate globally to use in callbacks
web_sub = True
TOF_mode = False
robotarm_mode = False
tof_cnt = 0

def cam_mode_control(cam_data):
    global i, cam_mode, zero_turn_dir
    if cam_data == 10:
        print(f"Cam Sub : GO {i}")
        i += 1
        control_bit = "11110001"
        # send_data(control_bit)
    elif cam_data == 1:
        print(f"Cam Sub : Right {i}")
        i += 1
        control_bit = "11100000"
        # send_data(control_bit)
    elif cam_data == -1:
        print(f"Cam Sub : Left {i}")
        i += 1
        control_bit = "01010001"
        # send_data(control_bit)
    elif cam_data == 0:
        print(f"Cam Sub : STOP {i}")
        i += 1
        control_bit = "00110001"
        # send_data(control_bit)
    if cam_data == -109:
        cam_mode = False
        zero_turn_dir = -1 # Zero turn Left
        pub_control_cam.publish(-1000) # Unable cam publishing
        print(f"Cam Sub : Switch to IR mode and Zero turn dir is Left {i}")
        i += 1
    elif cam_data == -111:
        cam_mode = False
        zero_turn_dir = 1 # Zero turn Right
        pub_control_cam.publish(-1000) # Unable cam publishing
        print(f"Cam Sub : Switch to IR mode and Zero turn dir is Right {i}")
        i += 1

def cam_motor_control_callback(data):
    global i, cam_mode, zero_turn_dir, zero_turn_mode, control_bit, zero_turn_stop, TOF_mode
    if cam_mode == True:
        cam_mode_control(data.data)
    elif data.data == -200:
        zero_turn_stop = True
    elif data.data == -300:
        TOF_mode = True
        cam_mode = False

def IR_motor_control_callback(data):
    global i, cam_mode, zero_turn_dir, zero_turn_mode, control_bit, rate, zero_turn_stop
    if TOF_mode == False:
        if cam_mode == False and zero_turn_mode == False:
            if data.data == 10:
                print(f"IR Sub : GO {i}")
                i += 1
                control_bit = "11110001"
                # send_data(control_bit)
            elif data.data == -120:
                print(f"IR Sub : Do Zero turn {i}")
                i += 1
                zero_turn_mode = True
                pub_control_cam.publish(2000) # Zero turn cam mode ON
        elif cam_mode == False and zero_turn_mode == True:
            Zero_turn_control(zero_turn_dir)

def Zero_turn_control(dir):
    global i, zero_turn_mode, cam_mode
    if dir == -1:
        print(f"Zero turn Sub : Turn Left {i}")
        i += 1
        ###############################
        ########## Zero turn ##########
        ###############################
        # 1. Signal to STM32 Zero turn Left
        # 2. If camera cx is center, Stop signal
        if zero_turn_stop:
            if TOF_mode:
                zero_turn_mode = False
                print(f"Zero turn Sub : TOF mode ON {i}")
            else:
                zero_turn_mode = False
                # 3. Switch to cam mode again
                cam_mode = True
                pub_control_cam.publish(1000) # After zero turn, Enable cam publishing
                print(f"Zero turn Sub : Zero turn STOP // Normal Cam Mode ON {i}")
                i += 1
    elif dir == 1:
        print(f"Zero turn Sub : Turn Right {i}")
        i += 1
        ###############################
        ########## Zero turn ##########
        ###############################
        # 1. Signal to STM32 Zero turn Right
        # 2. If camera cx is center, Stop signal
        if zero_turn_stop:
            if TOF_mode:
                zero_turn_mode = False
                print(f"Zero turn Sub : TOF mode ON {i}")
            else:
                zero_turn_mode = False
                # 3. Switch to cam mode again
                cam_mode = True
                pub_control_cam.publish(1000) # After zero turn, Enable cam publishing
                print(f"Zero turn Sub : Zero turn STOP // Normal Cam Mode ON {i}")
                i += 1

def TOF_control_callback(data):
    global i, robotarm_mode, TOF_mode, tof_cnt
    if cam_mode == False and TOF_mode == True and robotarm_mode == False:
        tof_cnt += 1
        if data.data == 10:
            print(f"TOF Sub : GO {i}")
            i += 1
            # send signal to STM32
        elif data.data == -1:
            print(f"TOF Sub : Left {i}")
            i += 1
            # send signal to STM32
        elif data.data == 1:
            print(f"TOF Sub : Right {i}")
            i += 1
            # send signal to STM32
        elif data.data == 0:
            print(f"TOF Sub : Stop {i}")
            i += 1
            # send signal to STM32
        if tof_cnt == 15:
            robotarm_mode = True
            pub_robotarm.publish(400)
            print(f"\nRobotarm mode ON\n")
            
def robotarm_callback(data):
    global i, robotarm_mode, TOF_mode
    if data.data == -400:
        print(f"##### Robotarm mode OFF {i} #####")
        i += 1
        # Should change mode properly
        robotarm_mode = False
        TOF_mode = False

def clean_up():
    rospy.loginfo("Sub node: Cleaning up...")

def listener():
    rospy.loginfo("Sub node : Start Subscribing")
    rospy.Subscriber('control_cam', Int32, cam_motor_control_callback)
    rospy.Subscriber('control_IR', Int32, IR_motor_control_callback)
    rospy.Subscriber('control_TOF', Int32, TOF_control_callback)
    rospy.Subscriber('control_robotarm', Int32, robotarm_callback)
    rospy.on_shutdown(clean_up)
    rospy.spin()

def send_data(control_bit):
    int_data = int(control_bit, 2)
    byte_data = int_data.to_bytes(1, byteorder='big')
    # ser.write(byte_data)
    rospy.loginfo(f"Sending: {bin(int_data)[2:].zfill(8)}")

if __name__ == '__main__':
    try:
        rospy.init_node('motor_control_sub_node', anonymous=True)
        # rate = rospy.Rate(10)
        # port = "/dev/ttyUSB0"
        # baudrate = 9600
        # ser = serial.Serial(port, baudrate, timeout=1)
        # threading.Thread(target=send_data(control_bit)).start()
        pub_control_cam = rospy.Publisher('pub_control_cam', Int32, queue_size=1) # Control Cam mode
        pub_robotarm = rospy.Publisher('pub_robotarm', Int32, queue_size=1) # Enable robotarm
        listener()
        
    except rospy.ROSInterruptException:
        print("Sub motor node : STOP")
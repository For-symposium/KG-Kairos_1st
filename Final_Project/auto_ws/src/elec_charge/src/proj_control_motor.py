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
from std_msgs.msg import Int32

i = 0
cam_mode = True
zero_turn_mode = False
zero_turn_dir = 0 # Left(-1), Right(1)

def cam_motor_control_callback(data):
    global i, cam_mode, zero_turn_dir, zero_turn_mode
    if cam_mode == True:
        if data.data == 10:
            print(f"Cam Sub : GO {i}")
            i += 1
            # mc.go_ahead(1)
        elif data.data == 1:
            print(f"Cam Sub : Right {i}")
            i += 1
            # mc.clockwise_rotation(1)
        elif data.data == -1:
            print(f"Cam Sub : Left {i}")
            i += 1
            # mc.counterclockwise_rotation(1)
        elif data.data == 0:
            print(f"Cam Sub : STOP {i}")
            i += 1
            # mc.stop()
        if data.data == -113:
            print(f"Cam Sub : Switch to IR mode && Zero-turn Left {i}")
            i += 1
            cam_mode = False
            zero_turn_dir = -1
        elif data.data == -117:
            print(f"Cam Sub : Switch to IR mode && Zero-turn Right {i}")
            i += 1
            cam_mode = False
            zero_turn_dir = 1


def IR_motor_control_callback(data):
    global i, cam_mode, zero_turn_dir, zero_turn_mode
    if cam_mode == False and zero_turn_mode == False:
        if data.data == 10:
            print(f"IR Sub : GO {i}")
            i += 1
            # mc.go_ahead(1)
        elif data.data == 0:
            print(f"IR Sub : All white. STOP {i}")
            i += 1
            zero_turn_mode = True
            # mc.stop()
    if cam_mode == False and zero_turn_mode == True:
        ##### Zero-turn by hard-coding #####
        if zero_turn_dir == -1:
            print(f"Zero turn Sub : Turn Left {i}")
            i += 1
            time.sleep(2)
            zero_turn_mode, cam_mode = False, True
        elif zero_turn_dir == 1:
            print(f"Zero turn Sub : Turn Right {i}")
            i += 1
            time.sleep(2)
            zero_turn_mode, cam_mode = False, True


def clean_up():
    rospy.loginfo("Sub node: Cleaning up...")
    # mc.stop()

def listener():
    rospy.init_node('motor_control_sub_node', anonymous=True)
    rospy.loginfo("Sub node : Start Subscribing")
    rospy.Subscriber('control_cam', Int32, cam_motor_control_callback) # line tracing
    rospy.Subscriber('control_IR', Int32, IR_motor_control_callback) # line tracing
    rospy.on_shutdown(clean_up)
    rospy.spin()  # Keep away from exiting

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        print("Sub motor node : STOP")
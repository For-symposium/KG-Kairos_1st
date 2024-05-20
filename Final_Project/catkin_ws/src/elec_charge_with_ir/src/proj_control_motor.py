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
'''

import rospy
import time
from std_msgs.msg import Int32

def cam_motor_control_callback(data):
    if data.data == 10:
        print("Cam Sub : GO")
        # mc.go_ahead(1)
    elif data.data == 1:
        print("Cam Sub : Right")
        # mc.clockwise_rotation(1)
    elif data.data == -1:
        print("Cam Sub : Left")
        # mc.counterclockwise_rotation(1)
    elif data.data == 0:
        print("Cam Sub : STOP")
        # mc.stop()

def IR_motor_control_callback(data):
    if data.data == 10:
        print("IR Sub : GO")
        # mc.go_ahead(1)
    elif data.data == 0:
        print("IR Sub : STOP")
        # mc.stop()
    
    if data.data == 99:
        print("Zero turn DIR Sub : Left")
        # zero_turn_left cmd
        time.sleep(2)
    elif data.data == 101:
        print("Zero turn DIR Sub : Right")
        # zero_turn_right cmd
        time.sleep(2)
    
def clean_up():
    rospy.loginfo("Sub node: Cleaning up...")
    # mc.stop()

def listener():
    rospy.init_node('motor_control_sub_node', anonymous=True)
    rospy.loginfo("Sub node Start")
    rospy.Subscriber('control_cam', Int32, cam_motor_control_callback) # line tracing
    rospy.Subscriber('control_IR', Int32, IR_motor_control_callback) # line tracing
    rospy.on_shutdown(clean_up)
    rospy.spin()  # Keep away from exiting

if __name__ == '__main__':
    listener()
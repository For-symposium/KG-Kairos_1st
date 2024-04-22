################################################################
##### Get a signal from publish node to control the motors #####
################################################################

import rospy
from std_msgs.msg import Int32
from pymycobot.myagv import MyAgv

mc = MyAgv('/dev/ttyAMA2', 115200)

def motor_control_callback(data):
    # rospy.loginfo(rospy.get_caller_id() + "Listen %d", data.data)
    if data.data == 0:
        print("Sub : GO")
        mc.go_ahead(1)
    elif data.data == 1:
        print("Sub : Right")
        mc.clockwise_rotation(1)
    elif data.data == -1:
        print("Sub : Left")
        mc.counterclockwise_rotation(1)
    elif data.data == 10:
        print("Sub : STOP")
        mc.stop()


def listener():
    print("Subscriber")
    rospy.init_node('motor_control_sub', anonymous=True)
    rospy.Subscriber('control_motor', Int32, motor_control_callback)
    rospy.spin() # Keep away from exiting

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        mc.stop()
        print("Finish Subscribing")

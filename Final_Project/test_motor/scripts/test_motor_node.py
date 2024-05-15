#!/usr/bin/env python2
import rospy
from std_msgs.msg import String

def test_motor_node():
    pub = rospy.Publisher('write', String, queue_size=10)
    rospy.init_node('test_motor_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "420"
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        test_motor_node()
    except rospy.ROSInterruptException:
        pass
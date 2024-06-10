import rospy
from std_msgs.msg import Int32
import time

def TOF_mode_pub():
    try:
        i = 0
        while not rospy.is_shutdown():
            pub_TOF.publish(10)
            print(f"TOF pub node : GO {i}")
            rate.sleep()
            pub_TOF.publish(-1)
            print(f"TOF pub node : LEFT {i}")
            rate.sleep()
            pub_TOF.publish(1)
            print(f"TOF pub node : RIGHT {i}")
            rate.sleep()
            pub_TOF.publish(0)
            print(f"TOF pub node : STOP {i}")
            rate.sleep()
            i += 1
    except KeyboardInterrupt:
        print("IR mode pub : Keyboard Interrupted")

if __name__=='__main__':
    try:
        rospy.init_node('TOF_pub_node', anonymous=True)
        pub_TOF = rospy.Publisher('control_TOF', Int32, queue_size=1)
        rate = rospy.Rate(4)
        TOF_mode_pub()
    except rospy.ROSInterruptException:
        print("TOF_mode_pub : Finish Publishing")

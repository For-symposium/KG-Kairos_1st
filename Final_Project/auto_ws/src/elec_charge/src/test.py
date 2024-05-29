import time
import rospy
from std_msgs.msg import Int32



if __name__ == '__main__':
    try:
        rospy.init_node('test_node', anonymous=True)
        rospy.loginfo("Test node launched")
        pub_motor = rospy.Publisher('vehicle_position', Int32, queue_size=10)
        rate = rospy.Rate(10)
        test_publish_message()
    except rospy.ROSInterruptException:
        print("Cam pub node : Stop publishing")

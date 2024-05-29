import time
import rospy
from std_msgs.msg import Int32

i = 0

def pub_test():
    global i
    while i <= 1:
        pub_test_web.publish(11)
        print(f"Web publish {i}")
        i += 1
        time.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('test_node', anonymous=True)
        rospy.loginfo("Test node launched")
        pub_test_web = rospy.Publisher('vehicle_position', Int32, queue_size=10)
        rate = rospy.Rate(10)
        pub_test()
    except rospy.ROSInterruptException:
        print("Cam pub node : Stop publishing")

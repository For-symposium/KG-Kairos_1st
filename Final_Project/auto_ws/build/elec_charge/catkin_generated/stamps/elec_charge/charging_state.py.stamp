import rospy
from std_msgs.msg import Int32
import time

def charging_state(data):
    i = 0
    try:
        if data.data == 3:   
            while not rospy.is_shutdown():
                print(f"Robotarm Charging... {i}")
                i += 1
                rate.sleep()
        elif data.data == 4:
                    print("Robotarm done")
                    pub_robotarm.publish(-400)
    except KeyboardInterrupt:
        print("IR mode pub : Keyboard Interrupted")

def listener():
    rospy.Subscriber('client_message', Int32, charging_state)
    rospy.spin()

if __name__=='__main__':
    try:
        rospy.init_node('charging_state_sub_node', anonymous=True)
        rospy.loginfo('charging_state node')
        pub_robotarm = rospy.Publisher('control_robotarm', Int32, queue_size=1)
        rate = rospy.Rate(1)
        listener()
    except rospy.ROSInterruptException:
        print("Robotarm mode pub : Finish Publishing")

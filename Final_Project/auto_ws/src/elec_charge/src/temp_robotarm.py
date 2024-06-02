import rospy
from std_msgs.msg import Int32
import time

def Robotarm_sub(data):
    i = 0
    try:
        if data.data == 400:   
            while not rospy.is_shutdown():
                print(f"Robotarm Charging... {i}")
                i += 1
                rate.sleep()
                if i == 5:
                    print("Robotarm done")
                    pub_robotarm.publish(-400)
                    break
    except KeyboardInterrupt:
        print("IR mode pub : Keyboard Interrupted")

def listener():
    rospy.Subscriber('pub_robotarm', Int32, Robotarm_sub)
    rospy.spin()

if __name__=='__main__':
    try:
        rospy.init_node('robotarm pub node', anonymous=True)
        rospy.loginfo('Robotarm node')
        pub_robotarm = rospy.Publisher('control_robotarm', Int32, queue_size=1)
        rate = rospy.Rate(1)
        listener()
    except rospy.ROSInterruptException:
        print("Robotarm mode pub : Finish Publishing")

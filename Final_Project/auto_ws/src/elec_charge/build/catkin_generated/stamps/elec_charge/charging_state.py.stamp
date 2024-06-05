import rospy
from std_msgs.msg import Int32

i = 0
mode = None

def charging_state(data):
    global mode
    mode = data.data

def while_charging(event):
    global i, mode
    if mode == 3:
        print(f"Robotarm Charging... {i}")
        i += 1
    elif mode == 4:
        pub_robotarm.publish(-400)
        print("Robotarm done")
        rospy.signal_shutdown("Charging complete")  # Shutdown ROS node after publishing -400
    else:
        print("Waiting")
def clean_up():
    rospy.loginfo("Sub node: Cleaning up...")

def listener():
    rospy.Subscriber('client_message', Int32, charging_state)
    rospy.on_shutdown(clean_up)
    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('charging_state_sub_node', anonymous=True)
        rospy.loginfo('charging_state node')
        pub_robotarm = rospy.Publisher('control_robotarm', Int32, queue_size=1)
        
        # Create a timer to call while_charging every second
        rospy.Timer(rospy.Duration(0.5), while_charging)
        
        listener()
    except rospy.ROSInterruptException:
        print("Robotarm mode pub : Finish Publishing")

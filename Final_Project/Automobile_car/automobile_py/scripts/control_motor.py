import rospy
from std_msgs.msg import Int32
from pymycobot.myagv import MyAgv

'''
< Data signals >

1. OpenCV Line-tracing
    - 0 : GO
    - -1 : Left
    - 1 : Right
    - 10 : STOP

2. Lidar Obstacle
    - 100 : STOP
    - 110 : Allow to move

3. Traffic light
    - 200 : STOP
    - 210 : Allowed
'''

mc = MyAgv('/dev/ttyAMA2', 115200)
lidar2motor_control = True # bridge from lidar to motor_control
traffic2motor_control = True # bridge from traffic to motor_control

def motor_control_callback(data):
    global lidar2motor_control
    if lidar2motor_control == True and traffic2motor_control == True:
        if data.data == 0:
            print("Cam Sub : GO")
            mc.go_ahead(1)
        elif data.data == 1:
            print("Cam Sub : Right")
            mc.clockwise_rotation(1)
        elif data.data == -1:
            print("Cam Sub : Left")
            mc.counterclockwise_rotation(1)
        elif data.data == 10:
            print("Cam Sub : STOP")
            mc.stop()

def lidar_check_callback(ldata):
    global lidar2motor_control
    if ldata.data == 100:
        print("Lidar Sub : STOP")
        mc.stop()
        lidar2motor_control = False
    elif ldata.data == 110:
        print("Lidar Sub : Pass")
        # mc.go_ahead(1)
        lidar2motor_control = True

def traffic_check_callback(tdata):
    global traffic2motor_control
    if tdata.data == 200:
        print("Traffic Sub : STOP")
        mc.stop()
        traffic2motor_control = False
    else:
        print("Traffic Sub : Pass")
        traffic2motor_control = True

def clean_up():
    rospy.loginfo("Sub node: Cleaning up...")
    mc.stop()

def listener():
    rospy.init_node('motor_control_sub', anonymous=True)
    rospy.Subscriber('control_motor', Int32, motor_control_callback)
    rospy.Subscriber('lidar_obstacle', Int32, lidar_check_callback)
    rospy.Subscriber('traffic_light', Int32, traffic_check_callback)
    rospy.on_shutdown(clean_up)
    rospy.spin()  # Keep away from exiting

if __name__ == '__main__':
    listener()
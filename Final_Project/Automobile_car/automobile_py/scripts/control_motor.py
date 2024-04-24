import rospy
from std_msgs.msg import Int32
from pymycobot.myagv import MyAgv

mc = MyAgv('/dev/ttyAMA2', 115200)
lidar2motor_control = True # bridge from lidar to motor_control

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

'''

def motor_control_callback(data):
    global lidar2motor_control
    if lidar2motor_control == True:
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

def listener():
    print("Sub node : Motor Control Subscriber")
    rospy.init_node('motor_control_sub', anonymous=True)
    rospy.Subscriber('control_motor', Int32, motor_control_callback)
    rospy.Subscriber('lidar_obstacle', Int32, lidar_check_callback)
    rospy.spin() # Keep away from exiting

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        mc.stop()
        print("Sub node : Finish Subscribing")
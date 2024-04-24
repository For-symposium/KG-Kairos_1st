import rospy
from std_msgs.msg import Int32
from pymycobot.myagv import MyAgv

mc = MyAgv('/dev/ttyAMA2', 115200)

'''
< Data signals >

1. OpenCV Line-tracing
    - 0 : GO
    - -1 : Left
    - 1 : Right
    - 10 : STOP

2. Lidar Obstacle
    - 100 : STOP

'''

def motor_control_callback(data):
    if data.data == 100:
        print("Lidar Sub : STOP")
        mc.stop()
    else:
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


def listener():
    print("Subscriber")
    rospy.init_node('motor_control_sub', anonymous=True)
    rospy.Subscriber('control_motor', Int32, motor_control_callback)
    rospy.Subscriber('lidar_obstacle', Int32, motor_control_callback)
    rospy.spin() # Keep away from exiting

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        mc.stop()
        print("Finish Subscribing")
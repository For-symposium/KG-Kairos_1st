import smbus
import time
import rospy
from std_msgs.msg import Int32

I2C_BUS = 1
ARDUINO_ADDRESS = 0x08

def read_i2c_data():
    bus = smbus.SMBus(I2C_BUS)
    try:
        data = bus.read_byte(ARDUINO_ADDRESS)
        return data
    except IOError:
        return None

def i2c_listener():
    rospy.init_node('i2c_listener', anonymous=True)
    pub = rospy.Publisher('ToF_Topic', Int32, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz

    while not rospy.is_shutdown():
        tof_state = read_i2c_data()
        if tof_state is not None:
            rospy.loginfo("Received ToF_State: %d", tof_state)
            pub.publish(tof_state)
        rate.sleep()

if __name__ == '__main__':
    try:
        i2c_listener()
    except rospy.ROSInterruptException:
        pass

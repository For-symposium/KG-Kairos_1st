#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
import smbus2
import time

# I2C bus and address setting
I2C_BUS = 1
SLAVE_ADDRESS = 0x04

def read_i2c_data():
    try:
        bus = smbus2.SMBus(I2C_BUS)
        data = bus.read_i2c_block_data(SLAVE_ADDRESS, 0, 4)
        # change data as byte
        value = int.from_bytes(data, byteorder='little', signed=True)
        return value
    except Exception as e:
        rospy.logerr("Failed to read from I2C device: %s", e)
        return None

def i2c_listener():
    rospy.init_node('i2c_listener', anonymous=True)
    pub = rospy.Publisher('ToF_Topic', Int32, queue_size=10)
    rate = rospy.Rate(10) # 10Hz

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

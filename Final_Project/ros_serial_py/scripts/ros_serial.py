#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Int32
import serial
import time

# 전역 시리얼 포트 객체
ser = None

def send_data(data):
    ser.write(data)
    rospy.loginfo(f"Sending: {data}")
    rospy.loginfo(f"Sending: {data.hex()}")

def receive_data():
    while ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        rospy.loginfo(f"Received (Hex): {data.hex()}")
        # rospy.loginfo(f"Received (Int): {int(data.hex(), 16)}")

def write_callback(msg):
    if msg.data:
        int_data = int(msg.data)
        byte_data = int_data.to_bytes(2, byteorder='big')
        send_data(byte_data)
        # hex_data = byte_data.hex()
        # send_data(hex_data)
        time.sleep(0.1)  # Wait a bit for the STM32 to respond
        receive_data()
    else:
        rospy.logwarn("Invalid input. Please enter a value between 210 and 1050.")

def main():
    global ser
    rospy.init_node('serial_node', anonymous=True)
    rospy.Subscriber('write', String, write_callback)

    # 시리얼 포트 설정
    port = "/dev/ttyUSB0"
    baudrate = 115200
    ser = serial.Serial(port, baudrate, timeout=1)
    rospy.loginfo(f"serial connetected")

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    finally:
        if ser:
            ser.close()

'''
Pin 8 (TX) -> Arduino Mega Pin 19 (RX1)
Pin 10 (RX) -> Arduino Mega Pin 18 (TX1)
GND -> GND (공통 그라운드 연결)
'''
import serial
import time
import rospy
from std_msgs.msg import Int32

def TOF_mode_pub():
    i = 0
    try:
        while not rospy.is_shutdown():
            if ser.in_waiting >= 1:  # 수신 대기 중인 데이터가 있을 때
                data = ser.read(1)  # 1바이트 읽기
                tof_state = int.from_bytes(data, byteorder='little', signed=True)
                if tof_state == 10:
                    pub_TOF.publish(10)
                    print(f"Received TOF_State: GO {i}")
                    i += 1
                elif tof_state == -1:
                    pub_TOF.publish(-1)
                    print(f"Received TOF_State: Left {i}")
                    i += 1
                elif tof_state == 1:
                    pub_TOF.publish(1)
                    print(f"Received TOF_State: Right {i}")
                    i += 1
                elif tof_state == 0:
                    pub_TOF.publish(0)
                    print(f"Received TOF_State: Stop and Robotarm mode ON {i}")
                    i += 1
                rate.sleep()

    except KeyboardInterrupt:
        print("TOF mode pub : Keyboard Interrupted")

if __name__=='__main__':
    try:
        rospy.init_node('TOF_pub_node', anonymous=True)
        pub_TOF = rospy.Publisher('control_TOF', Int32, queue_size=1)
        rate = rospy.Rate(10)
        ser = serial.Serial(uart_port, baud_rate)
        uart_port = '/dev/ttyTHS1'
        baud_rate = 9600
        TOF_mode_pub()
    except rospy.ROSInterruptException:
        print("TOF_mode_pub : Finish Publishing")
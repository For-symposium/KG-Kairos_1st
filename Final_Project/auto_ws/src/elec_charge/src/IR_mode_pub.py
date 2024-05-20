import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import Int32

# 사용할 GPIO 핀 번호 (BCM 모드)
IR_SENSOR_PIN_1 = 17 # GPIO 11
# IR_SENSOR_PIN = 11 # GPIO 23
IR_SENSOR_PIN_2 = 23 # GPIO 16
IR_SENSOR_PIN_3 = 16 # GPIO 36

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setup(IR_SENSOR_PIN_1, GPIO.IN)
GPIO.setup(IR_SENSOR_PIN_2, GPIO.IN)
GPIO.setup(IR_SENSOR_PIN_3, GPIO.IN)

i = 0

def read_ir_sensor_1():
	return GPIO.input(IR_SENSOR_PIN_1)

def read_ir_sensor_2():
	return GPIO.input(IR_SENSOR_PIN_2)

def read_ir_sensor_3():
	return GPIO.input(IR_SENSOR_PIN_3)

# 0 : White(No line), 1 : Black(Line)
def IR_mode_pub():
    global i
    try:
        while not rospy.is_shutdown():
            if read_ir_sensor_1 == 0 and read_ir_sensor_2 == 0 and read_ir_sensor_3 == 0:
                print(f"IR pub : All white. STOP {i}")
                i += 1
                pub_IR.publish(0) # STOP
                break
            else:
                print(f"IR pub : GO {i}")
                i += 1
                pub_IR.publish(10) # GO
            rate.sleep()
    except rospy.ROSInterruptException:
        print("IR mode pub : ROS Interrupted")
    except KeyboardInterrupt:
        print("IR mode pub : Keyboard Interrupted")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        rospy.init_node('IR pub node', anonymous=True)
        pub_IR = rospy.Publisher('control_IR', Int32, queue_size=10)
        rate = rospy.Rate(10)
        IR_mode_pub()
    except rospy.ROSInterruptException:
        print("IR mode pub : Finish Publishing")
    finally:
        GPIO.cleanup()
        print("IR mode pub : Finished Publishing")
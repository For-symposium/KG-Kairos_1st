"""
-113 : Zero turn Left
-117 : Zero turn Right
"""

import board
import busio
import adafruit_vl53l0x
import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import Int32
import threading

# 사용할 GPIO 핀 번호 (BCM 모드)
# IR_SENSOR_PIN_1 = 17 # GPIO 11
# IR_SENSOR_PIN = 11 # GPIO 23
# IR_SENSOR_PIN_2 = 23 # GPIO 16
# IR_SENSOR_PIN_3 = 16 # GPIO 36

# Board mode
IR_SENSOR_PIN_1 = 11 # BOARD
IR_SENSOR_PIN_2 = 16 # BOARD

# GPIO 설정
# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setup(IR_SENSOR_PIN_1, GPIO.IN)
GPIO.setup(IR_SENSOR_PIN_2, GPIO.IN)
# GPIO.setup(IR_SENSOR_PIN_3, GPIO.IN)
IR_mode = False
i = 0

# Set pin number
XSHUT1_PIN = 7
XSHUT2_PIN = 8

# Declare global variable
modestate = 0
offset = 0

def read_ir_sensor_Left():
    return GPIO.input(IR_SENSOR_PIN_1)

def read_ir_sensor_Right():
    return GPIO.input(IR_SENSOR_PIN_2)

# def read_ir_sensor_3():
# 	return GPIO.input(IR_SENSOR_PIN_3)

# 0 : White(No line), 1 : Black(Line)
def IR_mode_pub():
    global i, IR_mode
    NO_LINE = 0
    YES_LINE = 1
    try:
        while not rospy.is_shutdown():
            if read_ir_sensor_Left() == NO_LINE and read_ir_sensor_Right() == NO_LINE:
                print(f"IR pub : Do zero turn {i}")
                pub_IR.publish(-120) # Zero turn Left
                i += 1
            else:
                print(f"IR pub : GO {i}")
                pub_IR.publish(10)
                i += 1
            rate.sleep()
    except KeyboardInterrupt:
        print("IR mode pub : Keyboard Interrupted")
    finally:
        GPIO.cleanup()

def TOF_GPIO_setup(XSHUT1_PIN ,XSHUT2_PIN):
    global sensor1, sensor2

    GPIO.setup(XSHUT1_PIN, GPIO.OUT)
    GPIO.setup(XSHUT2_PIN, GPIO.OUT)

    # Deactivate both sensors
    GPIO.output(XSHUT1_PIN, GPIO.LOW)
    GPIO.output(XSHUT2_PIN, GPIO.LOW)
    time.sleep(0.1)

    # I2C 설정
    i2c = busio.I2C(board.SCL, board.SDA)

    # Activate first sensor
    GPIO.output(XSHUT1_PIN, GPIO.HIGH)
    time.sleep(0.1)
    sensor1 = adafruit_vl53l0x.VL53L0X(i2c)

    # Activate second sensor
    GPIO.output(XSHUT1_PIN, GPIO.LOW)
    GPIO.output(XSHUT2_PIN, GPIO.HIGH)
    time.sleep(0.1)
    sensor2 = adafruit_vl53l0x.VL53L0X(i2c)

    # Activate both sensors
    GPIO.output(XSHUT1_PIN, GPIO.HIGH)
    GPIO.output(XSHUT2_PIN, GPIO.HIGH)
    time.sleep(0.1)

def CompareLR(distance1, distance2):
    global modestate, offset
    offset = 90  # Unit : mm
    if distance2 - 90 <= distance1 <= distance2 + 90:  # Go
        modestate = 1
    elif distance1 > distance2 + 90:  # Right
        modestate = 2
    elif distance2 > distance1 + 90:  # Left
        modestate = 3
    else:  # Stop
        modestate = 0

def TOF_mode_pub():
    j = 0
    global modestate, sensor1, sensor2
    try:
        while not rospy.is_shutdown():
            distance1 = sensor1.range  # Left sensor
            distance2 = sensor2.range  # Right sensor
            print("Sensor 1: {}mm".format(distance1))
            print("Sensor 2: {}mm".format(distance2))
            CompareLR(distance1, distance2)
            if modestate == 0:  # Stop
                print(f"TOF pub : Stop //{j}")
                j += 1
                pub_TOF.publish(0)
            elif modestate == 1:  # Go
                print(f"TOF pub : Straight // {j}")
                j += 1
                pub_TOF.publish(10)
            elif modestate == 2:  # Right
                print(f"TOF pub : Right Drive(right shorter than left) // {j}")
                j += 1
                pub_TOF.publish(1)
            elif modestate == 3:  # Left
                print(f"TOF pub : Left Drive(left shorter than right) // {j}")
                j += 1
                pub_TOF.publish(-1)
            rate.sleep()
    except KeyboardInterrupt:
        print("TOF mode pub : Keyboard Interrupted")
    finally:
        sensor1.stop_ranging()
        sensor2.stop_ranging()
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        TOF_GPIO_setup(XSHUT1_PIN ,XSHUT2_PIN)
        rospy.init_node('IR TOF pub node', anonymous=True)
        pub_IR = rospy.Publisher('control_IR', Int32, queue_size=10)
        pub_TOF = rospy.Publisher('control_TOF', Int32, queue_size=10)
        rate = rospy.Rate(10)
        threading.Thread(target=TOF_mode_pub).start()
        IR_mode_pub()
    except rospy.ROSInterruptException:
        print("IR TOF mode pub : Finish Publishing")
    finally:
        GPIO.cleanup()
        print("IR TOF mode pub : Finished Publishing")
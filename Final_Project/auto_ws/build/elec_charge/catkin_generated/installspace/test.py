import time
import board
import busio
import adafruit_vl53l0x
import Jetson.GPIO as GPIO
import rospy
from std_msgs.msg import Int32

# Set pin number
XSHUT1_PIN = 15
XSHUT2_PIN = 7

# Declare global variable
modestate = 0
offset = 0

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
    i = 0
    global modestate
    try:
        while not rospy.is_shutdown():
            distance1 = sensor1.range  # Left sensor
            distance2 = sensor2.range  # Right sensor
            print("Sensor 1: {}mm".format(distance1))
            print("Sensor 2: {}mm".format(distance2))
            CompareLR(distance1, distance2)
            if modestate == 0:  # Stop
                print(f"TOF pub : Stop //{i}")
                i += 1
                pub_TOF.publish(0)
            elif modestate == 1:  # Go
                print(f"TOF pub : Straight // {i}")
                i += 1
                pub_TOF.publish(10)
            elif modestate == 2:  # Right
                print(f"TOF pub : Right Drive(right shorter than left) // {i}")
                i += 1
                pub_TOF.publish(1)
            elif modestate == 3:  # Left
                print(f"TOF pub : Left Drive(left shorter than right) // {i}")
                i += 1
                pub_TOF.publish(-1)
            rate.sleep()
    except KeyboardInterrupt:
        print("TOF mode pub : Keyboard Interrupted")
    finally:
        sensor1.stop_ranging()
        sensor2.stop_ranging()
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

if __name__ == '__main__':
    # Set GPIO
    try:
        GPIO.setmode(GPIO.BOARD)
    except ValueError as e:
        print(f"Warning: {e}")

    TOF_GPIO_setup(XSHUT1_PIN ,XSHUT2_PIN)

    try:
        rospy.init_node('TOF_pub_node', anonymous=True)
        pub_TOF = rospy.Publisher('control_TOF', Int32, queue_size=10)
        rate = rospy.Rate(10)
        TOF_mode_pub()
    except rospy.ROSInterruptException:
        print("TOF mode pub : Finish Publishing")
    finally:
        GPIO.cleanup()
        print("TOF mode pub : Finished Publishing")

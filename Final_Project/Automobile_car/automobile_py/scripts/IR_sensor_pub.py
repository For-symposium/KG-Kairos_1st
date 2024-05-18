import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import Int32


# 사용할 GPIO 핀 번호 (BCM 모드)
IR_SENSOR_PIN_1 = 17 # GPIO 11
# IR_SENSOR_PIN = 11 # GPIO 23
IR_SENSOR_PIN_2 = 23 # GPIO 16
IR_SENSOR_PIN_3 = 16 # GPIO 36

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN_1, GPIO.IN) # Left
GPIO.setup(IR_SENSOR_PIN_2, GPIO.IN) # Center
GPIO.setup(IR_SENSOR_PIN_3, GPIO.IN) # Right

def read_ir_sensor_left():
	return GPIO.input(IR_SENSOR_PIN_1)

def read_ir_sensor_center():
	return GPIO.input(IR_SENSOR_PIN_2)

def read_ir_sensor_right():
	return GPIO.input(IR_SENSOR_PIN_3)

def IR_publisher():
	IR_pub_motor = rospy.Publisher('control_IR', Int32, queue_size=10)
    rospy.init_node('IR_motor_control_pub', anonymous=True)
    rate = rospy.Rate(10)
    rospy.loginfo('Publishing IR sensor control')

    # White = 0(Non-track), Black = 1(Track)
	try:
		while not rospy.is_shutdown():
			if read_ir_sensor_left == 0 and read_ir_sensor_center == 0 and read_ir_sensor_right == 0: # STOP
				IR_pub_motor.publish(0)
				# Zero turn signal
            elif read_ir_sensor_left == 0 and read_ir_sensor_center == 1 and read_ir_sensor_right == 0: # GO
                IR_pub_motor.publish(10)
			elif read_ir_sensor_left == 0 and read_ir_sensor_center == 0 and read_ir_sensor_right == 1: # Turn right
				IR_pub_motor.publish(1)
            elif read_ir_sensor_left == 1 and read_ir_sensor_center == 0 and read_ir_sensor_right == 1: # Turn left
				IR_pub_motor.publish(-1)

			rate.sleep()
	except KeyboardInterrupt:
		print("Program interrupted")
	finally:
		GPIO.cleanup()

if __name__ == '__main__':
	IR_publisher()
except rospy.ROSInterruptException:
        print("IR_motor_control_pub node : Finish Publishing")
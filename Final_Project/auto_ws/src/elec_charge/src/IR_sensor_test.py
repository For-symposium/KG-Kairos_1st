import Jetson.GPIO as GPIO
import time
# import rospy
# from std_msgs.msg import Int32


# 사용할 GPIO 핀 번호 (BCM 모드)
IR_SENSOR_PIN_1 = 17 # GPIO 11
# IR_SENSOR_PIN = 11 # GPIO 23
IR_SENSOR_PIN_2 = 23 # GPIO 16
IR_SENSOR_PIN_3 = 16 # GPIO 36

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN_1, GPIO.IN)
GPIO.setup(IR_SENSOR_PIN_2, GPIO.IN)
GPIO.setup(IR_SENSOR_PIN_3, GPIO.IN)

def read_ir_sensor_1():
	return GPIO.input(IR_SENSOR_PIN_1)

def read_ir_sensor_2():
	return GPIO.input(IR_SENSOR_PIN_2)

def read_ir_sensor_3():
	return GPIO.input(IR_SENSOR_PIN_3)

def IR_publisher():
	# IR_pub_motor = rospy.Publisher('control_IR', Int32, queue_size=10)
    # rospy.init_node('motor_control_pub', anonymous=True)
    # rate = rospy.Rate(10)

	try:
		while True:
			if read_ir_sensor_1() == 0:
				print("1st White")
			else:
				print("1st Black")

			if read_ir_sensor_2() == 0:
				print("2nd White")
			else:
				print("2nd Black")

			if read_ir_sensor_3() == 0:
				print("3rd White")
			else:
				print("3rd Black")

			time.sleep(0.1)
	except KeyboardInterrupt:
		print("Program interrupted")
	finally:
		GPIO.cleanup()

if __name__ == '__main__':
	IR_publisher()

import Jetson.GPIO as GPIO
import time

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

def main():
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

			time.sleep(0.1)  # 0.5초 간격으로 값 읽기
	except KeyboardInterrupt:
		print("Program interrupted")
	finally:
		GPIO.cleanup()

if __name__ == '__main__':
	main()
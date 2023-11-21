import time
import VL53L0X
import Jetson.GPIO as GPIO

# 핀 번호 설정
XSHUT1_PIN = 7
XSHUT2_PIN = 11

# GPIO 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(XSHUT1_PIN, GPIO.OUT)
GPIO.setup(XSHUT2_PIN, GPIO.OUT)

# 두 센서 모두 비활성화
GPIO.output(XSHUT1_PIN, GPIO.LOW)
GPIO.output(XSHUT2_PIN, GPIO.LOW)
time.sleep(0.1)

# 첫 번째 센서만 활성화
GPIO.output(XSHUT1_PIN, GPIO.HIGH)
time.sleep(0.1)
sensor1 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
sensor1.start_ranging()
sensor1.change_address(0x30)
sensor1.stop_ranging()

# 두 번째 센서 활성화
GPIO.output(XSHUT1_PIN, GPIO.LOW)
GPIO.output(XSHUT2_PIN, GPIO.HIGH)
time.sleep(0.1)
sensor2 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
sensor2.start_ranging()
sensor2.change_address(0x31)
sensor2.stop_ranging()

# 두 센서를 모두 활성화
GPIO.output(XSHUT1_PIN, GPIO.HIGH)
time.sleep(0.1)

# 새로운 주소로 센서 초기화
sensor1 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x30)
sensor2 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x31)

sensor1.start_ranging()
sensor2.start_ranging()

try:
    while True:
        distance1 = sensor1.get_distance()
        distance2 = sensor2.get_distance()
        print("Sensor 1: {}mm".format(distance1))
        print("Sensor 2: {}mm".format(distance2))
        time.sleep(1)
finally:
    sensor1.stop_ranging()
    sensor2.stop_ranging()
    GPIO.cleanup()

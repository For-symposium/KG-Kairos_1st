import time
import board
import busio
import adafruit_vl53l0x
import Jetson.GPIO as GPIO

# GPIO 핀 설정 (유효한 핀 번호로 변경)
XSHUT_PIN = 12  # Jetson Nano에서 사용할 수 있는 유효한 GPIO 핀 번호

# 기존 모드가 설정된 경우 모드를 유지하고, 그렇지 않으면 새로운 모드 설정
if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BOARD)  # BOARD 모드로 설정

GPIO.setup(XSHUT_PIN, GPIO.OUT)

def initialize_sensor():
    # ToF 센서 전원 켜기 (XSHUT 핀 HIGH)
    GPIO.output(XSHUT_PIN, GPIO.HIGH)
    time.sleep(0.01)  # 센서 초기화 시간 대기

    # I2C 버스 초기화
    i2c = busio.I2C(board.SCL, board.SDA)

    # ToF 센서 초기화
    try:
        vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        # 센서 기본 설정
        vl53.measurement_timing_budget = 200000  # 200ms, 선택적으로 조정 가능
        print("VL53L0X ToF 센서 초기화 완료")
        return vl53
    except OSError as e:
        print(f"센서 초기화 실패: {e}")
        return None

# 센서 초기화 시도
vl53 = None
while vl53 is None:
    vl53 = initialize_sensor()
    if vl53 is None:
        print("센서 초기화 재시도 중...")
        time.sleep(1)  # 재시도 전 대기

# 거리 측정 루프
try:
    while True:
        distance = vl53.range  # 거리 측정 (mm 단위)
        print(f"거리: {distance} mm")
        time.sleep(1)  # 1초 간격으로 측정
except KeyboardInterrupt:
    print("측정 종료")
finally:
    GPIO.cleanup()  # GPIO 핀 해제

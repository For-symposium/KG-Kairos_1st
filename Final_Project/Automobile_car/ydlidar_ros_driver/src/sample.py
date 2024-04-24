import time
from LidarX2 import LidarX2
import RPi.GPIO as GPIO

PIN_LIDAR_PWR = 20      # GPIO pin to power the LiDAR
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LIDAR_PWR, GPIO.OUT)
GPIO.output(PIN_LIDAR_PWR, GPIO.HIGH)
time.sleep(0.5)

lidar = LidarX2("/dev/ttyAMA0")  # Name of the serial port, can be /dev/tty*, COM*, etc.

if not lidar.open():
    print("Cannot open lidar")
    exit(1)

try:
    i = 1
    t = time.time()
    while time.time() - t < 10:  # Run for 10 seconds
        # angle = lidar.getMeasures()
        measures = lidar.getMeasures()
        # print(angle, type(angle))
        # print(dist, type(dist), "\n")
        measures = [str(m) for m in measures if str(m)]  # Filter out empty strings
        if measures:  # Only print if there are valid measures
            print(f"Step {i}")
            i += 1
            print('\n'.join(measures))
            print('\n')
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.output(PIN_LIDAR_PWR, GPIO.LOW)
    print("LiDAR stoped")
    print("Done")
    pass

finally:
    lidar.close()
    print("Lidar closed.")
import time
from LidarX2 import LidarX2

lidar = LidarX2("/dev/ttyAMA0")  # Name of the serial port, can be /dev/tty*, COM*, etc.

if not lidar.open():
    print("Cannot open lidar")
    exit(1)

try:
    i = 1
    t = time.time()
    while time.time() - t < 10:  # Run for 10 seconds
        measures = lidar.getMeasures()
        measures = [str(m) for m in measures if str(m)]  # Filter out empty strings
        if measures:  # Only print if there are valid measures
            print(f"Step {i}")
            i += 1
            print('\n'.join(measures))
            print('\n')
        time.sleep(1)
finally:
    lidar.close()
    print("Lidar closed.")
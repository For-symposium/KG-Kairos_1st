import Second_LidarX2
import time

port =  '/dev/ttyAMA0'
lid = Second_LidarX2.YDLidarX2(port)
lid.connect()
lid.start_scan()

try:
    while True:
        if lid.available:
            distances = lid.get_data()
            # process the distance measurements
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

lid.stop_scan()
lid.disconnect()
print("Done")
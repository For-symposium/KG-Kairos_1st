import time
from LidarX2 import LidarX2
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import Int32

def ydlidar_publish_message():
    pub_lidar = rospy.Publisher('lidar_obstacle', Int32, queue_size=10)
    rospy.init_node('lidar_obstacle_node', anonymous=True)
    rate = rospy.Rate(10)
    rospy.loginfo('Lidar Pub node : Publishing Ydlidar Obstacle Detection')

    PIN_LIDAR_PWR = 20      # GPIO pin to power the LiDAR
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LIDAR_PWR, GPIO.OUT)
    GPIO.output(PIN_LIDAR_PWR, GPIO.HIGH)
    time.sleep(0.5)

    lidar = LidarX2("/dev/ttyAMA0")  # Name of the serial port, can be /dev/tty*, COM*, etc.

    if not lidar.open():
        print("Lidar Pub node : Cannot open lidar")
        exit(1)

    try:
        i = 1
        # t = time.time()
        # while time.time() - t < 10:
        while not rospy.is_shutdown():
            # angle = lidar.getMeasures()
            measures = lidar.getMeasures()
            '''
            [, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , Degree: 180.33   Dist: 61.65cm
            , Degree: 181.14        Dist: 61.02cm
            , Degree: 181.93        Dist: 60.62cm
            , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ]
            '''
            
            measures = [str(m) for m in measures if str(m)]  # Filter out empty strings
            if measures:  # Only print if there are valid measures
                print(f"\nStep {i}")
                # print(measures) 
                # ['Degree: 178.11\tDist: 745.50cm\n', 'Degree: 180.72\tDist: 61.65cm\n', 'Degree: 181.49\tDist: 61.73cm\n']
                i += 1
                print(''.join(measures))
                for measure in measures:
                    distance = float(measure.split("Dist:")[1].strip()[:-2])
                    # print(distance)
                    if 0 < distance <= 25:
                        pub_lidar.publish(100)
                        print("Lidar Pub node : STOP")
                    else:
                        pub_lidar.publish(110)
                        print("Lidar Pub node : Allowed")
                
            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.output(PIN_LIDAR_PWR, GPIO.LOW)
        print("Lidar Pub node : LiDAR stopped")
        print("Lidar Pub node : Done")
        pass

    finally:
        lidar.close()
        GPIO.output(PIN_LIDAR_PWR, GPIO.LOW)
        print("Lidar Pub node : Lidar stopped and closed.")
        

if __name__ == '__main__':
    try:
        ydlidar_publish_message()
    except rospy.ROSInterruptException:
        print("Lidar Pub node : Finish Publishing")
        pass
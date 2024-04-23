import os
import time

if os.name == "posix":
    import RPi.GPIO as GPIO

# def lidar_open(self):
#     def lidar_high():
#         GPIO.setmode(GPIO.BCM)
#         time.sleep(0.1)
#         GPIO.setup(20, GPIO.OUT)
#         GPIO.output(20, GPIO.HIGH)

#     lidar_high()
#     time.sleep(0.05)
    # launch_command = "roslaunch myagv_odometry myagv_active.launch"  # 使用ros 打开
    # subprocess.run(
    #     ['gnome-terminal', '-e', f"bash -c '{launch_command}; exec $SHELL'"])

def lidar_high():
    GPIO.setmode(GPIO.BCM)
    time.sleep(0.1)
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.HIGH)

# def lidar_close(self, run_launch):
#     def lidar_low():
#         GPIO.setmode(GPIO.BCM)
#         time.sleep(0.1)
#         GPIO.setup(20, GPIO.OUT)
#         GPIO.output(20, GPIO.LOW)

#     lidar_low()
#     time.sleep(0.05)

    # close_command = "ps -ef | grep -E " + run_launch + \
    #     " | grep -v 'grep' | awk '{print $2}' | xargs kill -2"
    # subprocess.run(close_command, shell=True)

def lidar_low():
    GPIO.setmode(GPIO.BCM)
    time.sleep(0.1)
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.LOW)

if __name__ == "__main__":
    lidar_high()
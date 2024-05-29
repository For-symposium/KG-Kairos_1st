"""
-113 : Zero turn Left
-117 : Zero turn Right
"""

import Jetson.GPIO as GPIO
import time
import rospy
from std_msgs.msg import Int32


# 사용할 GPIO 핀 번호 (BCM 모드)
IR_SENSOR_PIN_1 = 17 # GPIO 11
# IR_SENSOR_PIN = 11 # GPIO 23
IR_SENSOR_PIN_2 = 23 # GPIO 16
# IR_SENSOR_PIN_3 = 16 # GPIO 36

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setup(IR_SENSOR_PIN_1, GPIO.IN)
GPIO.setup(IR_SENSOR_PIN_2, GPIO.IN)
# GPIO.setup(IR_SENSOR_PIN_3, GPIO.IN)

def read_ir_sensor_Left():
    if GPIO.input(IR_SENSOR_PIN_1) == 0:
        return "LEFT NO LINE"
    elif GPIO.input(IR_SENSOR_PIN_1) == 1:
	    return "LEFT YES LINE"

def read_ir_sensor_Right():
    if GPIO.input(IR_SENSOR_PIN_2) == 0:
        return "RIGHT NO LINE"
    elif GPIO.input(IR_SENSOR_PIN_2) == 1:
        return "RIGHT YES LINE"

# def read_ir_sensor_3():
# 	return GPIO.input(IR_SENSOR_PIN_3)

# 0 : White(No line), 1 : Black(Line)
def IR_mode_pub():
    i = 0
    NO_LINE = 0
    YES_LINE = 1
    try:
        while not rospy.is_shutdown():
            '''
            1. ir sensor L&R are all out of line
            2. IR pub: Stop, control_sub need to start Zero turn according to Map_arr
            3. Else situation IR pub: Go
            
            '''
            if read_ir_sensor_Left()==NO_LINE and read_ir_sensor_Right()==NO_LINE:
                print(f"IR pub : Stop // Control_sub need to start Zero turn according to MAP_ARR {i}")
                pub_IR.publish(-120)
                i+=1
            else:
                print(f"IR pub : Go {i}")
                pub_IR.publish(10)
                i+=1

            ''' 
            if read_ir_sensor_Left() == YES_LINE and read_ir_sensor_Right() == NO_LINE:
                print(f"IR pub : Zero turn Left {i}")
                pub_IR.publish(-113) # Zero turn Left
                i += 1
            elif read_ir_sensor_Left() == NO_LINE and read_ir_sensor_Right() == YES_LINE:
                print(f"IR pub : Zero turn Right {i}")
                pub_IR.publish(-117) # Zero turn Right
                i += 1
            elif read_ir_sensor_Left() == NO_LINE and read_ir_sensor_Right() == NO_LINE:
                print(f"IR pub : GO {read_ir_sensor_Left()}, {read_ir_sensor_Right()} // {i}")
                pub_IR.publish(10) # GO
                i += 1
            '''
            rate.sleep()
    except KeyboardInterrupt:
        print("IR mode pub : Keyboard Interrupted")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        rospy.init_node('IR pub node', anonymous=True)
        pub_IR = rospy.Publisher('control_IR', Int32, queue_size=10)
        rate = rospy.Rate(10)
        IR_mode_pub()
    except rospy.ROSInterruptException:
        print("IR mode pub : Finish Publishing")
    finally:
        GPIO.cleanup()
        print("IR mode pub : Finished Publishing")
import serial
import time

py_serial = serial.Serial('/dev/tty.usbserial-11410', 9600)

while True:
    command = input("Command to arduino : ")
    py_serial.write(command.encode())
    time.sleep(0.1)

    if py_serial.readable(): # read line by Byte unit
        response = py_serial.readline()
        print(response[:len(response)-1].decode())

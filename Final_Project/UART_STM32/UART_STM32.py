'''
UART USB : /dev/tty.usbserial-B002FMSW
STM32 : /dev/tty.usbmodem1303
'''

import serial
import time

# Open the serial port
ser = serial.Serial('/dev/tty.usbserial-B002FMSW', 115200)  # Adjust port and baud rate

# Function to send data
def send_data(data):
    # ser.write(data.encode())
    ser.write(data)
    print(f"Sending: {data}")

# Function to receive data
def receive_data():
    # Wait for data to be available in the input buffer
    while ser.in_waiting > 0:
        ### Integer
        data = ser.read(ser.in_waiting)
        int_data = int.from_bytes(data, byteorder='big')
        print(f"Received: {data.hex()} ({int_data})")

        ### Hex
        # data = ser.read(ser.in_waiting)
        # hex_data = data.hex()
        # int_data = int(hex_data, 16)
        # print(f"Received: {hex_data}")
        # print(f"Received: {int_data}")

        ### Hex decode
        # data = ser.read(ser.in_waiting)
        # print(f"Received : {data.decode('utf-8')}")

# Example usage
data = 0
while True:
    # Range : 210 ~ 1050
    in_data = input("Enter PWM : ")
    if 210 <= int(in_data) <= 1050:  # Validate input
        byte_data = int(in_data).to_bytes(2, byteorder='big')
        send_data(byte_data)  # Send byte data
        time.sleep(0.1)  # Wait a bit for the STM32 to respond
        receive_data()  # Read the response from STM32
    else:
        print("Invalid input. Please enter 0 or 1.")
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
    print(f"Sending {data}")

# Function to receive data
def receive_data():
    # Wait for data to be available in the input buffer
    while ser.in_waiting > 0:
        # data = ser.read(ser.in_waiting).decode('utf-8')
        data = ser.read(ser.in_waiting)
        print(f"Received: {data}")

# Example usage
data = 0
while True:
    in_data = input("Enter 0 or 1: ")
    if in_data in ['0', '1']:  # Validate input
        byte_data = int(in_data).to_bytes(1, byteorder='big')
        send_data(byte_data)  # Send byte data
        time.sleep(0.1)  # Wait a bit for the STM32 to respond
        receive_data()  # Read the response from STM32
    else:
        print("Invalid input. Please enter 0 or 1.")

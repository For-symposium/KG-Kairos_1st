'''
Pin 8 (TX) -> Arduino Mega Pin 19 (RX1)
Pin 10 (RX) -> Arduino Mega Pin 18 (TX1)
GND -> GND (공통 그라운드 연결)
'''
import serial
import time

# Jetson Nano UART1 포트 (J41 Pin 8 & 10)
uart_port = '/dev/ttyTHS1'
baud_rate = 9600
i = 0

ser = serial.Serial(uart_port, baud_rate)

while True:
    if ser.in_waiting >= 1:  # 수신 대기 중인 데이터가 있을 때
        data = ser.read(1)  # 1바이트 읽기
        ToF_State = int.from_bytes(data, byteorder='little', signed=True)
        print("Received ToF_State:", ToF_State)


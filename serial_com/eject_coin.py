import serial
import time

# Open serial port (adjust '/dev/ttyUSB0' to the correct port your Arduino is connected to)
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2) # wait for the serial connection to initialize

def ten_eject():
    ser.write(b'T')  # Send byte command for ten yen eject
    print("Ten yen eject command sent")

def hundred_eject():
    ser.write(b'H')  # Send byte command for hundred yen eject
    print("Hundred yen eject command sent")

# Example usage
ten_eject()
time.sleep(1)  # Wait a bit between commands
hundred_eject()

import serial
import time

# Replace 'COM3' with the correct port name where your Arduino is connected
arduino = serial.Serial('/dev/tty.usbmodem149589401', 9600)
time.sleep(2) # Wait for the serial connection to initialize

def withdraw10Yen():
    arduino.write(b'a')

def withdraw100Yen():
    arduino.write(b'b')

def pickUp10Yen():
    arduino.write(b'c')

def pickUp100Yen():
    arduino.write(b'd')

# Example usage
    
pickUp10Yen()
time.sleep(1)
pickUp100Yen()
time.sleep(1)
withdraw10Yen()
time.sleep(1) # Delay to allow Arduino to process the command
withdraw100Yen()


arduino.close() # Close the serial connection

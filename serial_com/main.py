import serial
import time

# Open the serial port connected to Teensy
# Make sure to replace '/dev/ttyACM0' with your actual serial port
ser = serial.Serial('/dev/tty.usbmodem140279001', 9600)

time.sleep(2) # Wait for the connection to be established

while True:
    if ser.in_waiting > 0:
        incoming_message = ser.readline().decode('utf-8').rstrip()
        print(f"Received from Teensy: {incoming_message}")
        
        # Send a response
        ser.write("Hello from Raspberry Pi!\n".encode('utf-8'))

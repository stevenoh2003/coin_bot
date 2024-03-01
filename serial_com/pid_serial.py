import serial
import time

# Set up the serial connection (COM port might be different on your machine)
ser = serial.Serial('/dev/tty.usbmodem140279001', 9600, timeout=1)  # Update '/dev/ttyACM0' to your Arduino's serial port
time.sleep(2) # Wait for the connection to be established

# Function to send angle and read position
def send_angle_and_read_position(angle):
    ser.write(f"{angle}\n".encode())  # Send the angle to the Arduino
    while True:
        if ser.in_waiting > 0:
            position = ser.readline().decode().strip()  # Read the response from Arduino
            print(f"Position: {position}")
            break

# Example usage
send_angle_and_read_position(300)  # Send a target angle of 300

ser.close()  # Close the serial connection

import serial

# Configure the serial connection
import serial.tools.list_ports

# Check if COM6 is available
available_ports = [port.device for port in serial.tools.list_ports.comports()]
if 'COM6' not in available_ports:
    print("Error: COM6 is not available. Please check the connection.")
    input("Press Enter to exit...")
    exit(1)

try:
    ser = serial.Serial('COM6', baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Failed to open serial port: {e}")
    input("Press Enter to exit...")
    exit(1)

print("Connected to Raspberry Pi on COM6. Type 'exit' to quit.")

try:
    while True:
        # Get user input
        command = input("Enter command: ")
        if command.lower() == 'exit':
            print("Exiting terminal.")
            break

        # Send the command to the Raspberry Pi
        ser.write((command + '\n').encode('utf-8'))

        # Read and print the response
        response = ser.read(1024).decode('utf-8')
        print("Response:")
        print(response)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    ser.close()
    print("Serial connection closed.")

import serial
import serial.tools.list_ports

def get_serial_port_by_id(port_id):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Found port: {port.device}, HWID: {port.hwid}")
        if port_id in port.hwid:
            return port.device
    return None

def listen_to_serial(port_id, baudrate=9600, timeout=1):
    port = get_serial_port_by_id(port_id)
    if not port:
        print(f"Error: No serial port found with ID {port_id}")
        return

    try:
        # Open the serial port
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            print(f"Listening on {port} at {baudrate} baud...")
            while True:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"Received: {line}")
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    # Replace 'YOUR_PORT_ID' with the actual hardware ID of your serial device
    listen_to_serial(port_id='YOUR_PORT_ID')
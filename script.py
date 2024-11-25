import sys
from motort import Motor

def read_commands_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <port> <baudrate> <file>")
        sys.exit(1)

    port = sys.argv[1]
    baudrate = int(sys.argv[2])
    file_path = sys.argv[3]

    commands = read_commands_from_file(file_path)

    motor = Motor(baudrate)
    motor.send_ascii_commands(commands)
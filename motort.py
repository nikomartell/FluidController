import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1140
import time

class Motor:
    def __init__(self, baudrate):
        self.ser = None
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if 'FTDN6M3B' in port.hwid:
                try:
                    self.name = port.description
                    self.ser = serial.Serial(port.device, baudrate)
                    self.port = port
                    break
                except serial.SerialException as e:
                    self.ser = None
                    QMessageBox.critical(None, 'Error', f'Could not open port {port.device}: {e}')
        if self.ser is None:
            return self.ser

    def send_command(self, command):
        if self.ser:
            if not isinstance(command, str):
                command = str(command)
            self.ser.write(command.encode())
        else:
            raise Exception("Serial port not initialized")

    def read_response(self):
        if self.ser:
            return self.ser.readline().decode()
        else:
            raise Exception("Serial port not initialized")

    def send_binary_command(self, command):
        if self.ser:
            self.ser.write(command.to_bytes(1, byteorder='big'))
        else:
            raise Exception("Serial port not initialized")

    def enter_ascii_mode(self):
        self.send_binary_command(139)

    def send_ascii_commands(self, commands):
        self.enter_ascii_mode()
        for command in commands:
            self.send_command(command)
            response = self.read_response()
            print(f"Response: {response}")
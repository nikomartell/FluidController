import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import QMessageBox

class Motor:
    def __init__(self, ser, baudrate):
        self.name = None
        self.port = None
        self.ser = None
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if ser in port.hwid:
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
            self.ser.write(command.encode())
        else:
            raise Exception("Serial port not initialized")

    def read_response(self):
        if self.ser:
            return self.ser.readline().decode()
        else:
            raise Exception("Serial port not initialized")
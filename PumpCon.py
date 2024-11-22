import os
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import QMessageBox

class Component:
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
        
class PumpCon:
    def __init__(self, baudrate):
        self.name = 'Pump Controller'
        self.linearMotor = Component('FTDN6M3B', baudrate)
        self.rotaryMotor = Component('FTDN6FIV', baudrate)
        self.scale = Component('A9GKN3II', baudrate)
        self.errors = [None, None, None]
        self.commands = []
    
        if not self.linearMotor.ser:
            self.linearMotor = None
            self.errors[0] = 'Linear Motor not found '
        if not self.rotaryMotor.ser:
            self.rotaryMotor = None
            self.errors[1] = 'Rotary Motor not found '
        if not self.scale.ser:
            self.scale = None
            self.errors[2] = 'Scale not found '
    
    def get_commands(self):
        return self.commands
    
    def set_commands(self, commands):
        self.commands = commands

    def send_command(self, command):
        self.linearMotor.send_command(command)
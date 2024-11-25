import os
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import QMessageBox
from Scale import Scale
from Motor import Motor
        
class PumpCon:
    def __init__(self, baudrate):
        self.name = 'Pump Controller'
        self.linearMotor = Motor('FTDN6M3B', baudrate)
        self.rotaryMotor = Motor('A9GKN3II', baudrate)
        self.scale = Scale('FTDN6FIV', baudrate)
        self.errors = [None, None, None]
        self.stagedCommands = ''
        self.reply = None
    
        if not self.linearMotor.ser:
            self.linearMotor = None
            self.errors[0] = 'Linear Motor not found '
        if not self.rotaryMotor.ser:
            self.rotaryMotor = None
            self.errors[1] = 'Rotary Motor not found '
        if not self.scale.ser:
            self.scale = None
            self.errors[2] = 'Scale not found '


    # Sends commands to respective component (Linear Motor or Rotary Motor). One component used at a time
    def send_commands(self, commands):
        
        # Stage commands to be read properly
        self.stagedComponent = commands[0]
        self.stagedCommands = commands[1:]
        
        # Choose the correct device to send commands to
        match self.stagedComponent:
            case 'Linear Motor':
                if self.linearMotor is not None:
                    self.linearMotor.enter_ascii_mode()
                    for command in self.stagedCommands:
                        self.linearMotor.send_command(command)
                        self.linearMotor.read_response()
                else:
                    QMessageBox.critical(None, 'Error', 'Linear Motor not found')
            case 'Rotary Motor':
                if self.rotaryMotor is not None:
                    for command in self.stagedCommands:
                        self.rotaryMotor.send_command(command)
                    
                    self.rotaryMotor.read_response()
                else:
                    QMessageBox.critical(None, 'Error', 'Rotary Motor not found')
            case _:
                QMessageBox.critical(None, 'Error', 'Invalid component specified')
    
    def read_commands_from_file(self, file_path):
        if not os.path.isfile(file_path):
            QMessageBox.critical(None, 'Error', 'File not found')
            return
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        if not lines:
            QMessageBox.critical(None, 'Error', 'File is empty')
            return
        
        return lines
        

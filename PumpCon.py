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
        self.rotaryMotor = Motor('FTDN6FIV', baudrate)
        self.scale = Scale('A9GKN3II', baudrate)
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
    
    
    # Change to stage commands in appropriate commandline format
    def set_commands(self, commands):
        self.stagedComponent = commands[0]
        self.stagedCommands = commands[1:]
    
    # Sends commands to respective component (Linear Motor or Rotary Motor). One component used at a time
    def send_commands(self):
        # Choose the correct device to send commands to
        match self.stagedComponent:
            case 'Linear Motor':
                if self.linearMotor is not None:
                    for command in self.stagedCommands:
                        self.linearMotor.send_command(command)
                    
                    self.linearMotor.read_response()
                if self.rotaryMotor is not None:
                    for command in self.stagedCommands:
                        self.rotaryMotor.send_command(command)
                    
                    self.rotaryMotor.read_response()
                else:
                    QMessageBox.critical(None, 'Error', 'Motor not found')
                    self.rotaryMotor.send_command(command)
                
                self.rotaryMotor.read_response()
            case _:
                QMessageBox.critical(None, 'Error', 'Invalid component specified')
        
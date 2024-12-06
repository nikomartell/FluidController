import os
import serial
import serial.tools.list_ports
import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1140
from PyQt6.QtWidgets import QMessageBox
from Scale import Scale
from Motor import Motor
        
class Controller:
    def __init__(self):
        
        try: 
            interface1 = ConnectionManager().connect()
            interface2 = ConnectionManager().connect()
        except Exception as e:
            interface1 = None
            interface2 = None
        self.name = 'Pump Controller' 
        self.linearMotor = Motor(interface1)
        self.rotaryMotor = Motor(interface2)
        self.scale = Scale('COM4')
        self.errors = [None, None, None]
        self.stagedCommands = ''
        self.reply = None
    
        if not interface1:
            self.linearMotor = None
            self.errors[0] = 'Linear Motor not found '
        if not interface2:
            self.rotaryMotor = None
            self.errors[1] = 'Rotary Motor not found '
        if not self.scale.ser:
            self.scale = None
            self.errors[2] = 'Scale not found '


    # Sends commands to respective component (Linear Motor or Rotary Motor). One component used at a time
    def send_commands(self, commands):
        
        # Choose the correct device to send commands to
        match commands.component:
            case 'Linear Motor':
                if self.linearMotor is not None:
                    self.linearMotor.execute(commands)
                else:
                    QMessageBox.critical(None, 'Error', 'Linear Motor not found')
            case 'Rotary Motor':
                if self.rotaryMotor is not None:
                    self.rotaryMotor.execute(commands)
                    
                    self.rotaryMotor.read_response()
                else:
                    QMessageBox.critical(None, 'Error', 'Rotary Motor not found')
            case _:
                QMessageBox.critical(None, 'Error', 'Invalid component specified')
    
        

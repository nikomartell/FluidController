import os
import serial
import serial.tools.list_ports
import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from PyQt6.QtWidgets import QMessageBox
from Scale import Scale
from Motor import Motor
        
class Controller:
    def __init__(self):
        
        pytrinamic.show_info()
        connection_manager = ConnectionManager()
        try: 
            interface = connection_manager.connect()
        except Exception as e:
            interface = None
        self.name = 'Pump Controller' 
        module = TMCM3110(interface) if interface else None
        self.linear = Motor(module.motors[0]) if interface else None
        self.rotary = Motor(module.motors[1]) if interface else None
        self.scale = Scale('COM4')
        self.errors = [None, None, None]
        self.status = 0
    
        if not interface:
            self.linear = None
            self.errors[0] = 'Linear Motor not found '
        if not self.scale.ser:
            self.scale = None
            self.errors[2] = 'Scale not found '


    # Sends commands to respective component (Linear Motor or Rotary Motor). One component used at a time
    def send_commands(self, commands):
        self.status = 1
        print(self.rotary.motor.drive_settings)
        # Choose the correct device to send commands to
        try:
            match commands.component:
                case 'Linear Motor':
                    if self.linear is not None:
                        self.linear.execute(commands)
                    else:
                        QMessageBox.critical(None, 'Error', 'Linear Motor not found')
                case 'Rotary Motor':
                    if self.rotary is not None:
                        self.rotary.execute(commands)
                    else:
                        QMessageBox.critical(None, 'Error', 'Rotary Motor not found')
                case _:
                    QMessageBox.critical(None, 'Error', 'Invalid component specified')
        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Error: {e}')
            self.status = 0
        self.status = 0
    
    def stop(self):
        if self.linear.thread is not None:
            self.linear.thread.terminate()
        if self.rotary.thread is not None:
            self.rotary.thread.terminate()
    
        

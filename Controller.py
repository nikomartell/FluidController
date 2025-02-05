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
            with connection_manager.connect() as interface:

                self.name = 'Connected Components' 
                module = TMCM3110(interface) if interface else None
                self.motors = Motor(module.motors) if module else None
                self.scale = Scale('COM4')
                self.errors = [None, None, None]
                self.status = 0
            
                if not interface:
                    self.errors[0] = 'Linear Motor not found '
                    self.errors[1] = 'Rotary Motor not found '
                if not module.motors[0]:
                    self.errors[0] = 'Rotary Motor not found '
                if not module.motors[1]:
                    self.errors[1] = 'Linear Motor not found '
                if not self.scale.ser:
                    self.scale = None
                    self.errors[2] = 'Scale not found '
        except Exception as e:
            self.errors = [f'Error: {e}', None, None]
            self.motors = None
            self.scale = None
            self.status = 0
            

    # Sends commands to respective component (Linear Motor or Rotary Motor). One component used at a time
    def send_commands(self, commands):
        self.status = 1
        # Choose the correct device to send commands to
        if self.motors is None:
            return
        elif self.motors[0] is None:
            return
        elif self.motors[1] is None:
            return
        
        try:
            self.motors.execute(commands)
        except Exception as e:
            QMessageBox.critical(None, 'Error', 'Invalid component specified')
        
        self.status = 0
    
    def stop(self):
        if self.motors is None:
            QMessageBox.critical(None, 'Error', 'No motor found')
            return
        if self.motors.thread is not None:
            self.motors.thread.terminate()
            return
    
        

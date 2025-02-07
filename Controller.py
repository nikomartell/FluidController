import os
import serial
import serial.tools.list_ports
import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from PyQt6.QtWidgets import QMessageBox
from Scale import Scale
from Motor import Motor
import time
        
class Controller:
    def __init__(self):
        
        pytrinamic.show_info()
        connection_manager = ConnectionManager()
        self.module = None
        try:            
            with connection_manager.connect() as interface:

                self.name = 'Connected Components' 
                self.module = TMCM3110(interface)
                self.motors = Motor(self.module.motors)
                self.scale = None
                self.errors = [None, None, None]
                self.status = 0
            
                if not interface:
                    self.errors[0] = 'Linear Motor not found '
                    self.errors[1] = 'Rotary Motor not found '
                if not self.module.motors[0]:
                    self.errors[0] = 'Rotary Motor not found '
                if not self.module.motors[1]:
                    self.errors[1] = 'Linear Motor not found '
                if not self.scale:
                    self.scale = None
                    self.errors[2] = 'Scale not found '
        except Exception as e:
            print(e)
            self.module = TMCM3110(None)
            self.errors = [None , None, None]
            self.motors = Motor(self.module.motors)
            self.scale = Scale(None)
            self.status = 0
            

    # Sends commands to respective component (Linear Motor or Rotary Motor). One component used at a time
    def send_commands(self, commands):
        self.status = 1
        self.module.motors[0].rotate(1500)
        time.sleep(2)
        self.module.motors[0].stop()
        # Choose the correct device to send commands to
        if self.module.motors is None:
            return
        elif self.module.motors[0] is None:
            return
        elif self.module.motors[1] is None:
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
    
        

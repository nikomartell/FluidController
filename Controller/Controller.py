from pyftdi import *
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from PyQt6.QtCore import QDeadlineTimer, QObject
from Controller.Scale import Scale
        
class Controller(QObject):
    def __init__(self, interface=None):
        
        self.name = 'Pump Controller' 
        self.module = TMCM3110(interface) if interface else None
        self.rotary = self.module.motors[0] if interface else None
        self.linear = self.module.motors[1] if interface else None
        self.rotary_home = 6400
        if interface:
            self.linear.stop()
            self.rotary.stop()
        self.scale = Scale()
            #print(f'Error: {e}')
        self.errors = [None, None, None]
    
        if not interface:
            self.errors[0] = 'Rotary Motor not found'
            self.errors[1] = 'Linear Motor not found'
        if not self.scale.device:
            self.errors[2] = 'Scale not found'
    
    def set_motors(self, interface):
        self.module = TMCM3110(interface)
        self.linear = self.module.motors[0]
        self.rotary = self.module.motors[1]
        self.linear.stop()
        self.rotary.stop()
    
    
    def set_rotary_home(self, position):
        self.rotary_home = position
    
    def motor_settings(self):
        try:
            self.linear.max_acceleration = 500
            self.linear.max_velocity = 1175
            self.linear.drive_settings.max_current = 4
            self.linear.drive_settings.standby_current = 0
            self.linear.drive_settings.boost_current = 0
            
            self.rotary.max_acceleration = 1000
            self.rotary.max_velocity = 1000
            self.rotary.drive_settings.max_current = 4
            self.rotary.drive_settings.standby_current = 0
            self.rotary.drive_settings.boost_current = 0
            
        except Exception as e:
            print(f'Error: {e}')
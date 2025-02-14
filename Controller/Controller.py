import os
from ftd2xx import ftd2xx as ftd
import serial.tools.list_ports
import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDeadlineTimer, QObject
from Controller.Scale import Scale
from Controller.MotorThread import MotorThread
        
class Controller(QObject):
    def __init__(self):
        
        connection_manager = ConnectionManager()
        try: 
            interface = connection_manager.connect()
        except Exception as e:
            # print(f'Error: {e}')
            interface = None
        self.name = 'Pump Controller' 
        self.module = TMCM3110(interface) if interface else None
        self.linear = self.module.motors[0] if interface else None
        self.rotary = self.module.motors[1] if interface else None
        if interface:
            self.linear.stop()
            self.rotary.stop()
        self.scale = Scale()
            #print(f'Error: {e}')
        self.errors = [None, None, None]
    
        if not interface:
            self.errors[0] = 'Linear Motor not found'
            self.errors[1] = 'Rotary Motor not found'
        if not self.scale:
            self.errors[2] = 'Scale not found'
    
    def motor_settings(self):
        try:
            self.linear.max_acceleration = 500
            self.linear.max_velocity = 1175
            self.linear.drive_settings.max_current = 128
            self.linear.drive_settings.standby_current = 0
            self.linear.drive_settings.boost_current = 0
            self.linear.drive_settings.microstep_resolution = self.linear.ENUM.microstep_resolution_256_microsteps
            
            self.rotary.max_acceleration = 1000
            self.rotary.max_velocity = 1000
            self.rotary.drive_settings.max_current = 128
            self.rotary.drive_settings.standby_current = 0
            self.rotary.drive_settings.boost_current = 0
            self.rotary.drive_settings.microstep_resolution = self.linear.ENUM.microstep_resolution_256_microsteps
            
            self.linear.actual_position = 0
            self.rotary.actual_position = 0
        except Exception as e:
            print(f'Error: {e}')
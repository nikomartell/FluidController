import os
import serial
import serial.tools.list_ports
import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDeadlineTimer
from Scale import Scale
from MotorThread import MotorThread
        
class Controller:
    def __init__(self):
        
        pytrinamic.show_info()
        connection_manager = ConnectionManager()
        try: 
            interface = connection_manager.connect()
        except Exception as e:
            print(f'Error: {e}')
            interface = None
        self.name = 'Pump Controller' 
        self.module = TMCM3110(interface) if interface else None
        self.linear = self.module.motors[0] if interface else None
        self.rotary = self.module.motors[1] if interface else None
        self.scale = Scale('COM4')
        self.errors = [None, None, None]
    
        if not interface:
            self.errors[0] = 'Linear Motor not found'
            self.errors[1] = 'Rotary Motor not found'
        if not self.scale.ser:
            self.errors[2] = 'Scale not found'
            

    # Sends commands to respective component (Linear Motor or Rotary Motor). One component used at a time
    def send_commands(self, commands):
        # Choose the correct device to send commands to
        try:
            match commands.component:
                case 'Linear Motor':
                    if self.linear is not None:
                        self.linearProcess = MotorThread(motor=self.linear, command_set=commands)
                        self.linearProcess.finished.connect(lambda: print("Linear Motor finished"))
                        self.linearProcess.start()
                        self.linearProcess.wait(deadline=QDeadlineTimer(1000))
                    else:
                        QMessageBox.critical(None, 'Error', 'Linear Motor not found')
                case 'Rotary Motor':
                    if self.rotary is not None:
                        self.rotaryProcess = MotorThread(motor=self.rotary, command_set=commands)
                        self.rotaryProcess.finished.connect(lambda: print("Rotary Motor finished"))
                        self.rotaryProcess.start()
                        self.rotaryProcess.wait(deadline=QDeadlineTimer(1000))
                    else:
                        QMessageBox.critical(None, 'Error', 'Rotary Motor not found')
                case _:
                    QMessageBox.critical(None, 'Error', 'Invalid component specified')
        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Error: {e}')
            
    
    def stop(self):
        if self.linear.thread is not None:
            self.linearProcess.terminate()
        if self.rotary.thread is not None:
            self.rotaryProcess.terminate()
    
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
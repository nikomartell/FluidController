import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import time
from MotorThread import MotorThread

class Motor:
    def __init__(self, interface):
        self.motor = None
        self.thread = None
        
        try:
            self.motor = interface
            self.motor.max_acceleration = 1000
            self.motor.max_velocity = 1000
            self.motor.drive_settings.max_current = 128
            self.motor.drive_settings.standby_current = 0
            self.motor.drive_settings.boost_current = 0
            self.motor.drive_settings.microstep_resolution = self.motor.ENUM.microstep_resolution_256_microsteps
        except Exception as e:
            self.motor = None

        
    def execute(self, commandSet):
        # Check if the motor is connected
        if not self.motor:
            QMessageBox.critical(None, 'Error', 'Rotary Motor not found')
            return 0        # Return 0 if no execution
        
        # Move the motor to Default position
        try:
            # Run the command set for the specified number of iterations

            thread = MotorThread(interface=self.motor, command_set=commandSet)
            thread.finished.connect(lambda: print("Thread finished"))
            thread.start()
            
        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Error: {e}')
            return 0            # Return 0 if execution fails
        

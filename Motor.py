import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1140
from PyQt6.QtWidgets import QMessageBox
import time

class LinearMotor:
    def __init__(self):
        self.port = None
        self.connection = None
        self.module = None
        self.motor = None
        

        try:
            interface = ConnectionManager().connect()
            self.module = TMCM1140(interface)
            self.motor = self.module.motors[0]
        except Exception as e:
            self.connection = None
        if self.connection is None:
            return self.connection

        self.motor.drive_settings.max_current = 1000
        self.motor.drive_settings.standby_current = 0
        self.motor.drive_settings.boost_current = 0
        self.motor.drive_settings.microstep_resolution = self.motor.ENUM.MicrostepResolution256Microsteps
        
    def execute(self, commandSet):
        # Check if the motor is connected
        if not self.connection:
            QMessageBox.critical(None, 'Error', 'Rotary Motor not found')
            return
        
        self.motor.move_to(0)
        self.motor.rotate(commandSet.strokes)
        # 
        time.sleep(1)
        
        
class RotaryMotor:
    def __init__(self):
        self.port = None
        self.connection = None
        self.module = None
        self.motor = None
        

        try:
            interface = ConnectionManager().connect()
            self.module = TMCM1140(interface)
            self.motor = self.module.motors[1]
        except Exception as e:
            self.connection = None
        if self.connection is None:
            return self.connection

        self.motor.drive_settings.max_current = 1000
        self.motor.drive_settings.standby_current = 0
        self.motor.drive_settings.boost_current = 0
        self.motor.drive_settings.microstep_resolution = self.motor.ENUM.MicrostepResolution256Microsteps
        self.motor.linear_ramp.max_acceleration = 1000
        self.motor.linear_ramp.max_velocity = 1000

    def execute(self, commandSet):
        # Check if the motor is connected
        if not self.connection:
            QMessageBox.critical(None, 'Error', 'Rotary Motor not found')
            return
        
        # Move the motor to Default position
        self.motor.move_to(0)
        while not self.motor.get_position_reached():
            time.sleep(0.2)
        
        # Rotate the motor for flow rate at specified duration.
        if commandSet.flowDirection == 'Dispense':
            self.motor.rotate(commandSet.flowrate)
        elif commandSet.flowDirection == 'Aspirate':
            self.motor.rotate(-commandSet.flowrate)
        time.sleep(commandSet.duration)
        
        # Stop the motor
        self.motor.stop()
        

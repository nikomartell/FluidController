import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM1140
from PyQt6.QtWidgets import QMessageBox
import time

class Motor:
    def __init__(self, interface):
        self.port = None
        self.module = None
        self.motor = None
        
        try:
            self.module = TMCM1140(interface)
            self.motor = self.module.motors[0]
        except Exception as e:
            self.module = None
        if self.module is None:
            return self.module

        
    def execute(self, commandSet):
        # Check if the motor is connected
        if not self.module:
            QMessageBox.critical(None, 'Error', 'Rotary Motor not found')
            return 0        # Return 0 if no execution
        
        # Move the motor to Default position
        while int(commandSet.iterations) > 0:
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
            commandSet.iterations -= 1
        return 1            # Return 1 if execution is successful
        

import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from PyQt6.QtWidgets import QMessageBox
import time
from MotorThread import MotorThread

class Motor:
    def __init__(self, interface):
        self.motor = None
        self.thread = None
        
        try:
            self.motor = interface
        except Exception as e:
            self.motor = None

        
    def execute(self, commandSet):
        
        # Move the motor to Default position
        try:
            # Run the command set for the specified number of iterations
            
            thread = MotorThread(interface=self.motor, command_set=commandSet)
            thread.finished.connect(lambda: print("Thread finished"))
            try:
                thread.start()
            except (KeyboardInterrupt, SystemExit):
                thread.stop()
                thread.wait()
                thread.finished.emit()
                return 0
            
            
            self.motor.stop()
                
            if commandSet.iterations == 0:
                QMessageBox.information(None, 'Success', 'Motor executed successfully')
                return 1            # Return 1 if execution
            else:
                QMessageBox.critical(None, 'Error', 'Motor execution interrupted')
                return 2            # Return 2 if execution is interrupted
            

        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Error: {e}')
            return 0            # Return 0 if execution fails
        

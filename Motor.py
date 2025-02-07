import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from PyQt6.QtWidgets import QMessageBox
import time
from MotorThread import MotorThread

class Motor:
    def __init__(self, interface):
        self.module = interface
        self.thread = None
        self.rotary = self.module[0] if self.module[0] else None
        self.linear = self.module[1] if self.module[1] else None

        
    def execute(self, commandSet):
        
        # Move the motor to Default position
        try:
            # Run the command set for the specified number of iterations
            print(self.rotary.drive_settings)
            print(self.linear.drive_settings)
            self.thread = MotorThread(self.rotary, self. linear, commandSet)
            self.thread.finished.connect(lambda: print("Thread finished"))
            try:
                self.thread.start()
                while self.thread._is_running:
                    time.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                self.thread.stop()
                self.thread.wait()
                self.thread.finished.emit()
            

        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Error in Motor Class: {e}')
            return 0            # Return 0 if execution fails
        

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
import time

class MotorThread(QThread):
    finished = pyqtSignal()

    def __init__(self, interface, command_set):
        super().__init__()
        self.motor = interface
        self.command_set = command_set
        self._is_running = True

    def run(self):
        try:
            while self._is_running:
                
                while self.command_set.iterations > 0:      # Run the command set for the specified number of iterations
                    if self.command_set.flowDirection == 'Dispense':
                        self.motor.rotate(self.command_set.flowRate)
                    elif self.command_set.flowDirection == 'Aspirate':
                        self.motor.rotate(-self.command_set.flowRate)
                    time.sleep(self.command_set.duration)   # Run for the specified duration
                    
                    self.motor.stop()   # Stop the motor for 3 seconds before starting the next iteration
                    time.sleep(3)
                    
                    self.command_set.iterations -= 1
                    if self.command_set.iterations == 0:
                        break
        except Exception as e:
            print(f'Error: {e}')
        self.finished.emit()

    def stop(self):
        self._is_running = False
        self.motor.stop()

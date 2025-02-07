from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
import time

class MotorThread(QThread):
    finished = pyqtSignal()

    def __init__(self, rotary, linear, command_set):
        super().__init__()
        self.rotary = rotary
        self.linear = linear
        self.command_set = command_set
        self._is_running = True

    def run(self):
        try:
            while self._is_running:
                while self.command_set.iterations > 0:      # Run the command set for the specified number of iterations
                    if self.command_set.flowDirection == 'Dispense':
                        self.rotary.rotate(self.command_set.flowRate)
                    elif self.command_set.flowDirection == 'Aspirate':
                        self.rotary.rotate(-self.command_set.flowRate)
                    time.sleep(self.command_set.duration)   # Run for the specified duration
                    
                    self.rotary.stop()   # Stop the rotary for 3 seconds before starting the next iteration
                    time.sleep(3)
                    
                    self.command_set.iterations -= 1
                    if self.command_set.iterations == 0:
                        break
        except Exception as e:
            print(f'Error in Motor Process: {e}')
            self.finished.emit()
        finally:
            self.finished.emit()

    def stop(self):
        self._is_running = False
        self.rotary.stop()
        self.finished.emit()

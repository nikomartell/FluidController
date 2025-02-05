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
        # Move the motor to Default position
        try:
            while self._is_running:
                # Rotate the motor at the set flow rate for the specified duration.
                if self.command_set.flowDirection == 'Dispense':
                    self.motor.rotate(self.command_set.flowRate)
                elif self.command_set.flowDirection == 'Aspirate':
                    self.motor.rotate(-self.command_set.flowRate)
                time.sleep(self.command_set.duration)
                self.motor.stop()
                break
        except Exception as e:
            print(f'Error: {e}')
        self.finished.emit()

    def stop(self):
        self._is_running = False
        self.motor.stop()

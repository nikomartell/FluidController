from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject, QThread
import time

class MotorThread(QRunnable):

    def __init__(self, controller, command_set):
        super().__init__()
        self.controller = controller
        self.command_set = command_set
        self.signals = MotorSignal()
        self._is_running = False

    def quit(self):
        self._is_running = False

    def run(self):
        self._is_running = True
        if self.controller is not None:
            match self.command_set.component:
                case 'Linear Motor':
                    self.motor = self.controller.linear
                case 'Rotary Motor':    
                    self.motor = self.controller.rotary
                case _:
                    QMessageBox.critical(None, 'Error', f'Error: {e}')
                        
        # Move the motor to Default position
        try:
            print(self.motor.drive_settings)
            self.signals.running.emit()
            while self.command_set.iterations > 0 and self._is_running:
                
                if self.motor.actual_position != 0:
                    self.motor.move_to(0)
                    while self.motor.actual_position != 0:
                        if not self._is_running:
                            self.motor.stop()
                            break
                        time.sleep(0.1)
                        
                
                time.sleep(1)
                if not self._is_running:
                    break
                
                start_time = time.time()
                self.signals.start.emit()
                while time.time() - start_time < self.command_set.duration and self._is_running:
                    self.task()
                    time.sleep(0.1)
                
                self.motor.stop()
                self.command_set.iterations -= 1
                if not self._is_running:
                    break
                time.sleep(2)
                
        except Exception as e:
            print(f'Error: {e}')
        finally:
            if self._is_running:
                self._is_running = False
                print('Motor Thread Finished')
                self.signals.finished.emit()
            else:
                print('Motor Thread Stopped')
                self.signals.finished.emit()

    
    
    def task(self):
            # Rotate the motor at the set flow rate for the specified duration.
            if self.command_set.flowDirection == 'Dispense':
                self.motor.rotate(self.command_set.flowRate)
            elif self.command_set.flowDirection == 'Aspirate':
                self.motor.rotate(-self.command_set.flowRate)
        

class MotorSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    running = pyqtSignal()
    start = pyqtSignal()
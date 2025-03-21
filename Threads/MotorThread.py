from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject, QThread
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
import time

class MotorThread(QObject, QRunnable):

    def __init__(self, controller = Controller(), command_set = CommandSet()):
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
            
            # While the thread is running and there are still iterations left, keep running the motor
            while self.command_set.iterations > 0 and self._is_running:
                
                self.signals.toZero.emit()
                # If the motor is not at the default position, move it to the default position
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
                # Base time running off current time
                start_time = time.time()
                self.signals.start.emit()
                
                # While the motor is running, keep rotating the motor at the set flow rate
                while time.time() - start_time < self.command_set.duration and self._is_running:
                    self.task()
                    time.sleep(0.1)
                
                self.motor.stop()
                
                # Decrement the number of iterations
                self.command_set.iterations -= 1
                
                # If set to stop running, break out of the loop
                if not self._is_running:
                    break
                time.sleep(2)
            self._is_running = False
                
        except Exception as e:
            print(f'Error: {e}')
        finally:
            # If not forced off, emit the finished signal
            # If forced off, emit the stopped signal
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
    toZero = pyqtSignal()
    start = pyqtSignal()
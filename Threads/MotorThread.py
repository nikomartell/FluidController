from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject, QThread
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
import time

class MotorThread(QThread):

    def __init__(self, controller, command_set = CommandSet()):
        super().__init__()
        self.controller = controller
        self.command_set = command_set
        self.signals = MotorSignal()
        self._is_running = False

    def quit(self):
        self._is_running = False

    def run(self):
        self._is_running = True
        self.command_set.print()
        self.signals.start.emit()
        
        interval = 0.0001
        
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
                        time.sleep(interval)
                        
                
                time.sleep(1)
                if not self._is_running:
                    break
                # Base time running off current time
                self.signals.execute.emit()
                
                self.task()
                timer = 0
                # While the motor is running, keep rotating the motor at the set flow rate
                while timer < self.command_set.duration and self._is_running:
                    time.sleep(interval)
                    timer += interval
                
                self.signals.finished.emit()
                self.motor.stop()
                
                # Decrement the number of iterations
                self.command_set.iterations -= 1
                
                # If set to stop running, break out of the loop
                if not self._is_running:
                    break
                
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
                self.motor.rotate(self.command_set.speed)
            elif self.command_set.flowDirection == 'Aspirate':
                self.motor.rotate(-self.command_set.speed)
        

class MotorSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    toZero = pyqtSignal()
    execute = pyqtSignal()
    start = pyqtSignal()
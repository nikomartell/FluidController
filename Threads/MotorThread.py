from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject, QThread
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
from pytrinamic.modules import TMCM3110
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
        
        interval = 0.0001
        
        self.signals.start.emit()
        if isinstance(self.controller, Controller):
            match self.command_set.component:
                case 'Linear Motor':
                    self.motor = self.controller.linear
                case 'Rotary Motor':    
                    self.motor = self.controller.rotary
                case _:
                    QMessageBox.critical(None, 'Error', f'Error: {e}')
        else:
            QMessageBox.critical(None, 'Error', 'Error: Controller not found')
            self.signals.finished.emit()
            return
        
        # Move the motor to Default position
        try:
            print(self.motor.drive_settings)
            
            # While the thread is running and there are still iterations left, keep running the motor
            while self.command_set.iterations > 0 and self._is_running:
                
                # -----------------------Zeroing-------------------------- #
                
                # If the motor is not at the default position, move it to the default position
                self.signals.toZero.emit()
                while self.motor.actual_position != 0:
                    if self.motor.actual_position > 0:
                        self.motor.move_to(0, velocity=-100)
                    elif self.motor.actual_position < 0:
                        self.motor.move_to(0, velocity=100)
                        
                    # If the thread is not running, stop the motor and break out of the loop
                    if not self._is_running:
                        self.motor.stop()
                        break
                    
                    #time.sleep(interval)
                    
                # -----------------------Zeroing Finished-------------------------- #    
                
                time.sleep(1)
                
                if not self._is_running:
                    break
                
                # -----------------------Starting Task-------------------------- #
                
                self.signals.execute.emit()
                self.task()
                timer = 0
                # While the motor is running, keep rotating the motor at the set Flow Rate
                while timer < self.command_set.duration & self._is_running:
                    time.sleep(interval)
                    timer += interval
                
                self.signals.finished.emit()
                self.motor.stop()
                
                # Decrement the number of iterations
                self.command_set.iterations -= 1
                
                # If set to stop running, break out of the loop
                if not self._is_running:
                    break
                
                # ----------------Task Finished-------------------------- #
                
        except Exception as e:
            print(f'Error: {e}')
        finally:
            # If not forced off, emit the finished signal
            if self._is_running:
                self._is_running = False
                print('Motor Thread Finished')
                self.signals.finished.emit()
            
            # If forced off, emit the stopped signal
            else:
                print('Motor Thread Stopped')
                self.signals.finished.emit()

    
    
    def task(self):
            # Rotate the motor at the set Flow Rate for the specified duration.
            self.motor.max_acceleration = self.command_set.acceleration
            self.motor.max_velocity = self.command_set.speed
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
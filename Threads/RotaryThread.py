from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject, QThread
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
from pytrinamic.modules import TMCM3110
import time

class RotaryThread(QThread):

    def __init__(self, controller, command_set = CommandSet):
        super().__init__()
        self.controller = controller
        self.command_set = command_set
        self.signals = MotorSignal()
        self.motor = controller.rotary
        self._is_running = False

    def quit(self):
        self._is_running = False

    def run(self):
        self._is_running = True
        try:
            for command in self.command_set:
                if isinstance(command, CommandSet):
                    pass
                if not isinstance(command, CommandSet):
                    raise TypeError(f'Expected str, got {type(command)}')
                
                command.print()
                
                
                self.signals.start.emit()
                if isinstance(self.controller, Controller):  
                    self.motor = self.controller.rotary
                
                # Move the motor to Default position
                try:
                    print(self.motor.drive_settings)
                    
                    # While the thread is running and there are still iterations left, keep running the motor
                    while command.iterations > 0 and self._is_running:
                        
                        # -----------------------Zeroing-------------------------- #
                        home = self.controller.rotary_home
                        position = self.motor.get_actual_position() % home
                        self.motor.set_actual_position(position)
                        # If the motor is not at the default position, move it to the default position
                        self.signals.toZero.emit()
                        
                        while self.motor.actual_position != 0:
                            self.motor.move_to(0, velocity=100)
                            # If the thread is not running, stop the motor and break out of the loop
                            if not self._is_running:
                                self.motor.stop()
                                break
                            
                            #time.sleep(interval)
                            
                        # -----------------------Zeroing Finished-------------------------- #    
                        
                        time.sleep(2)
                        
                        if not self._is_running:
                            break
                        
                        # -----------------------Starting Task-------------------------- #
                        
                        self.signals.execute.emit()
                        self.task(command)
                        start_time = time.time()
                        timer = 0
                        duration = float(command.duration)
                        total_steps = command.strokes * self.controller.rotary_home
                        # While the motor is running, keep rotating the motor at the set Flow Rate
                        while timer < duration and self._is_running:
                            if abs(self.motor.actual_position) == total_steps:
                                self.motor.stop()
                                break
                            
                            print('Current Position:', self.motor.get_actual_position())
                            timer = time.time() - start_time
                            timer = round(timer, 2)
                            print('Timer:', timer)
                        
                        self.signals.finished.emit()
                        self.motor.stop()
                        
                        position_adjust = self.motor.actual_position % self.controller.rotary_home
                        self.motor.set_actual_position(position_adjust)
                        # Decrement the number of iterations
                        command.iterations -= 1
                        
                        # If set to stop running, break out of the loop
                        if not self._is_running:
                            break
                except Exception as e:
                    print(f'Error: {e}')
                    # ----------------Task Finished-------------------------- #
                
        except Exception as e:
            print(f'Error: {e}')
        finally:
            # If not forced off, emit the finished signal
            if self._is_running:
                self._is_running = False
                print('Motor Thread Finished')
                print('Motor Position:', self.motor.get_actual_position())
                self.signals.finished.emit()
            
            # If forced off, emit the stopped signal
            else:
                print('Motor Thread Stopped')
                print('Motor Position:', self.motor.get_actual_position())
                self.signals.finished.emit()

    
    
    def task(self, command):
        if isinstance(command, CommandSet):
            # Rotate the motor at the set Flow Rate for the specified duration.
            self.motor.max_acceleration = command.acceleration
            
            total_steps = 0
            speed = 0
            if command.flow_direction == 'Dispense':
                speed = command.speed
                total_steps = command.strokes * self.controller.rotary_home
            elif command.flow_direction == 'Aspirate':
                speed = -command.speed
                total_steps = -command.strokes * self.controller.rotary_home
            
            if total_steps != 0:
                self.motor.move_to(total_steps, velocity=speed)
            else:
                self.motor.rotate(speed)
        else:
            raise TypeError(f'Expected CommandSet, got {type(command)}')

class MotorSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    toZero = pyqtSignal()
    execute = pyqtSignal()
    start = pyqtSignal()
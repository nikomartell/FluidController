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
                
                interval = 0.0001
                
                self.signals.start.emit()
                if isinstance(self.controller, Controller):
                    match command.component:
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
                    while command.iterations > 0 and self._is_running:
                        
                        # -----------------------Zeroing-------------------------- #
                        home = self.controller.rotary_home
                        position = self.motor.get_actual_position() % home
                        self.motor.set_actual_position(position)
                        # If the motor is not at the default position, move it to the default position
                        self.signals.toZero.emit()
                        self.motor.move_to(0, velocity=100)
                        while self.motor.actual_position != 0:
                            
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
                        timer = 0
                        duration = command.duration
                        total_steps = command.strokes * self.controller.rotary_home
                        # While the motor is running, keep rotating the motor at the set Flow Rate
                        while (timer < duration) & self._is_running & (self.motor.actual_position != total_steps):
                            print('Current Position:', self.motor.get_actual_position())
                            time.sleep(interval)
                            timer += interval
                        
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
            self.motor.max_velocity = command.speed
            if command.strokes > 0:
                total_steps = command.strokes * self.controller.rotary_home
                if command.flowDirection == 'Dispense':
                    self.motor.move_to(total_steps, velocity=command.speed)
                elif command.flowDirection == 'Aspirate':
                    self.motor.move_to(-total_steps, velocity=command.speed)
            else:
                self.motor.rotate(command.speed)
        else:
            raise TypeError(f'Expected CommandSet, got {type(command)}')

class MotorSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    toZero = pyqtSignal()
    execute = pyqtSignal()
    start = pyqtSignal()
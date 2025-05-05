from PyQt6.QtCore import pyqtSignal, QObject, QThread
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
import time

class MotorThread(QThread):

    def __init__(self, controller, command_set = CommandSet):
        super().__init__()
        self.controller = controller
        self.command_set = command_set
        self.signals = MotorSignal()
        self.rotary = self.controller.rotary
        self.linear = self.controller.linear
        self._is_running = False

    def quit(self):
        self._is_running = False

    def run(self):
        
        self._is_running = True
        if isinstance(self.controller, Controller):
            self.rotary = self.controller.rotary
            self.linear = self.controller.linear
            print(self.rotary.drive_settings)

        try:
            for command in self.command_set:
                if isinstance(command, CommandSet):
                    command.print()
                else:
                    raise TypeError(f'Expected CommandSet, got {type(command)}')
                
                self.signals.start.emit()
                
                # Move the rotary to Default position
                try:
                    
                    # While the thread is running and there are still iterations left, keep running the rotary
                    while command.iterations > 0 and self._is_running:
                        
                        # -----------------------Zeroing-------------------------- #
                        
                        self.zero(command)
                        while self.rotary.actual_position != 0:
                            print(self.linear.actual_position)
                            print(self.rotary.actual_position)
                        
                            
                        # -----------------------Zeroing Finished-------------------------- #    
                        
                        time.sleep(1)
                        
                        if not self._is_running:
                            break
                        
                        # -----------------------Starting Task-------------------------- #
                        
                        self.signals.execute.emit()
                        self.task(command)
                        start_time = time.time()
                        timer = 0
                        duration = float(command.duration)
                        total_steps = command.strokes * self.controller.rotary_home
                        
                        # While the rotary is running, keep rotating the rotary at the set Flow Rate
                        while timer < duration and self._is_running:
                            if abs(self.rotary.actual_position) == total_steps:
                                self.rotary.stop()
                                break
                            
                            print('Current Position:', self.rotary.get_actual_position())
                            timer = time.time() - start_time
                            timer = round(timer, 2)
                            print('Timer:', timer)
                        
                        self.signals.finished.emit()
                        self.rotary.stop()
                        
                        position_adjust = self.rotary.actual_position % self.controller.rotary_home
                        self.rotary.set_actual_position(position_adjust)
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
                print('Motor Position:', self.rotary.get_actual_position())
                self.signals.complete.emit()
            
            # If forced off, emit the stopped signal
            else:
                print('Motor Thread Stopped')
                print('Motor Position:', self.rotary.get_actual_position())
                self.signals.complete.emit()

    
    
    def task(self, command):
        if isinstance(command, CommandSet):
            # Rotate the rotary at the set Flow Rate for the specified duration.
            self.rotary.max_acceleration = command.acceleration
            
            total_steps = 0
            speed = abs(command.speed)
            if command.flow_direction == 'Dispense':
                speed = speed if speed <= 1500 else 1500
                total_steps = command.strokes * self.controller.rotary_home
            elif command.flow_direction == 'Aspirate':
                speed = -speed if speed <= 1500 else 1500
                total_steps = -command.strokes * self.controller.rotary_home
            
            if total_steps != 0:
                self.rotary.move_to(total_steps, velocity=speed)
            else:
                self.rotary.rotate(speed)
        else:
            raise TypeError(f'Expected CommandSet, got {type(command)}')
        
        
    def zero(self, command):
        if isinstance(self.controller, Controller):
            # Set the position of the motor in reference to the Home position
            position = self.rotary.get_actual_position() % self.controller.rotary_home
            self.rotary.set_actual_position(position)
            
            
            self.signals.toZero.emit()
            
            if isinstance(command.position, int):
                
                if command.position > 42000:
                    print('linear Position to high; Defaulting to highest position of 4600')
                    command.position = 42000
                    
                elif command.position < 0:
                    print('linear position is too low; Defaulting to lowest position of -1600')
                    command.position = 0
                
                self.linear.move_to(22000)
                while self.linear.actual_position != 22000:
                    time.sleep(0.1)
            
            # If the rotary is not at the default position, move it to the default position
            self.rotary.move_to(0, velocity=100)
            while self.rotary.actual_position != 0:
                # If the thread is not running, stop the rotary and break out of the loop
                if not self._is_running:
                    self.rotary.stop()
                    break
        else:
            raise TypeError(f'Controller Expected for Zeroing, got {type(self.controller)}')

class MotorSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    complete = pyqtSignal()
    toZero = pyqtSignal()
    execute = pyqtSignal()
    start = pyqtSignal()
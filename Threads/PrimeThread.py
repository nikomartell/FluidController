from PyQt6.QtCore import pyqtSignal, QObject, QThread
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
import time

class PrimeThread(QThread):
    def __init__(self, controller):
        super().__init__()
        # setting up
        self.in1 = 5
        self.signals = PrimeSignals()
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.IN)
        
        super().__init__()
        self._is_running = False
        self.controller = controller
        self._is_running = False
        
    def quit(self):
        self._is_running = False
        self.rotary.stop()
        
    def run(self):
        self._is_running = True
        if isinstance(self.controller, Controller):
            self.rotary = self.controller.rotary
            
        while self._is_running:
            self.rotary.move_by(self.controller.rotary_home, velocity=100)
            if GPIO.input(self.in1) == GPIO.HIGH:
                self.signals.primed.emit()
                break
            time.sleep(0.0001)
        time.sleep(1)
        
        self.controller.adjust_position()
            
class PrimeSignals(QObject):
    start = pyqtSignal()
    primed = pyqtSignal()
    not_primed = pyqtSignal()
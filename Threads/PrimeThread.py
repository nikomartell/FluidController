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
        # This mainly crashes when attempting to use GPIO off the Raspberry Pi
        # So this allows the user to test it off the Pi
        try:
            self.in1 = 5
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.in1, GPIO.IN)
        except Exception as e:
            print("Unable to initialize Priming Funtion", e)
        self.signals = PrimeSignals()
        self._is_running = False
        self.controller = controller
        self._is_running = False
        
    def quit(self):
        self._is_running = False
        self.rotary.stop()
        
    def run(self):
        self._is_running = True
        self.signals.start.emit()
        if isinstance(self.controller, Controller):
            self.rotary = self.controller.rotary
            
        while self._is_running:
            self.rotary.move_by(self.controller.rotary_home, velocity=500)
            print(self.rotary.actual_position)
            if GPIO.input(self.in1) == GPIO.LOW:
                self.signals.primed.emit()
                break
            time.sleep(0.1)
        time.sleep(0.5)
        self.rotary.stop()
        self.controller.adjust_position()
            
class PrimeSignals(QObject):
    start = pyqtSignal()
    primed = pyqtSignal()
    not_primed = pyqtSignal()
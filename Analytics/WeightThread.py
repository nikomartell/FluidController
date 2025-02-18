from PyQt6.QtWidgets import QMessageBox
from ftd2xx import ftd2xx as ftd
import time
from PyQt6.QtCore import QThread, pyqtSignal, QObject

class WeightThread(QThread):
    def __init__(self, scale):
        super().__init__()
        self.scale = scale
        self.signals = WeightSignal()
        self.weight = 0.00
        self._is_running = True

    def quit(self):
        self._is_running = False

    def run(self):
        try:
            while self._is_running:
                if self.scale.device:
                    self.signals.result.emit(self.scale.get_weight())
                    time.sleep(0.01)
                if not self._is_running:
                    break
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.signals.finished.emit()
                
class WeightSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
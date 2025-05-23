from PyQt6.QtWidgets import QMessageBox
from Controller.Scale import Scale
import time
from PyQt6.QtCore import pyqtSignal, QObject, QThread

class WeightThread(QThread):
    def __init__(self, scale, precision = 3):
        super().__init__()
        self.scale = scale
        self.signals = WeightSignal()
        self.weight = 0.00
        self._is_running = True
        self.precision = precision

    def quit(self):
        self._is_running = False

    def run(self):
        if isinstance(self.scale, Scale):
            print('Weight Thread Running')
            while self._is_running:
                try:
                    if self.scale.device:
                        queue = self.scale.device.getQueueStatus()
                        if queue >= 16:
                            self.signals.result.emit(self.scale.get_weight())
                    if not self._is_running:
                        break
                except Exception as e:
                    print(f'Error: {e}')
            if self.scale.device:
                try:
                    self.scale.device.purge()  # Clear the input and output buffers
                    self.scale.device.close()  # Close the device
                except Exception as e:
                    print(f'Error: {e}')
                    self.signals.error.emit((e, 'WeightThread'))
            self.signals.finished.emit()
    
    # This is the primary way to tare the scale.
    # Using it directly through the scale can freeze the UI
    def tare(self):
        try:
            if isinstance(self.scale, Scale):
                self.scale.tare()
            self.scale.tare()
        except Exception as e:
            QMessageBox.critical(None, 'Error', {e})
                
class WeightSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
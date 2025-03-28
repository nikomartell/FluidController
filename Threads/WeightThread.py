from PyQt6.QtWidgets import QMessageBox
from ftd2xx import ftd2xx as ftd
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
            interval = 10 ** -self.precision
            print('Weight Thread Running')
            try:
                while self._is_running:
                    if self.scale.device:
                        self.signals.result.emit(self.scale.get_weight())
                        time.sleep(interval)
                    if not self._is_running:
                        break
            except Exception as e:
                print(f'Error: {e}')
            finally:
                if self.scale.device:
                    self.scale.device.purge()  # Clear the input and output buffers
                    self.scale.device.close()  # Close the device
                self.signals.finished.emit()
    
    # This is the primary way to tare the scale.
    # Using it directly through the scale can freeze the UI
    def tare(self):
        try:
            self.scale.tare()
            time.sleep(1)
        except Exception as e:
            QMessageBox.critical(None, 'Error', {e})
                
class WeightSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
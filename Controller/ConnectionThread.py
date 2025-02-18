from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QThread
from pytrinamic.connections import ConnectionManager
from Controller.Controller import Controller
import time, traceback, sys

class ConnectionThread(QThread):
    
    def __init__(self):
        super().__init__()
        self.con = Controller()
        self.signals = ConnectionSignal()
        self.interface = ConnectionManager()
        self._is_running = True
        
        
    def run(self):
        try:
            # While Connection is not established, keep trying to connect
            while self._is_running:
                if self.con.module is None:
                    self.con = Controller()
                    time.sleep(2)
                else:
                    self.signals.connected.emit()
                    break
                
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()
        
    def quit(self):
        self._is_running = False
        
class ConnectionSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    connected = pyqtSignal()
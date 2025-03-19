from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QThread
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from Controller.Controller import Controller
from Controller.Scale import Scale
import time, traceback, sys

class ConnectionThread(QObject, QRunnable):
    
    def __init__(self):
        super().__init__()
        self.signals = ConnectionSignal()
        self.connection_manager = ConnectionManager()
        self._is_running = True
        
        
    def run(self):
        con = Controller()
        try:
            while self._is_running:
                # While no Connections are established, keep trying to connect
                if not con.module:
                    con = Controller()
                    time.sleep(2)
                else:
                    self.signals.result.emit(con)
                    break
                if not self._is_running:
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
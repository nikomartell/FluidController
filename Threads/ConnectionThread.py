from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QThread
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from Controller.Controller import Controller
from Controller.Scale import Scale
import time, traceback, sys

class ConnectionThread(QThread):
    
    def __init__(self):
        super().__init__()
        self.signals = ConnectionSignal()
        self.connection_manager = ConnectionManager()
        self._is_running = True
        
        
    def run(self):
        con = Controller()
        attempts = 0
        try:
            while self._is_running:
                # While no Connections are established, keep trying to connect
                try:
                    interface = self.connection_manager.connect()
                    con = Controller(interface)
                    if interface:
                        self.signals.result.emit(con)
                        self.signals.connected.emit()
                        break
                    
                except Exception as e:
                    print(f'Error: {e}')
                    
                attempts += 1
                if attempts == 3:
                    self.signals.error.emit((Exception, "Connection Failed", "Could not connect to any devices."))
                    break
                time.sleep(1)
                    
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
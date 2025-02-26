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
        self.con = Controller()
        self.signals = ConnectionSignal()
        self.connection_manager = ConnectionManager()
        self._is_running = True
        
        
    def run(self):
        try:
            while self._is_running:
                # While no Connections are established, keep trying to connect
                while not self.con.module or not self.con.scale.device:
                    # If neither the module nor the scale are connected, try to connect to both
                    if not self.con.module and not self.con.scale.device:
                        try:
                            self.con = Controller()
                        except:
                            pass
                    # If one is not connected, try to connect to it.
                    else:
                        if not self.con.module:
                            try:
                                interface = self.connection_manager.connect()
                                self.con.module = TMCM3110(interface)
                                self.con.linear = self.con.module.motors[0]
                                self.con.rotary = self.con.module.motors[1]
                                self.con.linear.stop()
                                self.con.rotary.stop()
                            except:
                                pass
                        if not self.con.scale.device:
                            self.con.scale = Scale()
                        self.signals.connected.emit()
                    time.sleep(1)
                    if not self._is_running:
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
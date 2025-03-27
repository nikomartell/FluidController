from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QThread
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
from Controller.Controller import Controller
from Controller.Scale import Scale
import time, traceback, sys

class ConnectionThread(QThread):
    
    def __init__(self, con):
        super().__init__()
        self.signals = ConnectionSignal()
        self._is_running = True
        self.con = con
        
        
    def run(self):
            
        if not isinstance(self.con, Controller):
            return
        
        if self.con.module is None:
            try:
                # While no Connections are established, keep trying to connect
                with ConnectionManager().connect() as interface:
                    self.con.set_motors(interface)
                    self.signals.connected.emit()
                    
            except Exception as e:
                print(f'Error: {e}')
        
        if self.con.scale.device is None:
            try:
                self.con.scale = Scale()
                self.signals.connected.emit()
            except Exception as e:
                print(f'Error: {e}')
                traceback.print_exc()
        
        self.signals.result.emit(self.con)
        self.signals.finished.emit()
        
    def quit(self):
        self._is_running = False
        
class ConnectionSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    connected = pyqtSignal()
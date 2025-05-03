import sys
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject, QThread, QMutex, QWaitCondition
from Controller.Scale import Scale
import time
import traceback
import pandas as pd

class GraphThread(QThread):
    
    def __init__(self, scale, precision = 1):
        super().__init__()
        self.signals = GraphSignal()
        self._paused = False
        self._pause_mutex = QMutex()
        self._pause_condition = QWaitCondition()
        self._is_running = True
        self.scale = scale
        self.precision = precision
        self.time = 0
    
    # X is time, Y is weight
    def run(self):
        try:
            # This specifies the interval of time between each data point
            interval = 10 ** -self.precision
            
            # While the thread is running, keep updating the graph with new data
            while self._is_running:
                
                if self._paused:
                    self._pause_mutex.lock()
                    self._pause_condition.wait(self._pause_mutex)
                    self._pause_mutex.unlock()
                    
                else:
                    self.time += interval
                    self.time = round(self.time, self.precision)
                    self.signals.result.emit(self.time, self.scale.weight)
                    time.sleep(interval)
                    
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()
        
    def quit(self):
        self._is_running = False
        
    def pause(self):
        self._pause_mutex.lock()
        self._paused = True
        self._pause_mutex.unlock()
    
    def resume(self):
        self._pause_mutex.lock()
        self._paused = False
        self._pause_condition.wakeAll()
        self._pause_mutex.unlock()
        # sleep to account for the delay in scale data collection
        time.sleep(2)
    
    def reset(self):
        self.time = 0
        
class GraphSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object, object)
import sys
from PyQt6.QtCore import QThread, pyqtSignal, QObject
import time
import traceback
import pandas as pd

class GraphThread(QThread):
    
    def __init__(self, scale, graph, precision = 2):
        super().__init__()
        self.signals = GraphSignal()
        self._is_running = True
        self.data = pd.DataFrame(columns=['Time', 'Weight'])
        self.scale = scale
        self.graph = graph
        self.precision = precision
        
    # X is time, Y is weight
    def run(self):
        try:
            # This specifies the interval of time between each data point
            interval = 10 ** -self.precision
            self.x = 0
            
            # While the thread is running, keep updating the graph with new data
            while self._is_running:
                self.x += interval
                self.x = round(self.x, self.precision)
                self.data.loc[self.x] = [self.x, self.scale.weight]
                self.signals.result.emit()
                time.sleep(interval)
                
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            if self._is_running:
                self.signals.finished.emit()
        
    def quit(self):
        self._is_running = False
        
class GraphSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal()
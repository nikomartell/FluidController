import sys
from PyQt6.QtCore import QThread, pyqtSignal, QObject
import time
import traceback
import pandas as pd

class GraphThread(QThread):
    
    def __init__(self, time, scale, graph):
        super().__init__()
        self.signals = GraphSignal()
        self._is_running = True
        self.x = time
        self.data = pd.DataFrame(columns=['Time', 'Weight'])
        self.scale = scale
        self.graph = graph
        
    # X is time, Y is weight
    def run(self):
        try:
            
            # While the thread is running, keep updating the graph with new data
            while self._is_running:
                self.x += .001
                self.data.loc[self.x] = [self.x, self.scale.get_weight()]
                self.signals.result.emit()
                time.sleep(.001)
                
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        
    def quit(self):
        self._is_running = False
        
class GraphSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal()
import sys
from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal, QObject
import time
import traceback
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class GraphThread(QThread):
    
    def __init__(self, x, scale, graph):
        super().__init__()
        self.signals = GraphSignal()
        self._is_running = True
        self.x = x
        self.scale = scale
        self.graph = graph
        
    # X is time, Y is weight
    def run(self):
        try:
            # Reset the graph by making new empty data lists
            x_data = []
            y_data = []
            
            # While the thread is running, keep updating the graph with new data
            while self._is_running:
                self.x += .001
                x_data.append(self.x)
                y_data.append(self.scale.weight)
                self.graph.set_data(x_data, y_data)
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
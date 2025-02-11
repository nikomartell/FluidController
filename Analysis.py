from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QTimer, Qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class analysis_widget(QWidget):
    def __init__(self):
        
        self.Container = QWidget()
        self.Container.setObjectName('Data Analysis')
        
        graph_layout = QVBoxLayout(self.Container)
        graph_layout.setContentsMargins(50, 50, 50, 50)
        
        self.graph_label = QLabel('Graph', self.Container)
        self.graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graph_layout.addWidget(self.graph_label)
        
        self.graph_widget = QWidget(self.Container)
        self.graph_layout = QVBoxLayout(self.graph_widget)
        
        self.canvas = plt.figure().add_subplot(111)
        self.canvas.plot(np.random.rand(10))
        
        self.graph_layout.addWidget(self.canvas.figure.canvas)
        graph_layout.addWidget(self.graph_widget)
        
        
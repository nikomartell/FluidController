import sys
from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal, QObject
import time
import traceback
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Analytics.GraphThread import GraphThread

class AnalysisCenter(QWidget):
    def __init__(self, controller):
        
        self.Container = QWidget()
        self.Container.setObjectName('AnalysisCenter')
        
        top_layout = QVBoxLayout(self.Container)
        top_layout.setContentsMargins(50, 50, 50, 50)
        
        self.graph_label = QLabel('Graph', self.Container)
        self.graph_label.setObjectName('title')
        self.graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.graph_label)
        
        self.graph_widget = QWidget(self.Container)
        self.graph_layout = QVBoxLayout(self.graph_widget)
        
        weight_layout = QVBoxLayout(self.Container)
        weightSettings = QLabel('Weight Monitor', self.Container)
        weightSettings.setObjectName('title')
        weight_layout.addWidget(weightSettings, alignment=Qt.AlignmentFlag.AlignTop)
        weight_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        weightLabel = QLabel('0.00', self.Container)
        weightLabel.setObjectName('weight')
        weight_layout.addWidget(weightLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        timer = QTimer(self.Container)
        timer.timeout.connect(lambda: weightLabel.setText(str(controller.scale.get_weight())))
        timer.start(100)
        
        tareScale = QPushButton('Tare Scale', self.Container)
        tareScale.setObjectName('tare')
        weight_layout.addWidget(tareScale, alignment=Qt.AlignmentFlag.AlignRight)
        
        top_layout.addWidget(self.graph_widget)
        top_layout.addLayout(weight_layout)
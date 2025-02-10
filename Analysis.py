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
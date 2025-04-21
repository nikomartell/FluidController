from PyQt6.QtCore import pyqtSignal, QObject, QThread
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
import time

class PrimeThread(QThread):
    pass
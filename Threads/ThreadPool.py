from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QThread
from Threads.GraphThread import GraphThread
from Threads.MotorThread import MotorThread
from Threads.ConnectionThread import ConnectionThread
from Threads.WeightThread import WeightThread
from Controller.Controller import Controller
import time

class ThreadPool(QtCore.QThreadPool):
    def __init__(self, controller = Controller()):
        super().__init__()
        self.setMaxThreadCount(10)
        self.threads = []
        self.motor_thread = MotorThread()
        self.graph_thread = GraphThread()
        self.connection_thread = ConnectionThread()
        self.weight_thread = WeightThread()
        self.controller = controller
        
    # Take a Runnable object, move it to a thread, store it in Threads list
    def start(self, runnable):
        thread = QtCore.QThread()
        if isinstance(runnable, QObject):
            runnable.moveToThread(thread)
        else:
            raise TypeError("Runnable must inherit from QObject to use moveToThread.")
        thread.started.connect(runnable.run)
        thread.start()
        self.threads.append(thread)

    # Stop all threads
    def stop(self):
        for thread in self.threads:
            thread.quit()
            thread.wait()
        self.threads.clear()
    
    # Start the connection thread
    def start_connection(self):
        self.connection_thread.signals.finished.connect(self.stop)
        self.connection_thread.signals.error.connect(lambda e: QMessageBox.critical(None, 'Error', f'Error: {e}'))
        self.start(self.connection_thread)
    
    # Start the motor thread
    def start_motor(self, command_set):
        self.motor_thread.controller = self.controller
        self.motor_thread.command_set = command_set
        self.graph_thread.scale = self.controller.scale
        self.motor_thread.signals.finished.connect(self.stop)
        self.motor_thread.signals.error.connect(lambda e: QMessageBox.critical(None, 'Error', f'Error: {e}'))
        self.motor_thread.signals.start.connect(lambda: self.start(self.graph_thread))
        self.start(self.motor_thread)
        
    
    
    
    # Set the precision of the threads
    def set_precision(self, precision):
        self.weight_thread.precision = precision
        self.graph_thread.precision = precision

class ThreadPoolSignal(QObject):
    started = pyqtSignal()
    data = pyqtSignal(object)

    
    
    
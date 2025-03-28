from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QThread, QThreadPool
from Threads.GraphThread import GraphThread
from Threads.MotorThread import MotorThread
from Threads.ConnectionThread import ConnectionThread
from Threads.WeightThread import WeightThread
from Controller.Controller import Controller
import time

class ThreadPool(QThreadPool):
    def __init__(self, controller):
        super().__init__()
        self.setMaxThreadCount(10)
        self.signals = ThreadPoolSignal()
        self.controller = controller
        
        
        # Initialize Threads
        self.motor_thread = MotorThread(self.controller)
        self.graph_thread = GraphThread(self.controller.scale)
        self.weight_thread = WeightThread(self.controller.scale)
        self.connection_thread = ConnectionThread(self.controller)
        
        
    # Take a Runnable object, move it to a thread, store it in Threads list if not already started
    def start(self, runnable):
        runnable.run()

    # Stop all threads
    def stop(self):
        self.motor_thread.quit()
        self.graph_thread.quit()
        self.weight_thread.quit()
        self.connection_thread.quit()
    
    # Start the connection thread
    def start_connection(self):
        # Set signal connections
        self.connection_thread = ConnectionThread(self.controller)
        self.connection_thread.signals.error.connect(lambda e: QMessageBox.critical(None, 'Error', f'Error: {e}'))
        self.connection_thread.signals.result.connect(lambda con: self.set_controller(con))
        self.connection_thread.start()
    
    # Start the motor thread
    def start_process(self, command_set):
        
        # Set the controller and command set for the motor thread
        self.motor_thread.command_set = command_set
        
        # Set graph thread signal connections
        self.graph_thread = GraphThread(self.controller.scale)
        self.graph_thread.signals.result.connect(lambda t, w: self.signals.log.emit(t, w))
        
        # Set motor thread signal connections
        self.motor_thread.signals.execute.connect(lambda: self.graph_thread.start())
        self.motor_thread.signals.finished.connect(self.signals.finished.emit)
        self.motor_thread.signals.finished.connect(lambda: self.graph_thread.quit())
        self.motor_thread.signals.error.connect(lambda e: QMessageBox.critical(None, 'Error', f'Error: {e}'))
        
        self.motor_thread.start()
        
    
    # Set the precision of the threads
    def set_precision(self, precision):
        self.weight_thread.precision = precision
        self.graph_thread.precision = precision
    
    # When connection is established, set the controller for the motor thread and the scale for the weight thread
    def set_controller(self, controller):
        self.controller = controller
        self.motor_thread.controller = self.controller
        
        if self.controller.scale.device is not None:
            self.weight_thread = WeightThread(self.controller.scale)
            self.weight_thread.signals.result.connect(lambda weight: self.signals.data.emit(weight))
            self.weight_thread.start()


class ThreadPoolSignal(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    log = pyqtSignal(object, object)
    data = pyqtSignal(object)

    
    
    
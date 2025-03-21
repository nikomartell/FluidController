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
    def __init__(self):
        super().__init__()
        self.setMaxThreadCount(10)
        self.threads = []
        self.signals = ThreadPoolSignal()
        
        # Initialize Threads
        self.motor_thread = MotorThread()
        self.graph_thread = GraphThread()
        self.connection_thread = ConnectionThread()
        self.weight_thread = WeightThread()
        self.thread_motor = QThread()
        self.thread_graph = QThread()
        self.motor_thread.moveToThread(self.thread_motor)
        self.graph_thread.moveToThread(self.thread_graph)
        
        
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
        # Set signal connections
        self.connection_thread.signals.error.connect(lambda e: QMessageBox.critical(None, 'Error', f'Error: {e}'))
        self.connection_thread.signals.result.connect(lambda con: self.found_controller(con))
        self.connection_thread.start()
    
    # Start the motor thread
    def start_process(self, command_set):
        # Set the controller and command set for the motor thread
        self.motor_thread.command_set = command_set
        
        # Set the scale for the graph thread and emitting it's data
        self.graph_thread.signals.result.connect(lambda data: self.signals.log.emit(data))
        
        # Set signal connections
        #self.motor_thread.signals.start.connect(lambda: self.start(self.graph_thread))
        self.motor_thread.signals.finished.connect(self.signals.finished.emit)
        self.motor_thread.signals.error.connect(lambda e: QMessageBox.critical(None, 'Error', f'Error: {e}'))
        
        self.thread_motor.start()
        
    
    # Set the precision of the threads
    def set_precision(self, precision):
        self.weight_thread.precision = precision
        self.graph_thread.precision = precision
    
    # When connection is established, set the controller for the motor thread and the scale for the weight thread
    def found_controller(self, controller):
        self.weight_thread = WeightThread()
        self.controller = controller
        self.motor_thread.controller = self.controller
        self.weight_thread.scale = self.controller.scale
        if self.controller.scale.device:
            self.weight_thread.signals.result.connect(lambda weight: self.signals.data.emit(weight))
            self.weight_thread.start()

class ThreadPoolSignal(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    log = pyqtSignal(object)
    data = pyqtSignal(object)

    
    
    
import sys
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('QtAgg')
import numpy as np
import serial
from Controller.Controller import Controller
from ControlCenter import controlCenter
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QAction
from CommandSet import CommandSet
from Controller.ConnectionThread import ConnectionThread
from Controller.MotorThread import MotorThread
from Analytics.Analysis import AnalysisCenter
from Analytics.GraphThread import GraphThread
import csv

class MainSignals(QObject):
    def __init__(self):
        super().__init__()
        self.isClosing = False

class App(QWidget):
    def __init__(self):        
        super().__init__()
        self.mainSignals = MainSignals()
        self.threadpool = QThreadPool()
        self.connections = ConnectionThread()
        self.connections.start()
        self.device = self.connections.con
        self.fig, self.ax = plt.subplots()
        self.graph, = self.ax.plot(np.arange(100), np.arange(100))
        self.initUI()
        
    
    def initUI(self):
        
        # Stylesheet
        with open("main.css", "r") as file:
            self.setStyleSheet(file.read())
        
        # Setup
        self.setWindowTitle('Fluidics Device Controller')
        self.layout = QVBoxLayout()
        # Multithreading
        
        self.draw_errorLayout()
        self.layout.addLayout(self.errorLayout)
        #---------------------------------------------------------#

        # Window Action Items
        menubar = QMenuBar(self)
        
        #File Menu
        file_menu = menubar.addMenu('File')
        export_action = QAction('Save Config', self)
        export_action.triggered.connect(self.store_commands_to_csv)
        import_action = QAction('Import Config', self)
        import_action.triggered.connect(self.import_commands_from_csv)
        file_menu.addAction(export_action)
        file_menu.addAction(import_action)
        
        
        #Settings Menu
        settings_menu = menubar.addMenu('Settings')
        motor_settings_action = QAction('Change Motor Settings', self)
        scale_settings_action = QAction('Change Scale Settings', self)
        settings_menu.addAction(motor_settings_action)
        settings_menu.addAction(scale_settings_action)
        
        #Tools Menu
        tools_menu = menubar.addMenu('Tools')
        tools_action = QAction('Change Analysis', self)
        tools_menu.addAction(tools_action)
        
        #Help Menu
        help_menu = menubar.addMenu('Help')
        self.layout.setMenuBar(menubar)
        help_action = QAction('Manual', self)
        help_menu.addAction(help_action)
        #---------------------------------------------------------#
        
        # Device Control Center
        self.control_layout = QHBoxLayout()
        self.deviceControl = controlCenter(self.device)
        self.control_layout.addWidget(self.deviceControl.Container)
        
        # System Control (change this button to refresh device connection)
        button_layout = QHBoxLayout()

        self.motor_task = MotorThread(self.device, self.deviceControl.get_commands())
        
        self.execute_button = QPushButton('Execute', self)
        self.execute_button.setToolTip('Execute Commands')
        self.execute_button.setText('Execute')
        self.execute_button.clicked.connect(self.execute)
        self.draw_execute_button()        
        button_layout.addWidget(self.execute_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        plt.ion()
        
        self.graph_thread = GraphThread(0, 0, graph = self.graph)
        self.graph_thread.start()
        
        self.analysis_layout = QVBoxLayout()
        self.analysis_widget = self.graph
        
        self.analysis_layout.addWidget(self.fig.canvas, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.layout.addLayout(self.control_layout)
        self.control_layout.addLayout(self.analysis_layout)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)
    
    
    #---------------------------------------------------------#
    
    # Methods ---------- #
    
    def execute(self):
        if self.device is None:
            QMessageBox.critical(self, 'Error', 'Controller not found')
            return
        commands = self.deviceControl.get_commands()
        self.motor_task = MotorThread(self.device, commands)
        self.graph_thread = GraphThread(self.device, self.analysis_widget.canvas)
        self.motor_task.signals.finished.connect(self.draw_execute_button, self.graph_thread.quit)
        self.motor_task.start()
        self.graph_thread.start()
        self.draw_execute_button()
    
    # Update Layouts ----------- #
    
    def draw_errorLayout(self):
        self.errorLayout = QHBoxLayout()
        self.errorLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        if self.device is not None:
            self.pump_info_label = QLabel(f'Component Status:', self)
            self.pump_info_label.setStyleSheet('color: green; font-weight: bold;')
            self.pump_info_label.setObjectName('device_info')
            self.errorLayout.addWidget(self.pump_info_label, alignment=Qt.AlignmentFlag.AlignTop)
            for error in self.device.errors:
                if error is not None:
                    self.error_label = QLabel(error, self)
                    self.error_label.setStyleSheet('color: red; font-weight: bold;')
                    self.error_label.setObjectName('device_info')
                    self.errorLayout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignTop)
            
        if not self.device:
            error_label = QLabel('Controller not found', self)
            error_label.setStyleSheet('color: red; font-weight: bold;')
            error_label.setObjectName('device_info')
            self.errorLayout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignTop)
    
    def draw_execute_button(self):
        if self.device.module is None:
            self.execute_button.setEnabled(False)
            self.execute_button.setStyleSheet('background-color: red;')
            self.execute_button.setToolTip('Controller not found')
            self.execute_button.setText('Controller not found')
            
        elif not self.motor_task._is_running and self.device.module:
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: #0B41CD;')
            self.execute_button.setToolTip('Execute Commands')
            self.execute_button.setText('Execute')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.execute)
        
        elif self.motor_task._is_running:
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: red;')
            self.execute_button.setToolTip('STOP MOTOR')
            self.execute_button.setText('STOP MOTOR')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.motor_task.quit)
        
        
    # Files and Settings ----------- #
    
    def store_commands_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Commands to CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            commands = self.deviceControl.get_commands()
            with open(file_name, 'w', newline='') as csvfile:
                command_writer = csv.writer(csvfile)
                for command in commands:
                    command_writer.writerow([command])
            QMessageBox.information(self, 'Success', f'Commands saved to {file_name}')

    def import_commands_from_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Commands from CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as csvfile:
                command_reader = csv.reader(csvfile)
                commands = [row[0] for row in command_reader if row]
                self.deviceControl.set_commands(commands)
            QMessageBox.information(self, 'Success', f'Commands imported from {file_name}')

    #---------------------------------------------------------#

if __name__ == '__main__':
    def close_threads():
        ex.mainSignals.isClosing = True
        ex.connections.quit()
        ex.motor_task.quit()
        ex.graph_thread.quit()
        ex.threadpool.waitForDone()
        ex.threadpool.clear()
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(close_threads)
    ex = App()
    ex.show()
    sys.exit(app.exec())
    

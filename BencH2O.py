import sys
import time
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
from Analytics.WeightThread import WeightThread
import csv

class App(QWidget):
    def __init__(self):        
        super().__init__()
        self.connections = ConnectionThread()
        self.connections.start()
        self.device = self.connections.con
        
        self.fig, self.ax = plt.subplots()
        self.graph, = self.ax.plot(np.arange(10), np.arange(10))
        plt.ion()
        
        self.initUI()
        
    
    def initUI(self):
        
        # Stylesheet
        with open("main.css", "r") as file:
            self.setStyleSheet(file.read())
        
        # Setup
        self.setWindowTitle('Fluidics Device Controller')
        self.layout = QVBoxLayout()
        
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
        self.deviceControl = controlCenter()
        self.control_layout.addWidget(self.deviceControl.Container, alignment=Qt.AlignmentFlag.AlignTop)
        
        # System Control (change this button to refresh device connection)
        button_layout = QHBoxLayout()

        self.motor_task = MotorThread(self.device, self.deviceControl.get_commands())
        self.graph_thread = GraphThread(0, self.device.scale, graph = self.graph)
        
        
        if self.device.scale.device is not None:
            self.graph_thread.start()
        
        self.execute_button = QPushButton('Execute', self)
        self.execute_button.setToolTip('Execute Commands')
        self.execute_button.setText('Execute')
        self.execute_button.clicked.connect(self.execute)
        self.draw_execute_button()        
        button_layout.addWidget(self.execute_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Analysis Center
        
        self.analysis_layout = QVBoxLayout()
        self.analysisCenter = AnalysisCenter(self.device)
        self.graph_widget = QWidget(self.analysisCenter.Container)
        self.analysisCenter.graph_layout.addWidget(self.fig.canvas, alignment=Qt.AlignmentFlag.AlignRight)
        self.analysis_layout.addWidget(self.analysisCenter.Container)
        
        self.weight_thread = WeightThread(self.device.scale)
        self.weight_thread.start()
        self.analysisCenter.tareScale.clicked.connect(self.tare)
        self.weight_thread.signals.result.connect(lambda weight: self.analysisCenter.weightLabel.setText(weight))
        
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
        self.motor_task.signals.finished.connect(self.draw_execute_button, self.graph_thread.quit)
        if self.graph_thread._is_running:
            self.graph_thread.quit()
        self.graph_thread = GraphThread(0, self.device.scale, graph = self.graph)
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
        
        elif self.motor_task._is_running == True:
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: red;')
            self.execute_button.setToolTip('STOP MOTOR')
            self.execute_button.setText('STOP MOTOR')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.motor_task.quit)    
        
        elif (self.device.module is not None) and (self.motor_task._is_running == False):
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: #0B41CD;')
            self.execute_button.setToolTip('Execute Commands')
            self.execute_button.setText('Execute')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.execute)
        
    def tare(self):
        if self.weight_thread._is_running:
            self.weight_thread.quit()
        if self.graph_thread._is_running:
            self.graph_thread.quit()
        self.weight_thread = WeightThread(self.device.scale)
        self.graph_thread = GraphThread(0, self.device.scale, graph = self.graph)
        self.weight_thread.signals.result.connect(lambda weight: self.analysisCenter.weightLabel.setText(weight))
        self.device.scale.weight = 0.00
        self.weight_thread.start()
        self.graph_thread.start()
    
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
        ex.connections.quit()
        ex.motor_task.quit()
        ex.graph_thread.quit()
        ex.weight_thread.quit()
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(close_threads)
    ex = App()
    ex.show()
    sys.exit(app.exec())
    

import sys
from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
matplotlib.use('QtAgg')
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QAction
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
from Controller.ConnectionThread import ConnectionThread
from Controller.MotorThread import MotorThread
from Analytics.GraphThread import GraphThread
from Analytics.WeightThread import WeightThread
from Interface.Style import apply_style
from Interface.Analysis import AnalysisCenter
from Interface.ControlCenter import controlCenter
import csv
import os

class App(QWidget):
    def __init__(self):        
        super().__init__()
        
        # Device Connection
        self.connections = ConnectionThread()
        self.connections.start()
        self.device = self.connections.con
        
        # Data Collected
        self.data = pd.DataFrame(columns=['Time', 'Weight'])
        self.threadpool = QThreadPool()
        
        # Graph Setup
        self.fig, self.ax = plt.subplots()
        self.graph, = self.ax.plot(self.data['Time'], self.data['Weight'])
        self.ax.autoscale(enable=True, axis='both')
        self.initUI()
        
        
    
    def initUI(self):
        
        # Stylesheet
        apply_style(self)
        
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
        export_data_action = QAction('Export Data', self)
        export_data_action.triggered.connect(self.export_data_to_csv)
        file_menu.addAction(export_action)
        file_menu.addAction(import_action)
        file_menu.addAction(export_data_action)
        
        
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

        # These are the threads for each of the components.
        # Communication with components should be done through threads to prevent UI freezing.
        self.graph_thread = GraphThread(self.device.scale, graph = self.graph)
        self.weight_thread = WeightThread(scale = self.device.scale)
        self.motor_thread = MotorThread(controller = self.device, command_set = self.get_commands())
        self.graph_thread.signals.result.connect(self.update_graph)
        
        
        self.data = self.graph_thread.data # Data is updated in the graph thread    
        plt.ion()
        
        # Analysis Center
        self.analysis_layout = QVBoxLayout()
        self.analysisCenter = AnalysisCenter()
        self.graph_widget = QWidget(self.analysisCenter.Container)
        self.analysisCenter.graph_layout.addWidget(self.fig.canvas, alignment=Qt.AlignmentFlag.AlignRight)
        self.analysis_layout.addWidget(self.analysisCenter.Container)
        self.analysisCenter.tareScale.clicked.connect(self.tare)
        if self.device.scale.device is None:
            self.analysisCenter.weightLabel.setText('Scale not found')
            self.analysisCenter.tareScale.setEnabled(False)
        else:
            self.weight_thread.start()
            self.analysisCenter.tareScale.setEnabled(True)
        self.weight_thread.signals.result.connect(lambda weight: self.analysisCenter.weightLabel.setText(weight))
        
        self.execute_button = QPushButton('Execute', self)
        self.execute_button.setToolTip('Execute Commands')
        self.execute_button.setText('Execute')
        self.execute_button.clicked.connect(self.motor_thread.start)
        self.draw_execute_button()        
        button_layout.addWidget(self.execute_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.layout.addLayout(self.control_layout)
        self.control_layout.addLayout(self.analysis_layout)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)

        # Connection Signals
        # UI Elements are updated based on the connection status of the device
        self.connections.signals.connected.connect(self.draw_errorLayout)
        self.connections.signals.connected.connect(self.draw_execute_button)
        self.connections.signals.connected.connect(self.draw_analysis)
        
        self.motor_thread.signals.running.connect(self.draw_execute_button)
        self.motor_thread.signals.start.connect(self.graph_thread.start)
        self.motor_thread.signals.finished.connect(self.draw_execute_button)
        self.motor_thread.signals.finished.connect(self.graph_thread.quit)
        # Testing Area. Commment out contents before use #
        # self.graph_thread.start()
    
    #---------------------------------------------------------#
    
    # Methods ---------- #
    
    def get_commands(self):
        return self.deviceControl.get_commands()
        
    
    def tare(self):
        self.weight_thread.tare()
    
    # Update Layouts ----------- #
    
    def draw_errorLayout(self):
        self.errorLayout = QHBoxLayout()
        self.errorLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for error in self.device.errors:
            if error is not None:
                self.error_label = QLabel(error, self)
                self.error_label.setStyleSheet('color: red; font-weight: bold;')
                self.error_label.setObjectName('device_info')
                self.errorLayout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignTop)
    
    
    # Update Analysis Center based on connection status ----------- #
    def draw_analysis(self):
        if self.device.scale.device is None:
            self.analysisCenter.weightLabel.setText('Scale not found')
            self.analysisCenter.tareScale.setEnabled(False)
        else:
            self.weight_thread.start()
            self.analysisCenter.tareScale.setEnabled(True)
    
    
    # Update Execute Button based on connection and current state ----------- #
    def draw_execute_button(self):
        if self.device.module is None:
            self.execute_button.setEnabled(False)
            self.execute_button.setStyleSheet('background-color: red;')
            self.execute_button.setToolTip('Controller not found')
            self.execute_button.setText('Controller not found')
        
        elif self.motor_thread._is_running == True:
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: red;')
            self.execute_button.setToolTip('STOP MOTOR')
            self.execute_button.setText('STOP MOTOR')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.motor_thread.quit)    
        
        elif (self.device.module is not None) and (self.motor_thread._is_running == False):
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: #0B41CD;')
            self.execute_button.setToolTip('Execute Commands')
            self.execute_button.setText('Execute')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.motor_thread.start)
    
    
    # Update Graph ----------- #
    def update_graph(self):
        x = self.data['Time']
        y = self.data['Weight']
        self.graph.set_data(x, y)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw_idle()
    
    #---------------------------------------------------------#
    
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
            
    def export_data_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data to CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            self.data.to_csv(file_name)
            QMessageBox.information(self, 'Success', f'Data saved to {file_name}')
    
    def failsafe_data_csv(self):
        try:
            filepath = os.path.join(os.getcwd(), 'data.csv')
            self.data.to_csv(filepath)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error saving data: {e}')

    #---------------------------------------------------------#

if __name__ == '__main__':
    def close_threads():
        ex.graph_thread.quit()
        ex.weight_thread.quit()
        ex.motor_thread.quit()
        ex.connections.quit()
        ex.failsafe_data_csv()
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(close_threads)
    ex = App()
    ex.show()
    sys.exit(app.exec())
    

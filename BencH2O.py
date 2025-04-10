import sys
from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
matplotlib.use('QtAgg')
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTabWidget, QFileDialog, QMessageBox, QMenuBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from pytrinamic.connections import ConnectionManager
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
from Threads.ThreadPool import ThreadPool
from Interface.Style import apply_style
from Interface.AnalysisCenter import AnalysisCenter
from Interface.ControlCenter import ControlCenter
from Interface.CalibrationMenu import CalibrationMenu
import csv
import os

class App(QWidget):
    def __init__(self):        
        super().__init__()
        
        # Device Connection
        try:
            interface = ConnectionManager().connect()
        except Exception as e:
            interface = None
            print(f'Error: {e}')

        self.device = Controller(interface)
        self.threadpool = ThreadPool(self.device)
        
        # Data Collected
        self.data = pd.DataFrame(columns=['Time', 'Weight'])
        
        # Graph Setup
        self.fig, self.ax = plt.subplots()
        self.graph, = self.ax.plot(self.data['Time'], self.data['Weight'])
        self.graph.set_data(self.data['Time'], self.data['Weight'])
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
        calibrate_action = QAction('Calibrate Rotary Motor', self)
        calibrate_action.triggered.connect(self.open_rotary_calibration)
        tools_menu.addAction(calibrate_action)
        
        #Help Menu
        help_menu = menubar.addMenu('Help')
        self.layout.setMenuBar(menubar)
        help_action = QAction('Manual', self)
        help_menu.addAction(help_action)
        
        #---------------------------------------------------------#
        
        # Device Control Center
        self.control_layout = QHBoxLayout()
        self.deviceControl = ControlCenter()
        self.control_layout.addWidget(self.deviceControl.Container, alignment=Qt.AlignmentFlag.AlignTop)
        # Add a tab widget to hold multiple control centers
        self.control_tabs = QTabWidget()
        
        # Add the initial control center tab
        self.control_tabs.addTab(self.deviceControl.Container, "1")
        
        # Button to add a new control center
        self.add_tab_button = QPushButton("Add Control Center", self)
        self.add_tab_button.setToolTip("Add a new control center tab")
        self.add_tab_button.clicked.connect(self.add_control_center_tab)
        self.control_layout.addWidget(self.add_tab_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.control_layout.addWidget(self.control_tabs)
        self.control_sets = []

        # System Control (change this button to refresh device connection)
        button_layout = QHBoxLayout()
        
        # Analysis Center
        self.analysis_layout = QVBoxLayout()
        self.analysisCenter = AnalysisCenter()
        self.graph_widget = QWidget(self.analysisCenter.Container)
        self.analysisCenter.graph_layout.addWidget(self.fig.canvas, alignment=Qt.AlignmentFlag.AlignRight)
        self.analysis_layout.addWidget(self.analysisCenter.Container)
        self.analysisCenter.tareScale.clicked.connect(self.tare)
        
        
        self.statusText = QLabel('Standby')
        self.statusText.setObjectName('title')
        button_layout.addWidget(self.statusText, alignment=Qt.AlignmentFlag.AlignRight)
        
        
        self.execute_button = QPushButton('Execute', self)
        self.execute_button.setToolTip('Execute Commands')
        self.execute_button.setText('Execute')
        self.execute_button.clicked.connect(self.execute)
        self.draw_execute_button()
        button_layout.addWidget(self.execute_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        
        # Add Layouts to Main Layout
        self.layout.addLayout(self.control_layout)
        self.control_layout.addLayout(self.analysis_layout)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)

        # Connection Signals
        # UI Elements are updated based on the connection status of the device
        self.threadpool.motor_thread.signals.start.connect(self.draw_execute_button)
        self.threadpool.signals.started.connect(self.reset_graph)
        self.threadpool.motor_thread.signals.finished.connect(self.draw_execute_button)
        
        self.threadpool.motor_thread.signals.finished.connect(lambda: self.statusText.setText('Standby'))
        self.threadpool.motor_thread.signals.toZero.connect(lambda: self.statusText.setText('Moving Motor to Zero'))
        self.threadpool.motor_thread.signals.execute.connect(lambda: self.statusText.setText('Executing Commands'))
        
        self.threadpool.signals.data.connect(lambda weight: self.analysisCenter.weightLabel.setText(weight))
        
        self.threadpool.signals.log.connect(lambda t, w: self.update_graph(t, w))
        
        self.threadpool.connection_thread.signals.connected.connect(self.connected)
        self.threadpool.start_connection()
        
        self.flow_rate = self.calculate_flow_rate()
        self.threadpool.signals.data.connect(lambda: self.analysisCenter.flowRateLabel.setText(str(self.calculate_flow_rate())))
        
        
        # Testing Area. Commment out contents before use #
        # self.graph_thread.start()
    
    #---------------------------------------------------------#
    
    # Methods ---------- #
    
    def get_commands(self):
        commands = []
        for control_center in self.control_sets:
            # Get the command set from each control center
            command_set = control_center.get_commands()
            commands.append(command_set)
            print('Commands:', command_set)
        return commands
     
    
    def tare(self):
        self.threadpool.weight_thread.tare()
    
    # Update Layouts ----------- #
    
    def draw_errorLayout(self):
        self.errorLayout = QHBoxLayout()
        self.errorLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        rotary_error = QLabel(self.device.errors[0])
        linear_error = QLabel(self.device.errors[1])
        scale_error = QLabel(self.device.errors[2])
        rotary_error.setObjectName('error')
        linear_error.setObjectName('error')
        scale_error.setObjectName('error')
        self.errorLayout.addWidget(rotary_error)
        self.errorLayout.addWidget(linear_error)
        self.errorLayout.addWidget(scale_error)
    
    def add_control_center_tab(self, commands=None):
        # Create a new control center and add it as a new tab
        new_control_center = ControlCenter()
        self.control_tabs.addTab(new_control_center.Container, f"{self.control_tabs.count() + 1}")
        self.control_sets.append(new_control_center)
        if commands is not None:
            new_control_center.set_commands(commands)
    
    # Update Analysis Center based on connection status ----------- #
    def draw_analysis(self):
        if self.device.scale.device is None:
            #self.analysisCenter.weightLabel.setText('Scale not found')
            self.analysisCenter.tareScale.setEnabled(False)
        else:
            self.analysisCenter.tareScale.setEnabled(True)
    
    
    # Update Execute Button based on connection and current state ----------- #
    def draw_execute_button(self):
        # If the device is not connected, disable the execute button
        if self.device.module is None:
            self.execute_button.setEnabled(False)
            self.execute_button.setStyleSheet('background-color: red;')
            self.execute_button.setToolTip('Controller not found')
            self.execute_button.setText('Controller not found')
        
        # If the motor is running, disable the execute button
        elif self.threadpool.motor_thread._is_running == True:
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: red;')
            self.execute_button.setToolTip('STOP MOTOR')
            self.execute_button.setText('STOP MOTOR')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.threadpool.stop)    
        
        # If the motor is not running, enable the execute button
        elif (self.device.module is not None) and (self.threadpool.motor_thread._is_running == False):
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: #0B41CD;')
            self.execute_button.setToolTip('Execute Commands')
            self.execute_button.setText('Execute')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.execute)
    
    # Open Rotary Motor Calibration Window ----------- #
    def open_rotary_calibration(self):
        if self.device.errors[0] is not None:
            QMessageBox.critical(self, "Error", "Rotary motor not found!")
            return

        self.rotary_calibration = CalibrationMenu(self)
        self.rotary_calibration.show()
    
    # Execute Commands ----------- #
    def execute(self):
        print('Executing commands...')
        command_set = self.get_commands()
        self.threadpool.start_process(command_set)
    
    # Update UI based on connection status ----------- #
    def connected(self):
        self.draw_errorLayout()
        self.draw_execute_button()
        self.draw_analysis()
    
    # Update Graph ----------- #
    def update_graph(self, time, weight):
        # Add data to the dataframe
        self.data = pd.concat([self.data, pd.DataFrame({'Time': [time], 'Weight': [weight]})])
        
        # Update the graph
        x = self.data['Time']
        y = self.data['Weight']
        self.graph.set_data(x, y)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw_idle()
        
    def reset_graph(self):
        self.data = pd.DataFrame(columns=['Time', 'Weight'])
        x = self.data['Time']
        y = self.data['Weight']
        self.graph.set_data(x, y)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw_idle()
    
    def calculate_flow_rate(self):
        # Calculate the flow rate based on the data collected
        if len(self.data) > 1:
            time_diff = self.data['Time'].diff().iloc[1:]
            weight_diff = self.data['Weight'].diff().iloc[1:]
            flow_rate = weight_diff / time_diff
            self.flow_rate = round(flow_rate.mean(), 3)
            return self.flow_rate
        return 0.0
    
    #---------------------------------------------------------#
    
    # File Menu Actions
    
    # Export commands to CSV
    def store_commands_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Commands to CSV", "datasheet", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Component', 'Speed', 'Strokes', 'Acceleration', 'Flow Direction', 'Duration', 'Iterations'])
                control_sets = self.get_commands()
                for commands in control_sets:
                    writer.writerow(commands.array())
            QMessageBox.information(self, 'Success', f'Commands saved to {file_name}')

    # Import commands from CSV
    def import_commands_from_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Commands from CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as csvfile:
                command_reader = csv.reader(csvfile)
                commands = [row[1] for row in command_reader if row]
                self.deviceControl.set_commands(commands)
            QMessageBox.information(self, 'Success', f'Commands imported from {file_name}')
           
    # Export data to CSV 
    def export_data_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data to CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            self.data.to_csv(file_name)
            QMessageBox.information(self, 'Success', f'Data saved to {file_name}')
    
    # On close, save data to CSV
    def failsafe_data_csv(self):
        try:
            filepath = os.path.join(os.getcwd(), 'data.csv')
            self.data.to_csv(filepath)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error saving data: {e}')

    #---------------------------------------------------------#

if __name__ == '__main__':
    def close_threads():
        ex.threadpool.stop()
        ex.failsafe_data_csv()
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(close_threads)
    ex = App()
    ex.show()
    sys.exit(app.exec())
    

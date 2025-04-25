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
from PyQt6.QtGui import QIcon

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
        self.control_sets = []
        
        # Graph Setup
        self.fig, self.ax = plt.subplots()
        plt.tight_layout(pad=5)
        self.graph, = self.ax.plot(self.data['Time'], self.data['Weight'])
        self.graph.set_data(self.data['Time'], self.data['Weight'])
        self.ax.autoscale(enable=True, axis='both')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Weight (g)')
        self.ax.set_title('Weight vs Time')
        
        self.setWindowIcon(QIcon('interface/logo.png'))
        
        self.initUI()
            
    
    def initUI(self):
        
        # Stylesheet
        apply_style(self)
        
        # Setup
        self.setWindowTitle('BencH2O Fluidics Delivery')
        self.layout = QVBoxLayout()
        
        self.drawErrorLayout()
        self.layout.addLayout(self.errorLayout)
        
        #---------------------------------------------------------#

        self.makeMenuBar()
        
        #---------------------------------------------------------#
        
        # Device Control Center
        self.control_layout = QHBoxLayout()
        # Add a tab widget to hold multiple control centers
        self.control_tabs = QTabWidget()
        
        # Add the initial control center tab
        self.control_tabs.setObjectName('tab_bar')
        self.addControlCenterTab()
        
        # Button to add a new control center
        add_tab_button = QPushButton("Add Control Center", self)
        add_tab_button.setToolTip("Add a new control center tab")
        add_tab_button.clicked.connect(self.addControlCenterTab)
        
        # Button to remove the last control center
        remove_tab_button = QPushButton("Remove Control Center", self)
        remove_tab_button.setToolTip("Remove the last control center tab")
        remove_tab_button.clicked.connect(self.removeControlCenterTab)
        
        control_buttons = QVBoxLayout()
        control_buttons.addWidget(add_tab_button)
        control_buttons.addWidget(remove_tab_button)
        control_buttons.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.control_layout.addLayout(control_buttons)

        self.control_layout.addWidget(self.control_tabs)
        
        # Analysis Center --------------------------# 
        self.analysis_layout = QVBoxLayout()
        self.analysis_center = AnalysisCenter()
        self.graph_widget = QWidget(self.analysis_center.Container)
        self.analysis_center.graph_layout.addWidget(self.fig.canvas, alignment=Qt.AlignmentFlag.AlignTop)
        self.analysis_layout.addWidget(self.analysis_center.Container)
        self.analysis_center.tareScale.clicked.connect(self.tare)
        
        button_layout = QHBoxLayout()
        
        # Prime button for allowing user to manually prime system
        prime_button = QPushButton('Prime Tubing')
        prime_button.setToolTip('Run rotary motor until fluid reaches the end of the tubing')
        button_layout.addWidget(prime_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.statusText = QLabel('Standby')
        self.statusText.setObjectName('title')
        button_layout.addWidget(self.statusText, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.execute_button = QPushButton('Execute', self)
        self.execute_button.setToolTip('Execute Commands')
        self.execute_button.setText('Execute')
        self.execute_button.clicked.connect(self.execute)
        self.drawExecuteButton()
        button_layout.addWidget(self.execute_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        
        # Add Layouts to Main Layout ------------------#
        self.layout.addLayout(self.control_layout)
        self.control_layout.addLayout(self.analysis_layout)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)

        # Connection Signals
        self.setConnections()
        self.threadpool.start_connection()
        
        # Testing Area. Commment out contents before use #
        # self.graph_thread.start()
    
    #---------------------------------------------------------#
    
    # Methods ---------- #
    
    def getCommands(self):
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
    
    def makeMenuBar(self):
        # Window Action Items
        menubar = QMenuBar(self)
        
        #File Menu
        file_menu = menubar.addMenu('File')
        export_action = QAction('Save Config', self)
        export_action.triggered.connect(self.storeCommandsToCSV)
        import_action = QAction('Import Config', self)
        import_action.triggered.connect(self.importCommandsFromCSV)
        export_data_action = QAction('Export Data', self)
        export_data_action.triggered.connect(self.exportDataToCSV)
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
        calibrate_action.triggered.connect(self.openRotaryCalibration)
        tools_menu.addAction(calibrate_action)
        
        #Help Menu
        help_menu = menubar.addMenu('Help')
        help_action = QAction('Manual', self)
        help_menu.addAction(help_action)
        
        reset_ui_action = QAction('Reset UI', self)
        reset_ui_action.triggered.connect(self.resetUI)
        help_menu.addAction(reset_ui_action)
        
        self.layout.setMenuBar(menubar)
    
    def drawErrorLayout(self):
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
    
    def addControlCenterTab(self, commands=None):
        # Create a new control center and add it as a new tab
        new_control_center = ControlCenter()
        self.control_tabs.addTab(new_control_center.Container, f"{self.control_tabs.count() + 1}")
        self.control_sets.append(new_control_center)
        if commands is not None:
            new_control_center.set_commands(commands)
            
    def removeControlCenterTab(self):
        # Remove the current control center tab
        if self.control_tabs.count() > 1:
            self.control_tabs.removeTab(self.control_tabs.currentIndex())
            # Remove the corresponding control center from the list
            self.control_sets.pop()
            for i in range(self.control_tabs.count()):
                self.control_tabs.setTabText(i, str(i + 1))
        else:
            QMessageBox.warning(self, "Warning", "Cannot remove the last control center tab.")
            
    def setConnections(self):
         # UI Elements are updated based on the connection status of the device
        self.threadpool.motor_thread.signals.start.connect(self.drawExecuteButton)
        self.threadpool.motor_thread.signals.finished.connect(self.drawExecuteButton)
        
        self.threadpool.signals.started.connect(self.resetGraph)
        self.threadpool.signals.log.connect(lambda t, w: self.updateGraph(t, w))
        self.threadpool.signals.data.connect(lambda weight: self.analysis_center.weightLabel.setText(weight))
        self.threadpool.signals.data.connect(lambda: self.analysis_center.flowRateLabel.setText(str(self.calculateFlowRate())))
        self.threadpool.graph_thread.signals.finished.connect(lambda: self.analysis_center.flowRateLabel.setText(str(self.averageFlowRate())))
        
        self.threadpool.motor_thread.signals.finished.connect(lambda: self.statusText.setText('Standby'))
        self.threadpool.motor_thread.signals.toZero.connect(lambda: self.statusText.setText('Moving Motor to Zero'))
        self.threadpool.motor_thread.signals.execute.connect(lambda: self.statusText.setText('Executing Commands'))
        
        self.threadpool.connection_thread.signals.connected.connect(self.connected)
    
    # Update Analysis Center based on connection status ----------- #
    def drawAnalysis(self):
        if self.device.scale.device is None:
            #self.analysis_center.weightLabel.setText('Scale not found')
            self.analysis_center.tareScale.setEnabled(False)
        else:
            self.analysis_center.tareScale.setEnabled(True)
    
    
    # Update Execute Button based on connection and current state ----------- #
    def drawExecuteButton(self):
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
    def openRotaryCalibration(self):
        if self.device.errors[0] is not None:
            QMessageBox.critical(self, "Error", "Rotary motor not found!")
            return

        self.rotary_calibration = CalibrationMenu(self)
        self.rotary_calibration.show()
    
    # Execute Commands ----------- #
    def execute(self):
        print('Executing commands...')
        command_set = self.getCommands()
        self.threadpool.start_process(command_set)
    
    # Update UI based on connection status ----------- #
    def connected(self):
        self.drawErrorLayout()
        self.drawExecuteButton()
        self.drawAnalysis()
    
    # Update Graph ----------- #
    def updateGraph(self, time, weight):
        # Add data to the dataframe
        self.data = pd.concat([self.data, pd.DataFrame({'Time': [time], 'Weight': [weight]})])
        
        # Update the graph
        x = self.data['Time']
        y = self.data['Weight']
        self.graph.set_data(x, y)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw_idle()
        
    def resetGraph(self):
        self.data = pd.DataFrame(columns=['Time', 'Weight'])
        x = self.data['Time']
        y = self.data['Weight']
        self.graph.set_data(x, y)

        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw_idle()
    
    def calculateFlowRate(self):
        # Calculate the flow rate based on the data collected
        if len(self.data) > 1:
            time_diff = self.data['Time'].diff().iloc[1:]
            weight_diff = self.data['Weight'].diff().iloc[1:]
            flow_rate = weight_diff / time_diff
            self.flow_rate = round(flow_rate.mean(), 3)
            return self.flow_rate
        return 0.0
    
    def averageFlowRate(self):
        if len(self.data) > 1:
            total_weight = self.data['Weight'].iloc[-1] - self.data['Weight'].iloc[0]
            total_time = self.data['Time'].iloc[-1] - self.data['Time'].iloc[0]
            if total_time > 0:
                return round(total_weight / total_time, 3)
        return 0.00
    
    #---------------------------------------------------------#
    
    # File Menu Actions
    
    # Export commands to CSV
    def storeCommandsToCSV(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Commands to CSV", "datasheet", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Speed', 'Strokes', 'Acceleration', 'Flow Direction', 'Duration', 'Iterations', 'Position'])
                control_sets = self.getCommands()
                for commands in control_sets:
                    writer.writerow(commands.array())
            QMessageBox.information(self, 'Success', f'Commands saved to {file_name}')

    # Import commands from CSV
    def importCommandsFromCSV(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Commands from CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as csvfile:
                command_reader = csv.reader(csvfile)
                command = [row[1] for row in command_reader if row]
                inp = CommandSet().set(set = command)
                self.addControlCenterTab(commands=inp)
            QMessageBox.information(self, 'Success', f'Commands imported from {file_name}')
           
    # Export data to CSV 
    def exportDataToCSV(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data to CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            self.data.to_csv(file_name)
            QMessageBox.information(self, 'Success', f'Data saved to {file_name}')
    
    # On close, save data to CSV
    def failsafeToCSV(self):
        try:
            filepath = os.path.join(os.getcwd(), 'data.csv')
            self.data.to_csv(filepath)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error saving data: {e}')
            
    def resetUI(self):
        # Reset data and control sets
        self.data = pd.DataFrame(columns=['Time', 'Weight'])
        self.control_sets = []
        self.resetGraph()
        
        # Reset device and threadpool
        try:
            interface = ConnectionManager().connect()
        except Exception as e:
            interface = None
            print(f'Error: {e}')
        
        self.device = Controller(interface)
        self.threadpool = ThreadPool(self.device)
        
        # Reinitialize UI elements
        self.drawErrorLayout()
        self.drawExecuteButton()
        self.drawAnalysis()
        
        # Restart thread connections
        self.setConnections()
        self.threadpool.start_connection()

    #---------------------------------------------------------#

if __name__ == '__main__':
    def close_threads():
        ex.threadpool.stop()
        ex.failsafeToCSV()
        
    # Add a key event to toggle fullscreen on F11
    def toggle_fullscreen(event):
        if event.key() == Qt.Key.Key_F11:
            if ex.isFullScreen():
                ex.showNormal()
            else:
                ex.showFullScreen()
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(close_threads)
    ex = App()
    ex.show()

    app.installEventFilter(ex)
    ex.keyPressEvent = toggle_fullscreen
    sys.exit(app.exec())
    

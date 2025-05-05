from datetime import datetime
import sys
from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
matplotlib.use('QtAgg')
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTabWidget, QFileDialog, QMessageBox, QMenuBar, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from pytrinamic.connections import ConnectionManager
from Controller.Controller import Controller
from Controller.CommandSet import CommandSet
from Threads.ThreadPool import ThreadPool
from Interface.Style import apply_style
from Interface.AnalysisCenter import AnalysisCenter
from Interface.ControlCenter import ControlCenter
from Interface.CalibrationMenu import CalibrationMenu
from Interface.NozzleMenu import NozzleMenu
from Interface.Keyboard import Keyboard
import subprocess
import csv
import os
from PyQt6.QtGui import QIcon
import time

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
        plt.tight_layout(pad=6)
        self.graph, = self.ax.plot(self.data['Time'], self.data['Weight'])
        self.graph.set_data(self.data['Time'], self.data['Weight'])
        self.ax.autoscale(enable=True, axis='both')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Weight (g)')
        self.ax.set_title('Weight vs Time')
        self.fig.set_facecolor('#f0f0f0')
        
        self.setWindowIcon(QIcon('interface/logo.png'))
        #self.setGeometry(0, 0, 1024, 600)
        self.showFullScreen()
        self.setCursor(Qt.CursorShape.BlankCursor)
        
        self.initUI() 
            
    
    def initUI(self):
        
        # Stylesheet
        apply_style(self)
        
        # Setup
        self.setWindowTitle('BencH2O Fluidics Delivery')
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.makeMenuBar()
        
        self.drawErrorLayout()
        
        
        #---------------------------------------------------------#
        app_layout = QVBoxLayout()
        app_layout.setContentsMargins(10, 10, 10, 10)
        
        app_layout.addLayout(self.errorLayout)
        
        # Device Control Center
        self.control_layout = QHBoxLayout()
        # Add a tab widget to hold multiple control centers
        self.control_tabs = QTabWidget()
        
        # Add the initial control center tab
        self.control_tabs.setObjectName('tab_bar')
        
        # Button to add a new control center
        add_tab_button = QPushButton("+", self)
        add_tab_button.setToolTip("Add a new control center tab")
        add_tab_button.setObjectName("small")
        add_tab_button.clicked.connect(self.addControlCenterTab)
        
        # Button to remove the last control center
        remove_tab_button = QPushButton("-", self)
        remove_tab_button.setToolTip("Remove the control center tab")
        remove_tab_button.setObjectName("small")
        remove_tab_button.clicked.connect(self.removeControlCenterTab)
        
        #File Menu
        export_action = QPushButton('Export', self)
        export_action.clicked.connect(self.storeCommandsToCSV)
        export_action.setObjectName('small')
        export_action.setStyleSheet('font-size: 10px;')
        
        import_action = QPushButton('Import', self)
        import_action.clicked.connect(self.importCommandsFromCSV)
        import_action.setObjectName('small')
        import_action.setStyleSheet('font-size: 10px;')
        
        control_buttons = QVBoxLayout()
        control_buttons.addWidget(add_tab_button)
        control_buttons.addWidget(remove_tab_button)
        control_buttons.addWidget(export_action)
        control_buttons.addWidget(import_action)
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
        
        self.keyboard = Keyboard()
        self.analysis_layout.addWidget(self.keyboard.keyboard_widget, alignment=Qt.AlignmentFlag.AlignBottom)
        self.keyboard.keyboard_widget.hide()
        
        
        button_layout = QHBoxLayout()
        
        # Prime button for allowing user to manually prime system
        self.prime_button = QPushButton('Prime Tubing', self)
        self.prime_button.setToolTip('Run rotary motor until fluid reaches the end of the tubing')
        self.prime_button.clicked.connect(self.threadpool.prime)
        
        self.drawPrimeButton()
        button_layout.addWidget(self.prime_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.flush_button = QPushButton('Flush', self)
        self.flush_button.clicked.connect(self.threadpool.flush)
        button_layout.addWidget(self.flush_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.statusText = QLabel('Standby', self)
        self.statusText.setObjectName('title')
        button_layout.addWidget(self.statusText, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        export_button = QPushButton('Export Data', self)
        export_button.setToolTip('Export Data to CSV')
        export_button.clicked.connect(self.exportDataToCSV)
        button_layout.addWidget(export_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.execute_button = QPushButton('Execute', self)
        self.execute_button.setToolTip('Execute Commands')
        self.execute_button.setText('Execute')
        self.execute_button.clicked.connect(self.execute)
        self.drawExecuteButton()
        button_layout.addWidget(self.execute_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        
        # Add Layouts to Main Layout ------------------#
        app_layout.addLayout(self.control_layout)
        self.control_layout.addLayout(self.analysis_layout)
        app_layout.addLayout(button_layout)
        
        self.layout.addLayout(app_layout)
        
        self.setLayout(self.layout)

        # Connection Signals
        self.setConnections()
        self.threadpool.start_connection()
        self.attach_keyboard_events()
        
        # Testing Area. Commment out contents before use #
        # self.graph_thread.start()
        
    def attach_keyboard_events(self):
        if isinstance(self, QWidget):
            for child in self.findChildren(QWidget):
                if isinstance(child, QLineEdit):
                    child.focusInEvent = lambda event: self.show_keyboard()
                    child.focusOutEvent = lambda event: self.hide_keyboard()
    
    # On-Screen Keyboard for QLineEdit
    def show_keyboard(self):
        self.analysis_center.Container.hide()
        self.keyboard.keyboard_widget.show()

    def hide_keyboard(self):
        self.keyboard.keyboard_widget.hide()
        self.analysis_center.Container.show()
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
        menu_bar = QWidget()
        menu_bar.setObjectName('menubar')
        menubar = QHBoxLayout(menu_bar)
        menubar.setContentsMargins(5,5,5,5)
        
        #Tools Menu        
        calibrate_action = QPushButton('Calibrate Rotary', self)
        calibrate_action.clicked.connect(self.openRotaryCalibration)
        calibrate_action.setObjectName('barbutton')
        menubar.addWidget(calibrate_action)
        
        nozzle_action = QPushButton('Adjust Nozzle', self)
        nozzle_action.clicked.connect(self.openNozzleMenu)
        nozzle_action.setObjectName('barbutton')
        menubar.addWidget(nozzle_action)
        
        reset_action = QPushButton('Reset', self)
        reset_action.setObjectName('barbutton')
        reset_action.clicked.connect(self.resetUI)
        menubar.addWidget(reset_action)
        
        # Add a close button to the menu bar and align it to the far right
        close_action = QPushButton('Close', self)
        close_action.clicked.connect(self.close)
        close_action.setObjectName('barbutton')
        menubar.addWidget(close_action, alignment=Qt.AlignmentFlag.AlignRight)
                
        self.layout.addWidget(menu_bar, alignment=Qt.AlignmentFlag.AlignTop)
    
    def drawErrorLayout(self, error=None):
        if error == "Scale:":
            self.device.errors[2] = error
            
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
        self.control_tabs.addTab(new_control_center.Container, f"Task {self.control_tabs.count() + 1}")
        self.control_sets.append(new_control_center)
        if commands is not None:
            new_control_center.set_commands(commands)
        self.attach_keyboard_events()
        self.control_tabs.setCurrentWidget(new_control_center.Container)
            
    def removeControlCenterTab(self):
        # Remove the current control center tab
        if self.control_tabs.count() > 0:
            self.control_tabs.removeTab(self.control_tabs.currentIndex())
            # Remove the corresponding control center from the list
            self.control_sets.pop()
            for i in range(self.control_tabs.count()):
                self.control_tabs.setTabText(i, f"Task {i + 1}")
        else:
            QMessageBox.warning(self, "Warning", "No staged commands to remove.")
        
    # Set up connections for the threads ----------- #
    
    def setConnections(self):
        # UI Elements are updated based on the connection status of the device
        self.threadpool.motor_thread.signals.start.connect(self.drawExecuteButton)
        self.threadpool.motor_thread.signals.complete.connect(self.drawExecuteButton)
        
        self.threadpool.signals.started.connect(self.resetGraph)
        self.threadpool.signals.log.connect(lambda t, w: self.updateGraph(t, w))
        self.threadpool.signals.data.connect(lambda weight: self.analysis_center.weightLabel.setText(weight))
        self.threadpool.signals.data.connect(lambda: self.analysis_center.flowRateLabel.setText(str(self.calculateFlowRate())))
        self.threadpool.graph_thread.signals.finished.connect(lambda: self.analysis_center.flowRateLabel.setText(str(self.averageFlowRate())))
         
        self.threadpool.motor_thread.signals.complete.connect(lambda: self.statusText.setText('Standby'))
        self.threadpool.motor_thread.signals.toZero.connect(lambda: self.statusText.setText('Moving Motor to Zero'))
        self.threadpool.motor_thread.signals.execute.connect(lambda: self.statusText.setText('Executing Commands'))
        
        self.threadpool.connection_thread.signals.connected.connect(self.connected)
        
        self.threadpool.weight_thread.signals.error.connect(lambda e, d: self.drawErrorLayout(d))
        self.threadpool.prime_thread.signals.start.connect(self.drawPrimeButton)
        self.threadpool.prime_thread.signals.primed.connect(self.drawPrimeButton)
        self.threadpool.prime_thread.signals.start.connect(lambda: self.statusText.setText('Priming'))
        self.threadpool.prime_thread.signals.primed.connect(lambda: self.statusText.setText('Primed'))
        
        self.threadpool.graph_thread.signals.result.connect(lambda t, w: self.threadpool.signals.log.emit(t, w))
        
        # Set motor thread signal connections
        self.threadpool.motor_thread.signals.execute.connect(lambda: self.threadpool.graph_thread.resume())
        self.threadpool.motor_thread.signals.finished.connect(lambda: self.threadpool.graph_thread.pause())
        self.threadpool.motor_thread.signals.finished.connect(lambda: self.threadpool.signals.finished.emit())
        self.threadpool.motor_thread.signals.error.connect(lambda e: QMessageBox.critical(None, 'Error', f'Error: {e}'))
    
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
            
            self.flush_button.hide()
        
        # If the motor is running, disable the execute button
        elif self.threadpool.motor_thread._is_running == True:
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: red;')
            self.execute_button.setToolTip('STOP MOTOR')
            self.execute_button.setText('STOP MOTOR')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.threadpool.stop)
            
            self.flush_button.setEnabled(False) 
            self.prime_button.setEnabled(False)
        
        # If the motor is not running, enable the execute button
        elif (self.device.module is not None) and (self.threadpool.motor_thread._is_running == False):
            self.execute_button.setEnabled(True)
            self.execute_button.setStyleSheet('background-color: #0B41CD;')
            self.execute_button.setToolTip('Execute Commands')
            self.execute_button.setText('Execute')
            self.execute_button.clicked.disconnect()
            self.execute_button.clicked.connect(self.execute)
            
            self.flush_button.setEnabled(True)
            self.prime_button.setEnabled(True)
            
    def drawPrimeButton(self):
        if self.device.module != None:
            if self.device.primed is False:
                self.prime_button.setEnabled(True)
                self.prime_button.setToolTip('Run rotary motor until fluid reaches the end of the tubing')
                self.prime_button.setText('Prime Tubing')
            elif self.threadpool.prime_thread._is_running == True:
                self.prime_button.setEnabled(True)
                self.prime_button.setStyleSheet('background-color: red;')
                self.prime_button.setToolTip('STOP MOTOR')
                self.prime_button.setText('STOP MOTOR')
                self.prime_button.clicked.disconnect()
                self.prime_button.clicked.connect(self.threadpool.stop)   
            else:
                self.prime_button.setEnabled(True)
                self.prime_button.setStyleSheet('background-color: #0B41CD;')
                self.prime_button.setToolTip('Click to adjust primed fluid')
                self.prime_button.setText('Tubing Primed')
        else:
            self.prime_button.hide()
    
    # Open Rotary Motor Calibration Window ----------- #
    def openRotaryCalibration(self):
        if self.device.errors[0] is not None:
            QMessageBox.critical(self, "Error", "Rotary motor not found!")
            return

        self.rotary_calibration = CalibrationMenu(self)
        self.rotary_calibration.show()
        
    # Open Nozzle Menu ----------- #
    def openNozzleMenu(self):
        try:
            self.nozzle_menu = NozzleMenu(self)
            self.nozzle_menu.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Nozzle not found: {e}")
            return
    
    # Execute Commands ----------- #
    def execute(self):
        print('Executing commands...')
        self.analysis_center.Container.show()
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
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            focused_widget = self.focusWidget()
            if isinstance(focused_widget, QLineEdit):
                focused_widget.clearFocus()
    
    #---------------------------------------------------------#
    
    # File Menu Actions
    
    # Export commands to CSV
    def storeCommandsToCSV(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Commands to CSV", datetime.now().strftime("execution_%Y-%m-%d_%H-%M-%S.csv"), "CSV Files (*.csv);;All Files (*)")
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
                for row in command_reader:
                    # Skip the first row in the import. Just has labels.
                    if row[0] == "Speed":
                        continue
                    if row:
                        command = row
                        inp = CommandSet()
                        inp.importSet(set=command)
                        self.addControlCenterTab(commands=inp)
            QMessageBox.information(self, 'Success', f'Commands imported from {file_name}')
           
    # Export data to CSV 
    def exportDataToCSV(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Data to CSV", datetime.now().strftime("data_%Y-%m-%d_%H-%M-%S.csv"), "CSV Files (*.csv);;All Files (*)")
        if file_name:
            try:
                self.data.to_csv(file_name)
                QMessageBox.information(self, 'Success', f'Data saved to {file_name}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error saving data: {e}')
    
    # On close, save data to CSV
    def failsafeToCSV(self):
        try:
            filepath = os.path.join(os.getcwd(), 'data.csv')
            self.data.to_csv(filepath)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error saving data: {e}')
        
        # Add a key event to toggle fullscreen on F11
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def resetUI(self):
        # Reset data and control sets
        subprocess.run("./reset.sh")

    #---------------------------------------------------------#

if __name__ == '__main__':
    def close_threads():
        ex.threadpool.stop()
        ex.failsafeToCSV()
        try:
            if ex.device.nozzle is not None:
                ex.device.nozzle.cleanup()
        except Exception as e:
            print(f'Error: {e}')
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(close_threads)
    ex = App()
    ex.installEventFilter(ex)
    ex.mousePressEvent
    
    ex.show()

    sys.exit(app.exec())
    

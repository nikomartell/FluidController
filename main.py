import sys
import serial
from Controller import Controller
from ControlCenter import controlCenter
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QMenuBar, QFileDialog, QSizePolicy
from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtGui import QAction
from ConnectionThread import ConnectionThread
import csv

class App(QWidget):
    def __init__(self):        
        super().__init__()
        self.find_controller()
        self.initUI()
    
    def initUI(self):
        
        
        # Stylesheet
        with open("main.css", "r") as file:
            self.setStyleSheet(file.read())
        
        # Setup
        self.setWindowTitle('Fluidics Device Controller')
        self.layout = QVBoxLayout()
        # Multithreading
        self.threadpool = QThreadPool()
        connections = ConnectionThread(self.find_controller())
        self.threadpool.start(connections)
        
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
        settings_action = QAction('Settings', self)
        settings_menu.addAction(settings_action)
        
        #Tools Menu
        tools_menu = menubar.addMenu('Tools')
        tools_action = QAction('Tools', self)
        tools_menu.addAction(tools_action)
        
        #Help Menu
        help_menu = menubar.addMenu('Help')
        self.layout.setMenuBar(menubar)
        help_action = QAction('Help', self)
        help_menu.addAction(help_action)
        #---------------------------------------------------------#
        
        # Device Control Center
        control_layout = QHBoxLayout()
        self.deviceControl = controlCenter(self.device)
        control_layout.addWidget(self.deviceControl.Container)
        
        # System Control (change this button to refresh device connection)
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton('Refresh Device Connection', self)
        self.refresh_button.clicked.connect(self.refresh_device_connection)
        button_layout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.send_commands_button = QPushButton('Send Commands', self)
        self.send_commands_button.setText('Execute')
        self.send_commands_button.setStyleSheet('background-color: #0B41CD;')
        self.send_commands_button.clicked.connect(self.execute)
        
        if self.device.module is None:
            self.send_commands_button.setEnabled(False)
            self.send_commands_button.setStyleSheet('background-color: red;')
            self.send_commands_button.setToolTip('Controller not found')
            self.send_commands_button.setText('Controller not found')
            
        button_layout.addWidget(self.send_commands_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.layout.addLayout(control_layout)
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)
    
    #---------------------------------------------------------#
    
    # Methods
    def find_controller(self):
        self.device = Controller()
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
    
    def execute(self):
        if self.device is None:
            QMessageBox.critical(self, 'Error', 'Controller not found')
            return
        commands = self.deviceControl.get_commands()
        self.device.send_commands(commands)


    def refresh_device_connection(self):
        self.device = Controller()
        self.initUI(self.device)
        
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
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())

import sys
import serial
from Controller import Controller
from ControlCenter import controlCenter
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QMenuBar, QFileDialog, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
import csv

class App(QWidget):
    def __init__(self):        
        super().__init__()
        self.find_controller()
        self.initUI(self.device)
        
    def find_controller(self):
        try:
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                if 'Controller' in port.description:
                    self.device = port.device
                    break
            else:
                self.device = None
        except Exception as e:
            self.device = None
    
    def initUI(self, device):
        
        # Stylesheet
        with open("main.css", "r") as file:
            self.setStyleSheet(file.read())
        
        # Setup
        self.setWindowTitle('Fluidics Device Controller')
        layout = QVBoxLayout()
        
        errorLayout = QHBoxLayout()
        errorLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        if device is not None:
            pump_info_label = QLabel(f'Device: {self.device.name}', self)
            pump_info_label.setStyleSheet('color: green; font-weight: bold;')
            pump_info_label.setObjectName('device_info')
            errorLayout.addWidget(pump_info_label, alignment=Qt.AlignmentFlag.AlignTop)
            for error in device.errors:
                if error is not None:
                    error_label = QLabel(error, self)
                    error_label.setStyleSheet('color: red; font-weight: bold;')
                    error_label.setObjectName('device_info')
                    errorLayout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignTop)
            
        if not self.device:
            error_label = QLabel('Device not found', self)
            error_label.setStyleSheet('color: red; font-weight: bold;')
            error_label.setObjectName('device_info')
            errorLayout.addWidget(error_label, alignment=Qt.AlignmentFlag.AlignTop)

        layout.addLayout(errorLayout)
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
        layout.setMenuBar(menubar)
        help_action = QAction('Help', self)
        help_menu.addAction(help_action)
        #---------------------------------------------------------#
        
        # Device Control Center
        control_layout = QHBoxLayout()
        self.deviceControl = controlCenter(device)
        control_layout.addWidget(self.deviceControl.Container)
        
        # System Control (change this button to refresh device connection)
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton('Refresh Device Connection', self)
        self.refresh_button.clicked.connect(self.refresh_device_connection)
        button_layout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.send_commands_button = QPushButton('Send Commands', self)
        self.send_commands_button.clicked.connect(self.execute)
        button_layout.addWidget(self.send_commands_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(control_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)
    
    #---------------------------------------------------------#
    
    # Methods
    def execute(self):
        if self.device is None:
            QMessageBox.critical(self, 'Error', 'Device not found')
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

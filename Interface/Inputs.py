from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QTimer, Qt
from Controller.CommandSet import CommandSet

class NumPad(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NumPad")
        self.setGeometry(100, 100, 300, 200)
        self.setObjectName('NumPad')
        
        self.layout = QVBoxLayout(self)
        
    def submit_number(self):
        number = self.input_field.text()
        if number:
            QMessageBox.information(self, "Number Submitted", f"You entered: {number}")
            # Here you can add the logic to send the number to the device
            # For example: CommandSet.send_number(float(number))
import sys
from Controller import Controller
from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel

def device_status(device):
    container = QWidget()
    
    layout = QVBoxLayout(container)
    device_status = QLabel('Device Status', container)
    
    layout.addWidget(device_status)
    if device is None:
        device_status.setText('Not connected')
        layout.addWidget(device_status)
        return container
    else:
        if device.is_active():
            device_status.setText('Active')
        else:
            device_status.setText('Inactive')
        layout.addWidget(device_status)
    
        return container
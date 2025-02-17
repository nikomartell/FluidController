from usbx import ControlTransfer, Recipient, RequestType, usb, device
import serial.tools.list_ports
from PyQt6.QtWidgets import QMessageBox
from ftd2xx import ftd2xx as ftd

class Scale:
    def __init__(self):
        self.name = None
        try:
            self.device = ftd.open(0)
            print(self.device.getDeviceInfo())
            print(self.get_weight())
        except:
            self.device = None
            print('Scale not found')  

    # Function called by Control Panel to tare the scale
    def tare(self):
        if self.device:
            self.device.write(b'\x55')
        else:
            raise Exception("Scale not found")
            
    # Function called by Analysis Center to read weight
    def get_weight(self):
        if self.device:
            weight = self.device.read(64)
            return self.parse_weight(weight)
        else:
            return "Scale not found"
        
    # Function to read the bytes from the scale and decode the data of it to legible weight
    def parse_weight(self, data):
        if not data or len(data) < 16:
            return None

        sign = data[0:1].decode('latin-1')
        weight = data[2:9].decode('latin-1')
        unit1 = data[11:12].decode('latin-1')
        unit2 = data[12:13].decode('latin-1')

        if sign == '-':
            weight = '-' + weight

        return float(weight.strip())

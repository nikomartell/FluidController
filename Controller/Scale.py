from usbx import ControlTransfer, Recipient, RequestType, usb, device
import serial.tools.list_ports
from PyQt6.QtWidgets import QMessageBox
from ftd2xx import ftd2xx as ftd

class Scale:
    def __init__(self):
        self.name = None
        self.device = ftd.open(0)
        print(self.device.getDeviceInfo())
        print(self.get_weight())       

    def send_command(self):
        if self.device:
            self.device.open()
            transfer = ControlTransfer(RequestType.VENDOR, Recipient.DEVICE, 0x01, 0x00, 0x00)
            self.device.control_transfer_out(transfer)
            self.device.close()
        else:
            raise Exception("Scale not found")
            
        
    def get_weight(self):
        if self.device:
            weight = self.device.read(64)
            return self.parse_weight(weight)
        
    def parse_weight(self, data):
        if not data or len(data) < 16:
            return "No data received from the scale"

        sign = data[0:1].decode('latin-1')
        weight = data[2:9].decode('latin-1')
        unit1 = data[11:12].decode('latin-1')
        unit2 = data[12:13].decode('latin-1')

        if sign == '-':
            weight = '-' + weight

        return float(weight.strip())

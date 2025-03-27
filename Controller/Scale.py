import time
from PyQt6.QtWidgets import QMessageBox
from ftd2xx import ftd2xx as ftd

class Scale:
    def __init__(self):
        self.name = None
        try:
            ftd.createDeviceInfoList()
            self.device = ftd.open(0)
            self.device.getDeviceInfo()
            self.weight = self.get_weight()
        except Exception as e:
            self.device = None 
            self.weight = 0.00
            print(f'Error: {e}')

    
    # Function called by Control Panel to tare the scale
    def tare(self):
        try:
            self.device.write(b'ST\r\n')
            time.sleep(2)
            self.device.purge()  # Clear the input and output buffers
        except Exception as e:
            print(f'Error: {e}')
    
    # Function called by Analysis Center to read weight
    def get_weight(self):
        try:
            if self.device:
                weight = self.device.read(16)
                return self.parse_weight(weight)
            elif self.device is None:
                return 0.00

        except Exception as e:
            return f'Error: {e}'
        
    # Function to read the bytes from the scale and decode the data of it to legible weight
    def parse_weight(self, data):
        if not data or len(data) < 16:
            return "Unknown"

        sign = data[0:1].decode('latin-1').strip()  # 1 - space or mark
        weight = data[1:10].decode('latin-1').strip()  # 2-10 - space, digits, or decimal point
        unit1 = data[11:12].decode('latin-1').strip()  # 12 - K, l, c, p, or space
        unit2 = data[12:13].decode('latin-1').strip()  # 13 - G, b, t, c, or %

        self.weight = float(weight)
        
        return sign + weight + ' ' + unit1 + unit2

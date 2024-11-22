import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    if 'USB' in port.hwid:
        vid = port.vid
        pid = port.pid
        print(f"Device: {port.device}, Description: {port.description}, Address: {port.hwid}, VID: {vid}, PID: {pid}")
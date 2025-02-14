from usbx import usb
from ftd2xx import ftd2xx

def list_usb_devices():
    with ftd2xx.open(0) as dev:
        print(dev.getDeviceInfo())
        print(dev.getQueueStatus())
        print(dev.getBitMode())
        print(dev.getLatencyTimer())

if __name__ == "__main__":
    list_usb_devices()
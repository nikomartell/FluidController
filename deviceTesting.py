from usbx import usb

def list_usb_devices():
    for device in usb.get_devices():
        print(device)

if __name__ == "__main__":
    list_usb_devices()
from usbx import usb

def list_usb_devices():
    device = usb.find_device(serial = "A9GKN3II")
    print(device)

if __name__ == "__main__":
    list_usb_devices()
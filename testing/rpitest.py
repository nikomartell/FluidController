import serial as ser

data = ser.Serial("/dev/ttyS0",9600,timeout=2)

data.write("hello".encode())

data.close()
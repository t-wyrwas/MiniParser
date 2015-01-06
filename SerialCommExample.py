import serial

ser = serial.Serial(
    port='COM2',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.flush()
ser.close()
ser.open()

if ser.isOpen():
    print("Port is opened.")

while 1:
    out = ser.readline()
    print "#> ", out

ser.flush()
ser.close()
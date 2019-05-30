import serial
import io
from time import sleep

'''
while True:
    sleep(0.1)
    with serial.Serial('/dev/ttyS0', 250000, timeout=1) as ser:
        x = ser.read()          # read one byte
        s = ser.read(10)        # read up to ten bytes (timeout)
        line = ser.readline()   # read a '\n' terminated line
        print(line)


ser = serial.serial_for_url('loop://', timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

sio.write(unicode("hello\n"))
sio.flush() # it is buffering. required to get the data out *now*
hello = sio.readline()
print(hello == unicode("hello\n"))

'''

port = "/dev/ttyUSB0"

s1 = serial.Serial(port, 115200)
s1.flushInput()

#n = input("Set X distance: ")
#print("G1 X{}\r\n".format(n))


while True:
    if s1.inWaiting()>0:
        while s1.inWaiting()>0:
            inputValue = s1.readline()
            if inputValue.decode().strip():
                print(inputValue.decode().strip())
    c = input()
    # print('{}\r\n'.format(c).encode())
    s1.write('{}\n'.format(c).encode())

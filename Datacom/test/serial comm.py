import serial
from time import sleep

port = "/dev/ttyUSB0"

s1 = serial.Serial(port, 115200)
sleep(2)
s1.flushInput()

# c = input()
# s1.write('{}\n'.format(c).encode())

while True:
    '''
    if s1.inWaiting()>0:
        while s1.inWaiting()>0:
            inputValue = s1.readline()
            if inputValue.decode().strip():
                print(inputValue.decode().strip())
    '''

    s1.write('M105 ?\n'.encode())
    inputValue = s1.readline()
    s = str(inputValue.decode())

    delchars = dict.fromkeys(map(ord, 'okT:/B@'), None)
    s = list(map(float, s.translate(delchars).strip().split(' ')))
    print(s)
    sleep(1)

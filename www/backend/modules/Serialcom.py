import serial
from time import sleep


class Serialcom:

    def __init__(self):
        try:
            port = "/dev/ttyUSB0"
            self.s1 = serial.Serial(port, 115200)
            sleep(2)  # wait till init message of printer
            self.s1.flushInput()
        except Exception as e:
            print(e)

        self.tempchars = dict.fromkeys(map(ord, 'okT:/B@'), None)
        self.coordchars = dict.fromkeys(map(ord, 'okC:XYZE'), None)

    def send_command(self, c):
        command = c["command"]

        if command == 'G28':
            gcode = 'G28'
            if 'x' in c['axis']:
                gcode += ' X'
            if 'y' in c['axis']:
                gcode += ' Y'
            if 'z' in c['axis']:
                gcode += ' Z'

        elif command == 'G1':
            gcode = 'G1'
            if 'x' in c['axis']:
                gcode += ' X'
            elif 'y' in c['axis']:
                gcode += ' Y'
            elif 'z' in c['axis']:
                gcode += ' Z'

            gcode += str(c['value'])

        else:
            gcode = c['command']

        try:
            print("Sent: ", '{}\n'.format(gcode).encode())
            self.s1.write('{}\n'.format(gcode).encode())
        except Exception as e:
            print("Serial send error: ", e)
        sleep(0.01)

        try:
            if self.s1.inWaiting() > 0:
                inputValue = self.s1.readline()
                s = str(inputValue.decode())
                if s.strip():
                    print("Response: ", s.strip())
                    if s.strip() == "ok":
                        return s.strip()
                    elif(s.startswith('ok T:')):
                        s = list(map(float, s.translate(self.tempchars).strip().split(' ')))
                        return s
                    elif (s.startswith('ok C:')):
                        s = list(map(float, s.translate(self.coordchars).strip().split(' ')))
                        return s
        except Exception as e:
            print('Response Decoding Error: ', e)

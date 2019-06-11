import serial
from time import sleep


class Serialcom:

    def __init__(self):
        try:
            port = "/dev/ttyUSB0"
            self.s1 = serial.Serial(port, 115200)
            sleep(2)
            self.s1.flushInput()
        except Exception as e:
            print(e)

        self.delchars = dict.fromkeys(map(ord, 'okT:/B@'), None)

    def send_command(self, c):

        print(c)
        command = c["command"]

        gcode = ""
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

            if 'negative' in c.keys() and c['negative']:
                gcode += '-'

            gcode += str(c['value'])

        elif command == 'M18':
            gcode = 'M18'

        elif command == 'M106':
            gcode = 'M106'

        elif command == 'M107':
            gcode = 'M107'

        else:
            print("no known command or 'command' is null")
            gcode = c['command']

        print("send: ", '{}\n'.format(gcode).encode())
        try:
            self.s1.write('{}\n'.format(gcode).encode())
            sleep(0.02)

            if self.s1.inWaiting() > 0:
                inputValue = self.s1.readline()
                s = str(inputValue.decode())
                if s.strip():
                    print("ack: ", s.strip())
                    if s.strip() == "ok":
                        return s.strip()
                    else:
                        s = list(map(float, s.translate(self.delchars).strip().split(' ')))
                        return s
        except Exception as e:
            print('Response Decoding Error: ', e)

# setup serial communication with printer

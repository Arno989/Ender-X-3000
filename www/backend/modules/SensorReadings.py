from modules.DHT11 import DHT11
from modules.CCS811 import CCS811
from modules.I2C_LCD import I2C_LCD
from modules.PWM import PWM
from modules.OneWire import OneWire

from RPi import GPIO
import subprocess
from threading import Thread


class Sensor(Thread):  # Parent van Thread
    def __init__(self, conn, serial):
        Thread.__init__(self)  # Geef deze klasse door naar de parent Thread
        self.conn = conn
        self.serial = serial

        self.TCST2103 = 12
        self.relais = 17

        self.CCS811 = CCS811()
        self.DS18B20 = OneWire()

        self.R = PWM(21)
        self.G = PWM(20)
        self.B = PWM(16)

        self.printerdht = DHT11(pin=13)
        self.filamentdht = DHT11(pin=19)

        self.hysteresis = 2

        try:
            cmd = "ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'"
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = ps.communicate()
            self.local_ip = output[0].decode('ascii')[0:-1]
        except Exception as e:
            print("Ip Error: ", e)

        try:
            self.LCD = I2C_LCD()
            self.LCD.lcd_init()
            # ip = subprocess.check_output(['hostname', '--all-ip-addresses']).split()
            # ip1 = str(ip[0])[2:-1]
            self.LCD.lcd_string(self.local_ip, 1)
        except Exception as e:
            print("Lcd Error: ", e)

        GPIO.setmode(GPIO.BCM)

        self.R.InitPWM()
        self.G.InitPWM()
        self.B.InitPWM()

        GPIO.setup(self.TCST2103, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.relais, GPIO.OUT)

        GPIO.add_event_detect(self.TCST2103, GPIO.FALLING, callback=self.TCST2103_handler, bouncetime=200)

        self.daemon = True  # Zet hem in de achtergrond
        self.start()  # Start de aparte thread

    def run(self):
        while True:
            try:
                readingprn = self.read_printertemps()
                if readingprn:
                    self.save_sensor_data('th', readingprn[0])
                    self.save_sensor_data('tb', readingprn[2])
            except Exception as e:
                print("Serial error: ", e)

            try:
                readingamb = self.read_ambient_temp()
                if readingamb:
                    self.save_sensor_data('ta', readingamb)

                    if readingamb > 40 + self.hysteresis:
                        GPIO.output(self.relais, 1)
                    if readingamb < 40 - self.hysteresis:
                        GPIO.output(self.relais, 0)

            except Exception as e:
                print("onewire error: ", e)

            try:
                readingdht1 = self.filamentdht.getData()
                if readingdht1:
                    self.save_sensor_data('hp', readingdht1['humidity'])
            except Exception as e:
                print("DHT-1 error: ", e)

            try:
                readingdht2 = self.filamentdht.getData()
                if readingdht2:
                    self.save_sensor_data('hf', readingdht2['humidity'])
            except Exception as e:
                print("DHT-2 error: ", e)

            try:
                readingccs = self.read_CCS811()
                if readingccs:
                    self.save_sensor_data('co2', readingccs[0])
                    self.save_sensor_data('tvo', readingccs[1])
            except Exception as e:
                # print("CCS881 error: ", e)
                pass

            print("-----")
            pass


    def read_printertemps(self):
        t = self.serial.send_command({'command': 'M105 ?'})
        if t != 'ok':
            return t

    def read_ambient_temp(self):
        temp = self.DS18B20.get_slave("28-0416c0a80aff").get_data()
        temp = temp[:2] + "." + temp[2:4]
        return float(temp)

    def read_CCS811(self):
        values = self.CCS811.readSensor()
        return values

    def TCST2103_handler(self, arg):
        print("No filament detected!")

    def save_sensor_data(self, sensor, data):
        self.conn.set_data("INSERT INTO data (sensor, value) VALUES (%s, %s)", (sensor, data))

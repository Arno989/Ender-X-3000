from threading import Thread
from modules.DHT11 import DHT11
from modules.CCS811 import CCS811
from modules.I2C_LCD import I2C_LCD
from modules.PWM import PWM
from modules.OneWire import OneWire
from modules.Serialcom import Serialcom

from RPi import GPIO
from time import sleep
from subprocess import check_output


class Sensor(Thread):  # Parent van Thread
    def __init__(self, conn, serial):
        Thread.__init__(self)  # Geef deze klasse door naar de parent Thread
        self.conn = conn
        self.serial = serial

        self.TCST2103 = 12
        self.relais = 17

        self.CCS811 = CCS811()
        self.DS18B20 = OneWire()
        self.R = PWM(16)
        self.G = PWM(20)
        self.B = PWM(21)
        self.printerdht = DHT11(pin=13)
        self.filamentdht = DHT11(pin=19)

        try:
            self.LCD = I2C_LCD()
            self.LCD.lcd_init()
            ip = check_output(['hostname', '--all-ip-addresses']).split()
            ip1 = str(ip[0])[2:-1]
            self.LCD.lcd_string(ip1, 1)
        except Exception as e:
            print("Lcd Error: ", e)

        GPIO.setmode(GPIO.BCM)

        self.R.InitPWM()
        self.G.InitPWM()
        self.B.InitPWM()

        self.R.ChangeDutyCycle(80)
        self.G.ChangeDutyCycle(80)
        self.B.ChangeDutyCycle(80)

        GPIO.setup(self.TCST2103, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.relais, GPIO.OUT)

        GPIO.add_event_detect(self.TCST2103, GPIO.FALLING, callback=self.TCST2103_handler, bouncetime=200)

        self.daemon = True  # Zet hem in de achtergrond
        self.start()  # Start de aparte thread

    def run(self):  # Dit wordt gerunt door self.start().
        #  de run functie niet zelf starten. je moet de effectieve thread starten
        while True:  # Spreekt voor zich
            try:
                readingprn = self.read_printertemps()
                if readingprn:
                    self.save_sensor_data('th', readingprn[0])
                    print("Hotend Temperature: ", readingprn[0], " °C")
                    sleep(1)
                    self.save_sensor_data('tb', readingprn[2])
                    print("Bed Temperature: ", readingprn[2], " °C")
                else:
                    print("No reading Printer")
            except Exception as e:
                print("Serial error: ", e)

            try:
                readingamb = self.read_ambient_temp()
                if readingamb:
                    self.save_sensor_data('ta', readingamb)
                    sleep(0.5)
                    print("Ambient Temperature: ", readingamb, " °C")
                else:
                    print("No reading OneWire")
            except:
                print("onewire error")

            try:
                readingdht1 = self.filamentdht.getData()
                if readingdht1:
                    self.save_sensor_data('hp', readingdht1['humidity'])
                    sleep(0.5)
                    print("Printer Humidity: ", readingdht1['humidity'], "%")
                else:
                    print("No reading DHT1")
            except:
                print("dht1 error")

            try:
                readingdht2 = self.filamentdht.getData()
                if readingdht2:
                    self.save_sensor_data('hf', readingdht2['humidity'])
                    sleep(0.5)
                    print("Filament Humidity: ", readingdht2['humidity'], "%")
                else:
                    print("No reading DHT2")
            except:
                print("dht2 error")

            try:
                readingccs = self.read_CCS811()
                if readingccs:
                    self.save_sensor_data('co2', readingccs[0])
                    print("CO2: ", readingccs[0])
                    sleep(1)  # timestamp is PK
                    self.save_sensor_data('tvo', readingccs[1])
                    print("TVOC: ", readingccs[1])
                else:
                    print("No reading CCS811")
            except:
                print("ccs error")

            sleep(1)
            print("-----")
            pass

    def write_serial(self, command):
        return self.serial.send_command(command)

    def read_printertemps(self):
        t = self.serial.send_command({'command': 'M105 ?'})
        if t != 'ok':
            return t

    def read_ambient_temp(self):
        temp = self.DS18B20.get_slave("28-0416c0a80aff").get_data()
        temp = temp[:2] + "." + temp[2:4]
        return float(temp)

    def read_CCS811(self):
        try:
            values = self.CCS811.readSensor()
            return (values)
        except Exception as e:
            print(e)

    def TCST2103_handler(self, arg):
        print("No filament detected!")

    def save_sensor_data(self, sensor, data):
        self.conn.set_data("INSERT INTO data (sensor, value) VALUES (%s, %s)", (sensor, data))

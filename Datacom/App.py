from modules.DHT11 import DHT11
from modules.CCS811 import CCS811
from modules.I2C_LCD import I2C_LCD
from modules.PWM import PWM
from modules.OneWire import OneWire
from modules.SaveData import DataHandler

from RPi import GPIO
from time import sleep
import serial
from subprocess import check_output

TCST2103 = 12
relais = 17
port = "/dev/ttyUSB0"

CCS811 = CCS811()
DS18B20 = OneWire()
LCD = I2C_LCD()
R = PWM(16)
G = PWM(20)
B = PWM(21)
printerdht = DHT11(pin=13)
filamentdht = DHT11(pin=19)

s1 = serial.Serial(port, 115200)

sleep(2)
s1.flushInput()

database = DataHandler("site", "sensoruser", "sensoruser")


def write_serial(command):
    s1.write('{}\n'.format(command).encode())
    read_serial()


def read_serial():
    if s1.inWaiting() > 0:
        while s1.inWaiting() > 0:
            inputValue = s1.readline()
            if inputValue.decode().strip():
                print(inputValue.decode().strip())


def read_printertemps():
    s1.write('M105 ?\n'.encode())
    s = str(s1.readline().decode())

    delchars = dict.fromkeys(map(ord, 'okT:/B@'), None)
    s = list(map(float, s.translate(delchars).strip().split(' ')))
    return s


def read_ambient_temp():
    temp = DS18B20.get_slave("28-0416c0a80aff").get_data()
    temp = temp[:2] + "." + temp[2:4]
    return float(temp)


def read_CCS811():
    try:
        values = CCS811.readSensor()
        return(values)
    except Exception as e:
        print(e)


def TCST2103_handler(arg):
    print("No filament detected!")


def init():
    LCD.lcd_init()
    ip = check_output(['hostname', '--all-ip-addresses']).split()
    ip1 = str(ip[0])[2:-1]
    LCD.lcd_string(ip1, 1)

    GPIO.setmode(GPIO.BCM)

    R.InitPWM()
    G.InitPWM()
    B.InitPWM()

    R.ChangeDutyCycle(80)
    G.ChangeDutyCycle(80)
    B.ChangeDutyCycle(80)

    GPIO.setup(TCST2103, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(relais, GPIO.OUT)

    GPIO.add_event_detect(TCST2103, GPIO.FALLING, callback=TCST2103_handler, bouncetime=200)


try:
    init()

    while True:
        try:
            readingprn = read_printertemps()
            if read_printertemps():
                database.save_data('th', readingprn[0])
                print("Hotend Temperature: ", readingprn[0], " °C")
                sleep(1)
                database.save_data('tb', readingprn[2])
                print("Bed Temperature: ", readingprn[2], " °C")
            else:
                print("No reading Printer")
        except:
            print("Serial error")

        try:
            readingamb = read_ambient_temp()
            if readingamb:
                database.save_data('ta', readingamb)
                sleep(0.5)
                print("Ambient Temperature: ", readingamb, " °C")
            else:
                print("No reading OneWire")
        except:
            print("onewire error")

        try:
            readingdht1 = filamentdht.getData()
            if readingdht1:
                database.save_data('hp', readingdht1['humidity'])
                sleep(0.5)
                print("Printer Humidity: ", readingdht1['humidity'], "%")
            else:
                print("No reading DHT1")
        except:
            print("dht1 error")

        try:
            readingdht2 = filamentdht.getData()
            if readingdht2:
                database.save_data('hf', readingdht2['humidity'])
                sleep(0.5)
                print("Filament Humidity: ", readingdht2['humidity'], "%")
            else:
                print("No reading DHT2")
        except:
            print("dht2 error")

        try:
            readingccs = read_CCS811()
            if readingccs:
                database.save_data('co2', readingccs[0])
                print("CO2: ", readingccs[0])
                sleep(1)  # timestamp is PK
                database.save_data('tvo', readingccs[1])
                print("TVOC: ", readingccs[1])
            else:
                print("No reading CCS811")
        except:
            print("ccs error")

        sleep(1)
        print("-----")
        pass



except KeyboardInterrupt:
    print('Ok bye.')

except Exception as e:
    print(e)

finally:
    GPIO.cleanup()

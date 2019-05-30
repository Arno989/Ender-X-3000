from modules.DHT11 import DHT11
from modules.CCS811 import CCS811
from modules.I2C_LCD import I2C_LCD
from modules.PWM import PWM
from modules.OneWire import OneWire
from modules.SaveData import DataHandler

from RPi import GPIO
from time import sleep
from subprocess import check_output

TCST2103 = 12
relais = 17

CCS811 = CCS811()
DS18B20 = OneWire()
LCD = I2C_LCD()

printerdht = DHT11(pin=13)
filamentdht = DHT11(pin=19)

database = DataHandler("site", "sensoruser", "sensoruser")


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

    GPIO.setup(TCST2103, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(relais, GPIO.OUT)

    GPIO.add_event_detect(TCST2103, GPIO.FALLING, callback=TCST2103_handler, bouncetime=200)


try:
    init()

    while True:
        if read_ambient_temp():
            # database.save_data('ta', read_ambient_temp())
            print("Ambient Temperature: ", read_ambient_temp(), " °C")
        else:
            print("No reading OneWire")

        if printerdht.getData():
            # database.save_data('hp', printerdht.getData()['humidity'])
            print("Printer Humidity: ", printerdht.getData()['humidity'], "%")
        else:
            print("No reading DHT1")

        if filamentdht.getData():
            # database.save_data('hf', filamentdht.getData()['humidity'])
            print("Filament Humidity: ", filamentdht.getData()['humidity'], "%")
        else:
            print("No reading DHT2")

        readings = read_CCS811()
        if readings:
            # database.save_data('co', readings[0])
            print("CO2: ", readings[0])
            # database.save_data('tv', readings[1])
            print("TVOC: ", readings[1])
        else:
            print("No reading CCS811")

        sleep(.001)
        print("-----")
        pass



except KeyboardInterrupt:
    print('Ok bye.')

except Exception as e:
    print(e)

finally:
    GPIO.cleanup()

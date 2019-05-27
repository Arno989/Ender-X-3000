import modules.DHT11
import modules.CCS811
import modules.PWM
import modules.OneWire
from RPi import GPIO
from time import sleep

TCST2103 = 12
relais = 17


def TCST2103_handler(arg):
    print("No fillament detected!")
    pass


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TCST2103, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(TCST2103, GPIO.FALLING, callback=TCST2103_handler, bouncetime=200)
    GPIO.setup(relais, GPIO.OUT)
    #GPIO.setup(led, GPIO.OUT)

try:
    init()

    while True:
        sleep(0.1)
        pass

except KeyboardInterrupt:
    print('Ok bye.')

except Exception as e:
    print(e)

finally:
    GPIO.cleanup()

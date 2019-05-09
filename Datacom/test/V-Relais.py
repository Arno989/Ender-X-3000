from RPi import GPIO
from time import sleep

relais = 6

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relais, GPIO.OUT)

try:
    init()
    while True:
        GPIO.output(relais, GPIO.HIGH)
        sleep(2)
        GPIO.output(relais, GPIO.LOW)
        sleep(2)
        pass

except KeyboardInterrupt:
    print('Ok bye.')

except Exception as e:
    print(e)

finally:
    GPIO.cleanup()



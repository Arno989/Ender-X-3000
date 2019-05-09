from RPi import GPIO
from time import sleep

detector = 27
led = 25

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(detector, GPIO.IN)
    GPIO.setup(led, GPIO.OUT)

try:
    init()
    counter = 0

    while True:
        if GPIO.input(detector):
            print("Object " + str(counter))
            counter += 1
            GPIO.output(led, GPIO.LOW)
        else:
            GPIO.output(led, GPIO.HIGH)
        sleep(0.1)
        pass

except KeyboardInterrupt:
    print('Ok bye.')

except Exception as e:
    print(e)

finally:
    GPIO.cleanup()



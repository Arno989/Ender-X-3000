from RPi import GPIO
from time import sleep
from modules.PWM import PwmPin

fan = 17

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fan, GPIO.OUT)

def askPWM(pwmobj):
    pwm = input("Give pwm duty cycle: ")
    pwmobj.duty_cycle(pwm)

try:
    init()
    pwmFan = PwmPin(fan)

    while True:
        askPWM(pwmFan)
        sleep(0.1)
        pass

except KeyboardInterrupt:
    print('Ok bye.')

except Exception as e:
    print(e)

finally:
    GPIO.cleanup()

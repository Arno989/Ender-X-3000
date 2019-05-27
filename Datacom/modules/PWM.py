from RPi import GPIO
import time

class PWM():
    def __init__(self, pin):
        self.pin = pin

    def InitPWM(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 100)
        self.pwm.start(100)

    def ChangeDutyCycle(self, value):
        self.pwm.ChangeDutyCycle(value)
        time.sleep(2)
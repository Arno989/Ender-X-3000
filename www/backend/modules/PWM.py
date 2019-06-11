from RPi import GPIO

class PWM():
    def __init__(self, pin):
        self.pin = pin

    def InitPWM(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(100)

    def ChangeDutyCycle(self, value):
        self.pwm.ChangeDutyCycle(value)
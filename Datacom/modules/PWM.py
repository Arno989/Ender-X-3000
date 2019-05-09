from RPi import GPIO


class PwmPin:
    def __init__(self, pin, frequency=1000, duty_cycle=0):
        self.pin = pin
        self._duty_cycle = duty_cycle
        self._pwm = GPIO.PWM(pin, frequency)
        self._pwm.start(duty_cycle)

    @property
    def duty_cycle(self):
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        if value < 0 or value > 100:
            raise ValueError("dutycycle must have a value from 0 to 100")
        else:
            self._duty_cycle = value
            self._pwm.ChangeDutyCycle(value)

    def on(self):
        self._pwm.start(self._duty_cycle)

    def off(self):
        self._pwm.stop()

    def __del__(self):
        self._pwm.stop()

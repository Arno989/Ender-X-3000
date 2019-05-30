import Adafruit_DHT


class DHT11:
    def __init__(self, sensor=Adafruit_DHT.DHT11, pin=16):
        self.sensor = sensor
        self.pin = pin

    def getData(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin, 5, 0.2)

        if humidity is not None and temperature is not None:
            return {'temperature': temperature, 'humidity': humidity}
        else:
            # print('Failed to get DHT reading. Try again!')
            return False

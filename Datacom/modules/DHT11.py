import Adafruit_DHT


class DHT11:
    def __init__(self, sensor=Adafruit_DHT.DHT11, pin=16):
        self.sensor = sensor
        self.pin = pin

    def getData(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

        if humidity is not None and temperature is not None:
            return temperature, humidity
            #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')

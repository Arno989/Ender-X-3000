import Adafruit_DHT
import time

while True:

    humidity, temperature = Adafruit_DHT.read_retry(11, 5)

    print('Temp: {} C  Humidity: {} %'.format(temperature, humidity))
    time.sleep(2)
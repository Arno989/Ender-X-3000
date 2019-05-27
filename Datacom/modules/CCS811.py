from Adafruit_CCS811 import Adafruit_CCS811
from datetime import time
from time import sleep
import statistics


class CCS811:
    def __init__(self):
        pass

    def readSensor(self):
        ccs = Adafruit_CCS811()

        while not ccs.available():
            pass
        temp = ccs.calculateTemperature()
        ccs.tempOffset = temp - 25.0

        teller = 0
        co2 = []
        tvoc = []

        try:
            while teller < 150:
                if ccs.available():
                    if not ccs.readData():
                        print("CO2: ", ccs.geteCO2(), "ppm, TVOC: ", ccs.getTVOC())
                        if teller > 2:
                            co2.append(ccs.geteCO2())
                            tvoc.append(ccs.getTVOC())
                        else:
                            pass
                        teller += 1
                    else:
                        print("ERROR! {0}".format(time()))
                        while True:
                            pass
                sleep(1)
        except IOError as e:
            "I/O error({0}): {1}".format(e.errno, e.strerror)
            co2.append(1000)
            tvoc.append(1000)

        return [statistics.median(co2), statistics.median(tvoc)]

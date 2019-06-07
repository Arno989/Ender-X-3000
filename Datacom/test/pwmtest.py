from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

R = GPIO.PWM(16, 100)
G = GPIO.PWM(20, 100)
B = GPIO.PWM(21, 100)

R.start(100)
G.start(100)
B.start(100)

while True:
    sleep(1)
    red = input("red")
    green = input("green")
    blue = input("blue")
    R.ChangeDutyCycle(int(red))
    G.ChangeDutyCycle(int(green))
    B.ChangeDutyCycle(int(blue))





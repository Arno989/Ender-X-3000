from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)
# region Pins
RS = 20
E = 21
DB0 = 5
DB1 = 18
DB2 = 6
DB3 = 23
DB4 = 24
DB5 = 27
DB6 = 22
DB7 = 25


# endregion

class LCD():
    def __init__(self):
        self.rs = RS
        self.e = E
        self.db0 = DB0
        self.db1 = DB1
        self.db2 = DB2
        self.db3 = DB3
        self.db4 = DB4
        self.db5 = DB5
        self.db6 = DB6
        self.db7 = DB7

        # region SETUP PINS
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.e, GPIO.OUT)

        GPIO.setup(self.db0, GPIO.OUT)
        GPIO.setup(self.db1, GPIO.OUT)
        GPIO.setup(self.db2, GPIO.OUT)
        GPIO.setup(self.db3, GPIO.OUT)
        GPIO.setup(self.db4, GPIO.OUT)
        GPIO.setup(self.db5, GPIO.OUT)
        GPIO.setup(self.db6, GPIO.OUT)
        GPIO.setup(self.db7, GPIO.OUT)
        # endregion

    def stuur_instructie(self, byte=0x01):
        GPIO.output(self.e, GPIO.HIGH)
        GPIO.output(self.rs, GPIO.LOW)
        self.set_GPIO_bits(byte)
        time.sleep(0.005)
        GPIO.output(self.e, GPIO.LOW)

    def stuur_teken(self, char):
        bits = ord(char)
        GPIO.output(self.e, GPIO.HIGH)
        GPIO.output(self.rs, GPIO.HIGH)
        self.set_GPIO_bits(bits)
        time.sleep(0.005)
        GPIO.output(self.e, GPIO.LOW)

    def set_GPIO_bits(self, byte):
        list_db = [self.db0, self.db1, self.db2, self.db3, self.db4, self.db5, self.db6, self.db7]
        for i in range(0, 8):
            if (byte & (2 ** i)) == 0:
                GPIO.output(list_db[i], GPIO.LOW)
            else:
                GPIO.output(list_db[i], GPIO.HIGH)

'''
from time import sleep
from I2C import i2c

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001  # Register select bit


class lcd:
    def __init__(self):
        self.lcd_device = i2c(0x27, 1)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        sleep(0.2)

    def lcd_clear(self):
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_RETURNHOME)

    # clocks EN to latch command
    def lcd_strobe(self, data):
        self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
        sleep(.0005)
        self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        sleep(.0001)

    def lcd_write_four_bits(self, data):
        self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
        self.lcd_strobe(data)

    # write a command to lcd
    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_display_string(self, string, line=1, pos=0):
        if line == 1:
            pos_new = pos
        elif line == 2:
            pos_new = 0x40 + pos

        self.lcd_write(0x80 + pos_new)

        for char in string:
            self.lcd_write(ord(char), Rs)

    def lcd_load_custom_chars(self, fontdata):
        self.lcd_write(0x40)
        for char in fontdata:
            for line in char:
                self.lcd_write_char(line)

    def lcd_write_char(self, charvalue, mode=1):
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))
'''


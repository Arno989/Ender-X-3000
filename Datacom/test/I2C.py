import smbus
from time import sleep

bus = 1
lcd = 0x27
ccs = 0x5a

class i2c:
    def __init__(self, addr, port=bus):
        self.addr = addr
        self.bus = smbus.SMBus(port)

    # single command
    def write_cmd(self, cmd):
        self.bus.write_byte(self.addr, cmd)
        sleep(0.0001)

    # command and argument
    def write_cmd_arg(self, cmd, data):
        self.bus.write_byte_data(self.addr, cmd, data)
        sleep(0.0001)

    # block of data
    def write_block_data(self, cmd, data):
        self.bus.write_block_data(self.addr, cmd, data)
        sleep(0.0001)
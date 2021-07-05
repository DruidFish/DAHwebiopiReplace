"""
Python Library for PCF8574 io expander using Raspberry Pi 3 Model B+

Version for Edinburgh DAH course, replacing webiopi library

Took a few hints from https://github.com/flyte/pcf8574

"""

import smbus

class PCF8574:

  def __init__(self, address):

    self.bus = smbus.SMBus(1)
    self.address = address

  def portRead(self):

    return self.bus.read_byte(self.address)

  def portWrite(self, value):

    self.bus.write_byte(self.address, value)


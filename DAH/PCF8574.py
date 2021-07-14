"""
Python Library for PCF8574 io expander using Raspberry Pi 3 Model B+

Version for Edinburgh DAH course, replacing webiopi library

Using smbus approach from https://github.com/flyte/pcf8574

"""

import smbus

class PCF8574:

  def __init__(self, address):

    self.bus = smbus.SMBus(1)
    self.address = address

  def portRead(self):

    return self.bus.read_byte(self.address)

  def portWrite(self, value):

    if value < 0 or value > 255:
      raise ValueError('PCF8574 says: Invalid portWrite value (' + str(value) + ')! Options are 0-255')

    self.bus.write_byte(self.address, value)

  def digitalWrite(self, channel, value):

    if channel < 0 or channel > 7:
      raise ValueError('PCF8574 says: Invalid channel chosen (' + str(channel) +')! Options are 0-7')

    currentState = self.portRead()

    # Zero the relevant channel
    newState = currentState & ~( 1 << channel )

    # Set the channel high if requested
    if value:
      newState += ( 1 << channel )

    self.portWrite( newState )

  def digitalRead(self, channel):

    if channel < 0 or channel > 7:
      raise ValueError('PCF8574 says: Invalid channel chosen (' + str(channel) +')! Options are 0-7')

    currentState = self.portRead()

    # Mask all other channels
    channelState = currentState & ( 1 << channel )

    # Return a boolean
    return ( channelState > 0 )

"""
Python Library for PCF8574 io expander using Raspberry Pi 3 Model B+

Version for Edinburgh DAH course, replacing webiopi library

Using smbus approach from https://github.com/flyte/pcf8574

"""

import smbus

class PCF8574:

  def __init__(self, address=0x38):

    self.bus = smbus.SMBus(1)
    self.doPrint = False

    # 3 bits of address to work with, starting from 0x38
    if address < 0x38 or address > 0x3F:
      raise ValueError('PCF8574 says: Invalid address chosen ({:02X})! Options are 0x38-0x3F'.format(address))
    self.address = address

  def printRawData(self, value):

    self.doPrint = value

  def portRead(self):

    data = self.bus.read_byte(self.address)

    if self.doPrint:
      print( "from PCF8574: " + str( data ) )

    return data

  def portWrite(self, value):

    if value < 0 or value > 255:
      raise ValueError('PCF8574 says: Invalid portWrite value (' + str(value) + ')! Options are 0-255')

    if self.doPrint:
      print( "to PCF8574: " + str( value ) )

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

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

    self.bus.write_byte(self.address, value)


  def digitalWrite(self, pin, value):

    if pin < 0 or pin > 7:
      raise ValueError('PCF8574 says: Invalid pin chosen (' + str(pin) +')! Options are 0-7')

    currentState = self.portRead()

    # Zero the relevant pin
    newState = currentState & ~( 1 << pin )

    # Set the pin high if requested
    if value:
      newState += ( 1 << pin )

    self.portWrite( newState )


  def digitalRead(self, pin):

    if pin < 0 or pin > 7:
      raise ValueError('PCF8574 says: Invalid pin chosen (' + str(pin) +')! Options are 0-7')

    currentState = self.portRead()

    # Mask all other pins
    pinState = currentState & ( 1 << pin )

    # Return a boolean
    return ( pinState > 0 )

"""
Python Library for MCP23S17 io expander using Raspberry Pi 3 Model B+

Version for Edinburgh DAH course, replacing webiopi library

"""

import spidev
import RPi.GPIO as GPIO

class MCP23S17:

  def __init__(self, chip=0, address=0x20):

    # 3 bits of address to work with, starting from 0x20
    if address < 0x20 or address > 0x27:
      raise ValueError('MCP23S17 says: Invalid device ID chosen ({:02X})! Options are 0x20-0x27'.format(address))
    self.address = address
    self.printRawData = False

    # Use the spidev library for communication
    self.spi = spidev.SpiDev(0, 1)
    self.spi.max_speed_hz=10000000
    self.spi.mode = 0
    self.spi.lsbfirst = False
    #self.spi.cshigh = False

    # Use the GPIO library for chip select
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    if chip == 0:
      self.setCS( 8 )
    elif chip == 1:
      self.setCS( 7 )
    else:
      raise ValueError('MCP23S17 says: Invalid chip chosen (' + str(chip) + ')! Options are 0 or 1')

  def __del__(self):

    self.close()

  def setCS(self, cs):

    if cs < 0 or cs > 27:
      raise ValueError('MCP23S17 says: Invalid CS chosen (' + str(cs) + ')! Options are 0-27')

    self.cs = cs
    GPIO.setup(self.cs, GPIO.OUT)
    GPIO.output(self.cs, GPIO.HIGH)

  def printRawData(self, value):

    self.printRawData = value

  def digitalCount(self):

    return 16

  def rawIO(self, a, b, c):

    # Activate chip select
    GPIO.output(self.cs, GPIO.LOW)

    # Write command to MCP23S17, read its response
    data = self.spi.xfer2([a, b, c])

    # Deactivate chip select
    GPIO.output(self.cs, GPIO.HIGH)

    if self.printRawData:
      print( "to MCP23S17: " + str( [a, b, c] ) )
      print( "from MCP23S17: " + str( data ) )

    return data[2]

  def portReadA(self):

    return self.rawIO( (self.address << 1) + 1, 18, 0 )

  def portReadB(self):

    return self.rawIO( (self.address << 1) + 1, 19, 0 )

  def portRead(self):

    return ( self.portReadB() << 8 ) + self.portReadA()

  def digitalRead(self, channel):

    if channel < 0 or channel > 15:

      raise ValueError('MCP23S17 says: Invalid channel chosen (' + str(channel) + ')! Options are 0-15')

    elif channel < 8:

      return self.portReadA() & ( 1 << channel )

    else:

      return self.portReadB() & ( 1 << (channel-8) )

  def portWriteA(self, value):

    self.rawIO( (self.address << 1) + 0, 18, value )

  def portWriteB(self, value):

    self.rawIO( (self.address << 1) + 0, 19, value )

  def portWrite(self, value):

    self.portWriteA( value & 0xFF )
    self.portWriteB( ( value >> 8 ) & 0xFF )

  def digitalWrite(self, channel, value):

    if channel < 0 or channel > 15:

      raise ValueError('MCP23S17 says: Invalid channel chosen (' + str(channel) + ')! Options are 0-15')

    elif channel < 8:

      # Get current state
      currentState = self.portReadA()

      # Zero the relevant channel
      newState = currentState & ~( 1 << channel )

      # Set the channel high if requested
      if value:
        newState += ( 1 << channel )

      self.portWriteA( newState )

    else:

      # Get current state
      currentState = self.portReadB()

      # Zero the relevant channel
      newState = currentState & ~( 1 << (channel-8) )

      # Set the channel high if requested
      if value:
        newState += ( 1 << (channel-8) )

      self.portWriteA( newState )

  def getModeA(self):

    return self.rawIO( (self.address << 1) + 1, 0, 0 )

  def getModeB(self):

    return self.rawIO( (self.address << 1) + 1, 1, 0 )

  def setModeA(self, value):

    self.rawIO( (self.address << 1) + 0, 0, value )

  def setModeB(self, value):

    self.rawIO( (self.address << 1) + 0, 1, value )

  def setMode(self, channel, value):

    if channel < 0 or channel > 15:

      raise ValueError('MCP23S17 says: Invalid channel chosen (' + str(channel) + ')! Options are 0-15')

    elif channel < 8:

      # Get current state
      currentState = self.getModeA()

      # Zero the relevant channel
      newState = currentState & ~( 1 << channel )

      # Set the channel high if requested
      if value:
        newState += ( 1 << channel )

      self.setModeA( newState )

    else:

      # Get current state
      currentState = self.getModeB()

      # Zero the relevant channel
      newState = currentState & ~( 1 << (channel-8) )

      # Set the channel high if requested
      if value:
        newState += ( 1 << (channel-8) )

      self.setModeB( newState )

  def setInput(self, channel):

    self.setMode(channel, 1)

  def setOutput(self, channel):

    self.setMode(channel, 0)

  def close(self):

    self.spi.close()


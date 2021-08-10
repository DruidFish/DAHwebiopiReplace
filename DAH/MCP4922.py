"""
Python Library for MCP4922 DAC using Raspberry Pi 3 Model B+

Version for Edinburgh DAH course, replacing webiopi library

Based on https://github.com/mrwunderbar666/Python-RPi-MCP4922

"""

import spidev
import RPi.GPIO as GPIO

class MCP4922:

  def __init__(self, chip=1, vref=3.3):

    # Reference voltage
    self.vref = vref

    # Use the spidev library for communication
    self.spi = spidev.SpiDev(0, 1)
    self.spi.max_speed_hz=1000000
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
      raise ValueError('MCP4922 says: Invalid chip chosen (' + str(chip) + ')! Options are 0 or 1')

  def __del__(self):

    self.shutdown(0)
    self.shutdown(1)
    self.close()

  def setCS(self, cs):

    if cs < 0 or cs > 27:
      raise ValueError('MCP4922 says: Invalid CS chosen (' + str(cs) + ')! Options are 0-27')

    self.cs = cs
    GPIO.setup(self.cs, GPIO.OUT)
    GPIO.output(self.cs, GPIO.HIGH)

  def analogCount(self):

    return 2

  def analogResolution(self):

    return 12

  def analogMaximum(self):

    return 4095

  def analogReference(self):

    return self.vref

  def analogWrite(self, channel, value):

    if channel == 0:
      output = 0x3000
    elif channel == 1:
      output = 0xb000
    else:
      raise ValueError('MCP4922 says: Invalid channel chosen (' + str(channel) + ')! Options are 0 or 1')

    if value > 4095:
      value = 4095
    if value < 0:
      value = 0

    output |= value
    buf0 = (output >> 8) & 0xff
    buf1 = output & 0xff

    # Activate chip select
    GPIO.output(self.cs, GPIO.LOW)

    # Write command to MCP4922
    self.spi.writebytes([buf0, buf1])

    # Deactivate chip select
    GPIO.output(self.cs, GPIO.HIGH)

  def analogWriteFloat(self, channel, value):

    self.analogWrite( channel, int( value * float( self.analogMaximum() ) ) )

  def analogWriteVolt(self, channel, value):

    self.analogWriteFloat( channel, value / self.analogReference() )

  def shutdown(self, channel):

    if channel == 0:
      output = 0x2000
    elif channel == 1:
      output = 0xA000
    else:
      raise ValueError('MCP4922 says: Invalid channel chosen (' + str(channel) + ')! Options are 0 or 1')

    buf0 = (output >> 8) & 0xff
    buf1 = output & 0xff

    # Activate chip select
    GPIO.output(self.cs, GPIO.LOW)

    # Write command to MCP4922
    self.spi.writebytes([buf0, buf1])

    # Deactivate chip select
    GPIO.output(self.cs, GPIO.HIGH)

  def close(self):

    self.spi.close()


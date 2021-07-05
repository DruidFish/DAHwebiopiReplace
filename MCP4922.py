"""
Python Library for MCP4922 DAC using Raspberry Pi 3 Model B+

Version for Edinburgh DAH course, replacing webiopi library

Based on https://github.com/mrwunderbar666/Python-RPi-MCP4922

"""

import spidev
import RPi.GPIO as GPIO

class MCP4922(object):

  def __init__(self, chip=1):

    # Use the spidev library for communication
    self.spi = spidev.SpiDev(0, 1)
    self.spi.max_speed_hz=1000000
    self.spi.mode = 0
    self.spi.lsbfirst = False
    #self.spi.cshigh = False

    # Use the GPIO library for chip select
    if chip == 0:
      self.cs = 8
    elif chip == 1:
      self.cs = 7
    else:
      raise ValueError('MCP4922 says: Invalid CS chosen (' + str(chip) + '! Options are 0 or 1')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.cs, GPIO.OUT)
    GPIO.output(self.cs, 1)

  def __del__(self):

    shutdown(0)
    shutdown(1)
    close()



  def analogWrite(self, channel, value):

    if channel == 0:
      output = 0x3000
    elif channel == 1:
      output = 0xb000
    else:
      raise ValueError('MCP4922 says: Invalid channel chosen (' + str(channel) + '! Options are 0 or 1')

    if value > 4095:
      value = 4095
    if value < 0:
      value = 0

    output |= value
    buf0 = (output >> 8) & 0xff
    buf1 = output & 0xff

    # Activate chip select
    GPIO.output(self.cs, 0)

    # Write command to MCP4922
    self.spi.writebytes([buf0, buf1])

    # Deactivate chip select
    GPIO.output(self.cs, 1)

  def shutdown(self, channel):

    if channel == 0:
      output = 0x2000
    elif channel == 1:
      output = 0xA000
    else:
      raise ValueError('MCP4922 says: Wrong Channel Selected! Chose either 0 or 1!')

    buf0 = (output >> 8) & 0xff
    buf1 = output & 0xff

    # Activate chip select
    GPIO.output(self.cs, 0)

    # Write command to MCP4922
    self.spi.writebytes([buf0, buf1])

    # Deactivate chip select
    GPIO.output(self.cs, 1)

  def close(self):
    self.spi.close


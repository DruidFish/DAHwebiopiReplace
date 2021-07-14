"""
Python Library for MCP3208 ADC using Raspberry Pi 3 Model B+

Version for Edinburgh DAH course, replacing webiopi library

Based on https://github.com/MomsFriendlyRobotCompany/mcp3208

"""

import spidev
import RPi.GPIO as GPIO

class MCP3208:

  def __init__(self, chip=0, vref=3.3):

    # Reference voltage
    self.vref = vref

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
      raise ValueError('MCP3208 says: Invalid chip chosen (' + str(chip) + ')! Options are 0 or 1')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.cs, GPIO.OUT)
    GPIO.output(self.cs, 1)

  def __del__(self):

    self.close()

  def setCS(self, cs):

    if cs < 0 or cs > 27:
      raise ValueError('MCP3208 says: Invalid CS chosen (' + str(cs) + ')! Options are 0-27')

    self.cs = cs
    GPIO.setup(self.cs, GPIO.OUT)
    GPIO.output(self.cs, 1)

  def analogCount(self):

    return 8

  def analogResolution(self):

    return 12

  def analogMaximum(self):

    return 4095

  def analogReference(self):

    return self.vref

  def analogRead(self, channel):

    if channel > 7 or channel < 0:
      raise ValueError('MCP3208 says: Invalid channel chosen (' + str(channel) +')! Options are 0-7')

    cmd = 128  # 1000 0000
    cmd += 64  # 1100 0000
    cmd += ((channel & 0x07) << 3)

    # Activate chip select
    GPIO.output(self.cs, 0)

    # Write command to MCP3208, read its response
    ret = self.spi.xfer2([cmd, 0x0, 0x0])

    # Deactivate chip select
    GPIO.output(self.cs, 1)

    # get the 12b out of the return
    val = (ret[0] & 0x01) << 11  # only B11 is here
    val |= ret[1] << 3           # B10:B3
    val |= ret[2] >> 5           # MSB has B2:B0 ... need to move down to LSB

    return (val & 0x0FFF)  # ensure we are only sending 12b

  def analogReadFloat(self, channel):

    return float( self.analogRead( channel ) ) / float( self.analogMaximum() )

  def analogReadVolt(self, channel):

    return self.vref * self.analogReadFloat( channel )

  def analogReadAll(self):

    result = [0]*8
    for channel in range( self.analogCount() ):
      result[ channel ] = analogRead( channel )

    return result

  def analogReadAllFloat(self):

    result = [0]*8
    for channel in range( self.analogCount() ):
      result[ channel ] = analogReadFloat( channel )

    return result

  def analogReadAllVolt(self):

    result = [0]*8
    for channel in range( self.analogCount() ):
      result[ channel ] = analogReadVolt( channel )

    return result

  def close(self):

    self.spi.close()


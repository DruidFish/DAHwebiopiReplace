"""
Python Library for DS18B20 temperature sensor using Raspberry Pi 3 Model B+

Version for Edinburgh DAH course, replacing webiopi library

"""

import os.path

class DS18B20:

  def __init__(self, address):

    self.path = os.path.join( "/sys/bus/w1/devices", address, "w1_slave" )

    if not os.path.exists( self.path ):
      raise FileNotFoundError( "DS18B20 says: could not find sensor with address " + str(address) )


  def getCelsius(self):

    # Load the raw temperature data
    inputFile = open( self.path, "r" )

    # The file is two lines long, and we only care about the last one
    inputFile.readline()
    inputData = inputFile.readline()

    # The last 5 characters of the line contain the temperature information
    inputData = inputData[ len( inputData ) - 6 : ]

    # Convert the temperature information to a number (with correct magnitude)
    inputTemperature = float( inputData ) / 1000.0

    inputFile.close()
    return inputTemperature

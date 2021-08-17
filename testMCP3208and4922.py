from DAH import MCP3208, MCP4922
import time

# Define ADC on Chip Enable 0 (CE0/GPIO8)
ADC0 = MCP3208(chip=0, vref=3.3)

# Define DAC on Chip Enable 1 (CE1/GPIO7)
DAC1 = MCP4922(chip=1, vref=3.3)

# Set single DAC channel, read single ADC channel
for i in range(1, 10):
  DAC1.analogWriteVolt(0, 0.3*float(i))
  print( "DAC out: " + str( 0.3*float(i) ) + " ADC in: " + str( ADC0.analogReadVolt(0) ) )
  time.sleep(1.0)

# Set all DAC channels, read all ADC channels
for i in range(1, 10):
  DAC1.analogWriteVolt(0, 0.3*float(i))
  DAC1.analogWriteVolt(1, 3.0 - 0.3*float(i))
  print( "DAC out: " + str( 0.3*float(i) ) + " ADC in: " + str( ADC0.analogReadAllVolt() ) )
  time.sleep(1.0)

# Turn off
DAC1.shutdown(0)
DAC1.shutdown(1)


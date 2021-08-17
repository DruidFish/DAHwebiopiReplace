from DAH import DS18B20
import time

# Define temperature sensors
tmp0 = DS18B20(address="10-000802cb2f2c")
tmp1 = DS18B20(address="10-000802dec1d3")

# Read out temperatures
for i in range(1, 10):
  print( "Tmp0: " + str( tmp0.getCelsius() ) + ", Tmp1: " + str( tmp1.getCelsius() ) )
  #time.sleep(1.0) #readout slow anyway

from DAH import PCF8574
import time

pcf = PCF8574( address=0x38 )

# Read all pins 20 times, allowing you to make changes see output
for sample in range( 20 ):
  print( pcf.portRead() )
  time.sleep( 0.5 )

# Flash all pins
for flash in range( 10 ):
  pcf.portWrite( 0xFF )
  time.sleep( 0.5 )
  pcf.portWrite( 0x00 )
  time.sleep( 0.5 )

# Light each pin in sequence
for pin in range( 0, 8 ):
  pcf.digitalWrite( pin, 1 )
  time.sleep( 0.5 )

# Turn off pins
pcf.portWrite( 0x00 )

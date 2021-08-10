from DAH import MCP23S17
import time

mcp = MCP23S17( chip=0, address=0x20 )

# Set all pins to input
for pin in range( 0, 16 ):
  mcp.setInput( pin )

# Read all pins 20 times, allowing you to make changes see output
for sample in range( 20 ):
  print( mcp.portRead() )
  time.sleep( 0.5 )

# Set every even pin to output - effectively a mask for the next step
for pin in range( 0, 16, 2 ):
  mcp.setOutput( pin )

# Flash all pins, but only the even ones should respond
for flash in range( 10 ):
  mcp.portWrite( 0xFFFF )
  time.sleep( 0.5 )
  mcp.portWrite( 0x0000 )
  time.sleep( 0.5 )

# Set all pins to output, light each one in sequence
for pin in range( 0, 16 ):
  mcp.setOutput( pin )
  mcp.digitalWrite( pin, 1 )
  time.sleep( 0.5 )

# Turn off pins
mcp.portWrite( 0x0000 )

import smbus

class PCF8574:

  def __init__(self, address):

    self.bus = smbus.SMBus(1)
    self.address = address

  def portRead(self):

    return self.bus.read_byte(self.address)

  def portWrite(self, value):

    self.bus.write_byte(self.address, value)

  def port(self, value):
      # type: (List[bool]) -> None
      """
      Set the whole port using a list.
      """
      assert len(value) == 8
      new_state = 0
      for i, val in enumerate(value):
          if val:
              new_state |= 1 << 7 - i
      self.bus.write_byte(self.address, new_state)

  def set_output(self, output_number, value):
      # type: (int, bool) -> None
      """
      Set a specific output high (True) or low (False).
      """
      assert output_number in range(
          8
      ), "Output number must be an integer between 0 and 7"
      current_state = self.bus.read_byte(self.address)
      bit = 1 << 7 - output_number
      new_state = current_state | bit if value else current_state & (~bit & 0xFF)
      self.bus.write_byte(self.address, new_state)

  def get_pin_state(self, pin_number):
      # type: (int) -> bool
      """
      Get the boolean state of an individual pin.
      """
      assert pin_number in range(8), "Pin number must be an integer between 0 and 7"
      state = self.bus.read_byte(self.address)
      return bool(state & 1 << 7 - pin_number)


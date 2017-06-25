# small test to ensure forward movement on detection of green color by rgb sensor

from a_star import AStar
import Adafruit_TCS34725
import smbus

a_star = AStar()
tcs = Adafruit_TCS34725.TCS34725()


tcs.set_interrupt(False)
r, g, b, c = tcs.get_raw_data()

while (g > r and g > b):
  print('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))
  a_star.motors(int(100), int(100))
  r, g, b, c = tcs.get_raw_data()

# Enable interrupts and put the chip back to low power sleep/disabled.
tcs.set_interrupt(True)
tcs.disable()

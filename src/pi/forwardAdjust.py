# small test to ensure forward movement on detection of green color by rgb sensor

from a_star import AStar
import Adafruit_TCS34725
import smbus
import time

main()
  
def main():
  a_star = AStar()
  tcs = Adafruit_TCS34725.TCS34725()
  tcs.set_interrupt(False)
  
  #initial state of green
   if (g > r and g > b):
      a_star.motors(100, 100)

  while (True): 
    r, g, b, c = tcs.get_raw_data()
    while(g < r or g < b):
      adjustTime = time.time()
      a_star.motors(50, 100)
      while((time.time() - adjustTime) < 0.5):
        pass 
      r, g, b, c = tcs.get_raw_data()
      if(g > r and g > b): 
        break
      adjustTime = time.time()
      a_star.motors(100, 50)
      while((time.time() - adjustTime) < 1):
        pass
      a_star.motors(100, 100)
  
  # Enable interrupts and put the chip back to low power sleep/disabled.
  tcs.set_interrupt(True)
  tcs.disable()

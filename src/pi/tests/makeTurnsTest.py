# test of the turn() method of the Robot class
# must check visually whether the robot turns correctly
# robot should be facing original direction
from romi import *
import time

def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()
  romi.turn('left')
  romi.turn('right')
  romi.turn('forward')
  romi.turn('backward')
  romi.turn('backward')
  romi.stop()
  romi.turnOnInterruptsRGB()
  romi.disableRGB()  
#end main
    
if __name__ == "__main__": main()   

# simple test that utilizes the romi class
# move forward on green until lost
from romi import *
import time
def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()
  initTime = time.clock()

  while(True):
    if(romi.checkGreen()):
      romi.goForwardtwo()
    else:
      romi.calibrateDirection()
  
  '''
  while(True):
    while(romi.checkGreen()):
      romi.goForwardtwo()

    if(romi.checkRed()):
      romi.adjustIntersection()
      
    romi.calibrateDirection()

    if(time.clock() - initTime > 10):
      break
  
  romi.stop()
  '''
  
  '''
  while(romi.checkGreen()):
    romi.goForward()
    romi.printColorInfo()
    
  romi.stop()
  

  romi.turn90Left()
  time.sleep(2)
  romi.turn90Right()
  time.sleep(2)
  romi.goForward()
  time.sleep(3)
  romi.stop()
  time.sleep(2)
  romi.turn90Left()
  romi.turn90Left()
  time.sleep(3)
  romi.goForward()
  time.sleep(2)
  romi.stop()
  ''' 
  romi.turnOnInterruptsRGB()
  romi.disableRGB()
#end main
    
if __name__ == "__main__": main()


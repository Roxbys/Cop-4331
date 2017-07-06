#simple test that utilizes the romi class
# move forward on green until lost
from romi import *

def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()
  '''
  while(True):
    if(romi.checkGreen()):
      romi.goForward()
    else:
      romi.calibrate()
  romi.stop()
  '''
  '''
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

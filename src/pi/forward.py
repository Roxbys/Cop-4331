# simple test that utilizes the romi class
# move forward on green until lost
from romi import *

def main():
    romi = Robot()
    romi.turnOffInterruptsRGB()
    
    while(not romi.isLost):
      if(romi.isGreen):
        pass
      elif(romi.checkGreen()):
        romi.goForward()
      else:
        romi.calibrateDirection()
        if(romi.isGreen):
          romi.goForward()
    # end while
        
    if(romi.isLost):
        romi.giveUp()
      
    romi.turnOnInterruptsRGB()
    romi.disableRGB()
#end main
    
if __name__ == "__main__": main()

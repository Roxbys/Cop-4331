# simple test that utilizes the romi class
# move forward on green until lost

from romi import *

def main():
    romi = Robot()
    romi.tcs.set_interrupt(False)
    
    while(not romi.isLost):
      if(romi.isGreen):
        pass
      elif(romi.checkGreen()):
        romi.goForward()
      else:
        romi.calibrateDirection()
        if(romi.isGreen):
          romi.goForward()
        
    if(romi.isLost):
        romi.giveUp()
      
    romi.tcs.set_interrupt(True)
    romi.tcs.disable()

if __name__ == "__main__": main()

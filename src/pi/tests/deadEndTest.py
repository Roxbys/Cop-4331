# test of the getPaths() method of the Robot class

from romi import *
import time

def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()
  retval = False
  while(romi.checkGreen()):
    romi.goForwardtwo
  if(romi.checkRed()):
    romi.adjustIntersection()
    paths = romi.getPaths
    if(not paths):
      retval = True
  romi.stop()
  romi.turnOnInterruptsRGB()
  romi.disableRGB()  
#end main
    
if __name__ == "__main__": main()   

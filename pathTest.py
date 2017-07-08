# simple test that utilizes the romi class
# move forward on green until lost
from romi import *
import time
def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()

  flag = False
  
  while(True):
    if(flag):
      print(romi.readEncoders())
    if(romi.checkGreen() == True):
      romi.goForwardtwo()
      if(flag):
        romi.printColorInfo()
    elif(romi.checkRed() == True):
      print("found red, stopping")
      romi.stop()
      time.sleep(1)
      romi.adjustIntersection()
      romi.stop()
      time.sleep(1)
      pathTuple = romi.getValidPaths()
      print(pathTuple)
      if(pathTuple[0]):
        print("made a left")
        romi.turn90Left()
        flag = True
        time.sleep(3)
      elif(romi.noValidPaths(pathTuple)):
        print("at dead end")
        romi.turn90Left()
        romi.turn90Left()
        romi.sweepsForGreen(150)
    else:
      romi.calibrateTwo()
  
  '''
  for i in range (0, 10):
    romi.printColorInfo()
    time.sleep(1)
  '''  
  romi.stop()
  romi.turnOnInterruptsRGB()
  romi.disableRGB()

  
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
  
#end main
    
if __name__ == "__main__": main()


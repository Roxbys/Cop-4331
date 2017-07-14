# simple test that utilizes the romi class
# move forward on green until lost
from romi import *
import time

romi = Robot()
romi.turnOffInterruptsRGB()

def main():


  #romi.calibrateColors()
  if(romi.completeMaze()):
    print("Holy shit! You found the end!")

  '''
  while(True):
  
    if(romi.checkGreen()):
      romi.goForward()
    elif(romi.checkRed()):
      print('found red')
      romi.stop()
      time.sleep(1)
      romi.adjustIntersection()
      #romi.reset()
      pathInfo = romi.getValidPaths()
      #romi.reset()
      if len(pathInfo) == 1:
         print("deadend")
         romi.turnCounts('left', pathInfo[0][1])
         romi.calibrateTwo()
      else:
        romi.turnCounts('left', 744)
        romi.stop()
        time.sleep(1)
    else:
      romi.calibrateTwo()
    romi.reset()
    '''
  romi.stop()
  romi.turnOnInterruptsRGB()
  romi.disableRGB()
  '''
  def backTracking():
    print('found red')
    romi.stop()
    time.sleep(1)
    romi.adjustIntersection()
    pathInfo = romi.getValidPaths()
    if not pathInfo:
      romi.turnCounts('left', 3000)
      romi.calibrateTwo()
    else:
      for i in range (0, if (len(pathInfo) > 0) then len(pathInfo) - 1 else 0):
        counts = [y for (x, y) in pathInfo if x == i]
        if not counts:
          print("no path in direction" + str(i))
        else:
          romi.turnCounts('left', 744)
          romi.calibrateTwo()
          main()
   
    '''
      
#end main
    
if __name__ == "__main__": main()   




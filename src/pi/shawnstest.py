# simple test that utilizes the romi class
# move forward on green until lost
from romi import *
from goforwardtwo import *
import time

romi = Robot()
hey = goForward()
romi.turnOffInterruptsRGB()

def main():
  
  romi.turn90Right()
  romi.turn90Right()
  hey.reset_encoders()
  print(romi.grabdifference())
  romi.stop()
  time.sleep(5)
  print ("jhviugviytcuyrdytestrwareqa")
  endtime = time.time() + 2
  while(time.time() < endtime):
    # if(romi.checkGreen()):
      hey.goForwardtwo()
    # elif(romi.checkRed()):
    #   print('found red')
    #   romi.stop()
    #   time.sleep(1)
    #   romi.adjustIntersection()
    #   pathInfo = romi.getValidPaths()
    #   if not pathInfo:
    #      print("deadend")
    #      romi.turnCounts('left', 3000)
    #      romi.calibrateTwo()
    #   else:
    #     romi.turnCounts('left', 744)
    #     romi.stop()
    #     time.sleep(1)
    # else:
    #   romi.calibrateTwo()
      
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
    for i in range (0, if len(pathInfo) > 0 then len(pathInfo) - 1 else 0):
      counts = [y for (x, y) in pathInfo if x == i]
      if not counts:
        print("no path in direction" + str(i))
      else:
        romi.turnCounts('left', 744)
        romi.calibrateTwo()
        main()
''' 

  # for i in range (0, 10):
  #   romi.printColorInfo()
  #   time.sleep(1)

  
  
#end main
    
if __name__ == "__main__": main()


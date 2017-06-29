# small test to ensure forward movement on detection of green color by rgb sensor
from a_star import AStar
import Adafruit_TCS34725
import smbus
import time

# recalibrate the robot onto the path
def calibrateDirection(a_star, tcs, mode, searchTime, turnWheelSpeed):
  adjustTime = time.time()
  # search left
  if(mode == 0):
    a_star.motors(turnWheelSpeed, 100)
  # search right
  elif(mode == 1):
    a_star.motors(100, turnWheelSpeed)
  while((time.time() - adjustTime) < searchTime):
    if(checkIfGreen(tcs)):
      break
  # end while 
# end calibrateDirection()

def checkIfGreen(tcs):
  r, g, b, c = tcs.get_raw_data()
  return (g > r and g > b)
# end checkIfGreen()
 
def main():
  # create romi and rgb sensor objects
  a_star = AStar()
  tcs = Adafruit_TCS34725.TCS34725()
  tcs.set_interrupt(False)
 
  # initial states
  isGoingForward = False
  searchFailed = False
  # used to switch left/right search (left: 0, right: 1)
  toggleSearchDirection = 0 
 
  while (not searchFailed):
    isGreen = checkIfGreen(tcs)
    # if green is found and not already moving, move forward
    if (isGreen and (not isGoingForward)):
      a_star.motors(100, 100)
      isGoingForward = True
    # unnecessary to update motor speed if already going forward
    elif(isGreen and isGoingForward):
      pass
    # green not found, start search
    else:
      isGoingFoward = False
      # default search time for initial stray
      searchTime = .2 
      while(not isGreen):
        calibrateDirection(a_star, toggleSearchDirection, searchTime, 40)
        toggleSearchDirection = toggleSearchDirection ^ 1
        isGreen = checkIfGreen(tcs)
        # don't allow an oscillation to exceed 5 seconds
        if(searchTime > 5 and (not isGreen)):
          searchFailed = True
          break
        else:
          # double search time on opposite side
          searchTime *= 2
      # end while
  # end while
  
  # Enable interrupts and put the chip back to low power sleep/disabled.
  tcs.set_interrupt(True)
  tcs.disable()
#end main()

if __name__ == "__main__": main()

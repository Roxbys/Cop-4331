from a_star import AStar
import Adafruit_TCS34725
import smbus
import time

class Robot:
  def __init__(self):
    self.isLost = False
    self.nextSearchDirection = 0  # (left: 0, right: 1)
    self.veerSpeed = 50
    self.maxSpeed = 100
    self.a_star = AStar()
    self.tcs = Adafruit_TCS34725.TCS34725()
    
  def isGreen(self):
    r, g, b, c = self.tcs.get_raw_data()
    return (g > r and g > b)
  
  def motors(self, lspeed, rspeed):
    self.a_star.motors(lspeed, rspeed)
    
  def goForward(self):
    self.motors(self.maxSpeed, self.maxSpeed)
    
  def veerLeft(self):
    self.motors(self.veerSpeed, self.maxSpeed)
    
  def veerRight(self):
    self.motors(self.maxSpeed, self.veerSpeed)
  
  def getTime(self):
    return time.time()
   
  # recalibrate the robot onto the path
  def calibrateDirection(self):
    maxTurnTime = 0.2
    maxSearchTime = 5 
    totalSearchTime = self.getTime()
    calibrated = False
    
    while(not calibrated):
      if((self.getTime() - totalSearchTime) >= maxSearchTime):
        self.isLost = True
        break
      turnTime = self.getTime()
      # turn the robot one direction 
      if (self.nextSearchDirection == 0):
        self.veerLeft()
      else:
        self.veerRight()
      # switch turn direction for next iteration 
      self.nextSearchDirection = self.nextSearchDirection ^ 1 
      # wait to see if direction was correct  
      while((self.getTime() - turnTime) < maxTurnTime):
        if(self.isGreen()):
          calibrated = True
          break
      # end while
      maxTurnTime *= 2  # double max search time for next direction 
    # end while
    self.goForward()
  # end calibrateDirection()
# end Class Robot()
 
    
def main():
    romi = Robot()
    romi.tcs.set_interrupt(True)
    
    while(not romi.isLost):
      if(romi.isGreen):
        romi.goForward()
      else:
        romi.calibrateDirection()
    
    romi.tcs.set_interrupt(True)
    romi.tcs.disable()

if __name__ == "__main__": main()

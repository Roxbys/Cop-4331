from a_star import AStar
import Adafruit_TCS34725
import smbus
import time

class Robot:
  def __init__(self):
    self.isLost = False
    self.isGreen = False
    self.nextSearchDirection = 0  # (left: 0, right: 1)
    self.veerSpeed = 50
    self.maxSpeed = 100
    self.aStar = AStar()
    self.tcs = Adafruit_TCS34725.TCS34725()
    
  # check if currently reading green tape  
  def checkGreen(self):
    r, g, b, c = self.tcs.get_raw_data()
    self.isGreen = (g > r and g > b)
    return self.isGreen
  
  # set motor speeds
  def motors(self, lspeed, rspeed):
    self.aStar.motors(lspeed, rspeed)
  
  def goForward(self):
    self.motors(self.maxSpeed, self.maxSpeed)

  def stop(self):
    self.motors(0, 0)
    
  def veerLeft(self):
    self.motors(self.veerSpeed, self.maxSpeed)
    
  def veerRight(self):
    self.motors(self.maxSpeed, self.veerSpeed)
  
  def getTime(self):
    return time.time()
  
  def playNotes(self):
    self.aStar.play_notes("o4l16ceg>c8")
  
  # turn leds on or off
  def leds(self, red, yellow, green):
    self.aStar.leds(red, yellow, green)
    
  def blinkRed(self):
    time = self.getTime()
    status = 1
    while(self.getTime() - time < 5)
      self.leds(status, 0, 0)
      status = status ^ 1
      time.sleep(.5)
    # end while
    
  def giveUp(self):
    self.playNotes()
    self.motors(self.maxSpeed, self.maxSpeed * (-1))
    self.blinkRed()
    self.stop()
    
  def readAnalog(self):
    return self.aStar.read_analog()
  
  def readBatteryMillivolts(self):
    return self.aStar.read_battery_millivolts()
  
  def readButtons(self):
    return self.aStar.read_buttons()
    
  def readEncoders(self):
    return self.aStar.read_encoders()
  
  def printColorInfo(self):
    r, g, b, c = self.tcs.get_raw_data()
    temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)
    lux = Adafruit_TCS34725.calculate_lux(r, g, b)
    print('Color: r={0} g={1} b={2} temp={3} lux={4}'.format(r, g, b, temp, lux))
    
  def turnOffInterruptsRGB(self):
    self.tcs.set_interrupt(False)
  
  def turnOnInterruptsRGB(self):
    self.tcs.set_interrupt(True)
  
  # rgb sensor is enabled by default in the constructor method
  def enableRGB(self):
    self.tcs.enable()
    
  def disableRGB(self):
    self.tcs.disable()
   
  # recalibrate the robot onto the path
  def calibrateDirection(self):
    maxTurnTime = 0.2
    maxSearchTime = 5 
    totalSearchTime = self.getTime()
    calibrated = False
    
    while(not calibrated):
      if(self.getTime() - totalSearchTime >= maxSearchTime):
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
      while(self.getTime() - turnTime < maxTurnTime):
        if(self.checkGreen()):
          calibrated = True
          break
      # end while
      maxTurnTime *= 2  # double max search time for next direction 
    # end while
  # end calibrateDirection()    
# end Class Robot()

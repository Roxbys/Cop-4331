from a_star import AStar
import Adafruit_TCS34725
import smbus
import time

class Robot:
  def __init__(self):
    self.isLost = False
    self.nextSearchDirection = 0  # (left: 0, right: 1)
    self.veerSpeed = 40
    self.maxSpeed = 200
    self.aStar = AStar()
    self.tcs = Adafruit_TCS34725.TCS34725()
    self.initialLeftCount = self.aStar.read_encoders()[0]
    self.initialRightCount = self.aStar.read_encoders()[1]
  
  # check if currently reading green tape  
  def checkGreen(self):
    r, g, b, c = self.tcs.get_raw_data()
    return (g > r and g > b)
  
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
    
  def readAnalog(self):
    return self.aStar.read_analog()
  
  def readBatteryMillivolts(self):
    return self.aStar.read_battery_millivolts()
  
  def readButtons(self):
    return self.aStar.read_buttons()
    
  def readEncoders(self):
    encoders = self.aStar.read_encoders()
    return (encoders[0] - self.initialLeftCount, encoders[1] - self.initialRightCount)
  
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

  def turn90Left(self):
    initEncoders = self.readEncoders()
    while(    self.readEncoders()[0] > initEncoders[0] - 744
          and self.readEncoders()[1] < initEncoders[1] + 744):
      self.motors(self.maxSpeed * (-1), self.maxSpeed)
    self.stop()

  def turn90Right(self):
    initEncoders = self.readEncoders()
    while(    self.readEncoders()[1] > initEncoders[1] - 744
          and self.readEncoders()[0] < initEncoders[0] + 744):
      self.motors(self.maxSpeed, self.maxSpeed * (-1))
    self.stop()
  
  def goForward(self):
    self.motors(self.maxSpeed, self.maxSpeed)
    x = self.maxSpeed
    if(self.readEncoders()[1] > self.readEncoders()[0])
      while(self.readEncoders()[1]>self.readEncoders()[0])
        self.motors(x--,self.maxSpeed)
        self.sleep(.01)
      x = self.maxSpeed
      while(self.readEncoders()[1]>self.readEncoders()[0])
        self.motors(self.maxSpeed,x--)
        time.sleep(.01)

  def calibrate(self):
    while(self.checkGreen() == False):
      for x in range(100, -20, -1):
        self.motors(100 if x+40>100 else x+40,x)
      
      
  # recalibrate the robot onto the path
  def calibrateDirection(self):
    calibrated = False
    turnAmount = 200 # initial encoder count
    
    while(self.checkGreen() == False):
      # turn the robot one direction 
      if (self.nextSearchDirection == 0):
        self.veerLeft()
      else:
        self.veerRight()
      # switch turn direction for next iteration 
      self.nextSearchDirection = self.nextSearchDirection ^ 1 
      # wait to see if direction was correct  
      while(self.readEncoders()[self.nextSearchDirection] < turnAmount):
        if(self.checkGreen()):
          break
      # end while
      turnAmount *= 2  # double max search time for next direction 
    # end while
  # end calibrateDirection()

  
# end Class Robot()
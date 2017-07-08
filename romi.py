from a_star import AStar
import Adafruit_TCS34725
import smbus
import time
import math

class Robot:
  def __init__(self):
    self.isLost = False
    self.nextSearchDirection = 0  # (left: 0, right: 1)
    self.veerSpeed = 30
    self.maxSpeed = 70
    self.aStar = AStar()
    self.tcs = Adafruit_TCS34725.TCS34725()
    self.initialLeftCount = self.aStar.read_encoders()[0]
    self.initialRightCount = self.aStar.read_encoders()[1]
  
  # check if currently reading green tape  
  def checkGreen(self):
    r, g, b, c = self.tcs.get_raw_data()
    return (g > r and g > b)

  def checkRed(self):
    r, g, b, c = self.tcs.get_raw_data()
    return (r > 1.6*g or r > 1.6*b) and r > 50
  
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

  def turnLeft(self,count):
    while(self.readEncoders()[0]%744 > (-1)*count and self.readEncoders()[1]%744 < count):
      if(self.checkGreen()):
        return 1
        break
      self.motors(0, self.maxSpeed)
      self.stop()
      return 0

  def turnRight(self,count):
    while(self.readEncoders()[0]%744 < count and self.readEncoders()[1]%744 > (-1)*count):
      if(self.checkGreen()):
        return 1
        break
      self.motors(self.maxSpeed, 0)
      self.stop()
      return 0

  def changeCount(self,count):
    if(count != 0):
      count = count / 2
		
  def calibrate(self):
    count = 744
    while(self.checkGreen() == False):
      if(self.turnLeft(count)):
        pass
      elif(self.turnRight(count)):
        pass
      self.changeCount(count)
    # end while
    self.goForwardtwo()

  def greenIsLeft(self):
    initEncoders = self.readEncoders()
    while(    self.readEncoders()[0] > initEncoders[0] - 100
          and self.readEncoders()[1] < initEncoders[1] + 100
          and self.checkGreen() == False):
      self.motors(-50, 50)
    self.stop()
    if(self.checkGreen()):
      return True
    else:
      return False

  def greenIsRight(self):
    initEncoders = self.readEncoders()
    while(    self.readEncoders()[1] > initEncoders[1] - 100
          and self.readEncoders()[0] < initEncoders[0] + 100
          and self.checkGreen() == False):
      self.motors(50, -50)
    self.stop()
    if(self.checkGreen()):
      return True
    else:
      return False

  def adjustSlightly(self, direction):
    counts = 50
    initEncoders = self.readEncoders()
    if(direction == 'left'):
       while(self.readEncoders()[1] < initEncoders[1] + counts):
         self.motors(-50, 50)
    else:
      while(self.readEncoders()[0] < initEncoders[0] + counts):
         self.motors(50, -50)
         
  def calibrateTwo(self):
      self.stop()
      if(self.greenIsLeft()):
        self.adjustSlightly('left')
      elif(self.greenIsRight()):
        self.adjustSlightly('right')
      elif(self.checkRed()):
        pass
      else:
        print("Unable to find green")
  '''
  def calibrateTwo(self):
    self.sweepsForGreen(80)
  '''
    
    
  def turnCounts(self, direction, counts):
    initEncoders = self.readEncoders()
    if(direction == 'left'):
      while(    self.readEncoders()[0] > initEncoders[0] - counts
          and self.readEncoders()[1] < initEncoders[1] + counts):
        self.motors(self.maxSpeed * (-1), self.maxSpeed)
    elif(direction == 'right'):
      while(    self.readEncoders()[1] > initEncoders[1] - counts
          and self.readEncoders()[0] < initEncoders[0] + counts):
        self.motors(self.maxSpeed, self.maxSpeed * (-1))
    else:
      print("Invalid turn direction")
    self.stop()

  def turn90Left(self):
    self.turnCounts('left', 744)

  def turn90Right(self):
    self.turnCounts('right', 744)

  # return true is green is found within a sweep distance, false otherwise
  def sweepsForGreen(self, counts):
    # counts is equal to the number of encoders counts at both sides of
    # facing direction  e.g. count = 50 searches 50 counts left and 50 right
    interval = 10
    iterations = math.ceil(counts / interval)
    initEncoders = self.readEncoders()
    # sweep left
    for i in range (1, iterations):
      self.turnCounts('left', interval)
      if(self.checkGreen()):
        return True
    #print(self.readEncoders()[1] - initEncoders[1])
    #self.turnCounts('right', self.readEncoders()[1] - initEncoders[1])
    # sweep right
    for i in range (1, iterations):
      self.turnCounts('right', interval)
      if(self.checkGreen()):
        return True
    #print(self.readEncoders()[0] - initEncoders[0])
    #self.turnCounts('left', self.readEncoders()[0] - initEncoders[0])
    return False

  def isPathInDirection(self, direction):
    if(direction == 'forward'):
      pass
    elif(direction == 'left'):
      self.turn90Left()
    elif(direction == 'right'):
      self.turn90Right()
    return self.sweepsForGreen(120)

  def getValidPaths(self):
    forward = self.isPathInDirection('forward')
    self.stop()
    time.sleep(0.5)
    left = self.isPathInDirection('left')
    self.stop()
    time.sleep(0.5)
    self.turn90Right()
    right = self.isPathInDirection('right')
    self.stop()
    time.sleep(0.5)
    self.turn90Left()
    time.sleep(0.5)
    return (left, forward, right)

  def noValidPaths(pathTuple):
    return not (pathTuple[0] or pathTuple[1] or pathTuple[2])
 
  def goForwardtwo(self):
    self.motors(self.maxSpeed, self.maxSpeed)
    x = self.maxSpeed
    diff = math.fabs(self.readEncoders()[1] - self.readEncoders()[0]) 
    while(diff > 2):
      diff = math.fabs(self.readEncoders()[1] - self.readEncoders()[0]) 
      x-=1
      if(self.readEncoders()[1] > self.readEncoders()[0]):
        self.motors(self.maxSpeed,x)
        time.sleep(1.0/1000.0)
      elif(self.readEncoders()[0] > self.readEncoders()[1]):
        self.motors(x,self.maxSpeed)
        time.sleep(1.0/1000.0)
    self.motors(self.maxSpeed, self.maxSpeed)

  '''   
  def calibrate(self):
    while(self.checkGreen() == False):
      for x in range(100, -20, -1):
        self.motors(100 if x+40>100 else x+40,x)
      
  '''

  def adjustIntersection(self):
    saveEncoders = self.readEncoders()
    while(self.readEncoders()[0] - saveEncoders[0] < 700
          and self.readEncoders()[1] - saveEncoders[1] < 700):
      self.goForwardtwo()
    print("Centered at intersection")
      
  # recalibrate the robot onto the path
  def calibrateDirection(self):
    calibrated = False
    turnAmount = 500 # initial encoder count
    print("in calibrate")
    
    while(calibrated == False):
      # turn the robot one direction 
      if (self.nextSearchDirection == 0):
        self.veerLeft()
      else:
        self.veerRight()
      # switch turn direction for next iteration 
      self.nextSearchDirection = self.nextSearchDirection ^ 1
      print("in first while")
      recordEncoder = self.readEncoders()[self.nextSearchDirection]
      # wait to see if direction was correct  
      while(self.readEncoders()[self.nextSearchDirection] - recordEncoder < turnAmount):
        print("in second while")
        if(self.checkGreen()):
          # creep forward until centered
          self.adjustIntersection()
          print("done centering")
          # reposition front of robot onto green edge
          while(self.checkGreen() == False):
            if(self.nextSearchDirection == 0):
              print("repositioning [left] to green edge")
              self.veerLeft()
            else:
              print("repositioning [right] to green edge")
              self.veerRight()
          print("done repositioning to green edge")
          calibrated = True
          '''
          # rotate half an inch until sensor is centered on tape
          slapEncoders = self.readEncoders()
          if(self.nextSearchDirection == 0):
            while(self.readEncoders()[1] - slapEncoders[1] < 81):
              print("rotating left half an inch")
              self.motors(-100, 100)
            self.stop()
          else:
            while(self.readEncoders()[0] - slapEncoders[0] < 81):
              print("rotating right half an inch")
              self.motors(100, -100)
            self.stop()
          '''
          break
        else:
          pass  # not green, continue to veer
      # end while
  # end calibrateDirection()
  
# end Class Robot()

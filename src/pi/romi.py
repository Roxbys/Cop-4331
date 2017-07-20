from a_star import AStar
import Adafruit_TCS34725
import smbus
import time
import math

class Robot:
  # initialize robot
  def __init__(self):
    self.directionFacing = 'north'
    self.maxSpeed = 100
    self.aStar = AStar()
    self.tcs = Adafruit_TCS34725.TCS34725()
    self.initialLeftCount = self.aStar.read_encoders()[0]
    self.initialRightCount = self.aStar.read_encoders()[1]
  
  # makes multiple readings with RGB sensor and returns the average values
  def getColorAverage(self):
    numIterations = 3
    averageG = averageR = averageB = 0
    for i in range(0,numIterations):
      r, g, b, c = self.tcs.get_raw_data()
      averageG += g
      averageR += r
      averageB += b
    averageG /= numIterations
    averageR /= numIterations
    averageB /= numIterations
    return (averageR, averageG, averageB)
  
  # check whether RGB sensor is reading green
  def checkGreen(self):
    averageColors = self.getColorAverage()
    return (averageColors[1] > averageColors[0]) and (averageColors[1] > averageColors[2]) and averageColors[1] > 20

  # check whether RGB sensor is reading red
  def checkRed(self):
    averageColors = self.getColorAverage()
    return (averageColors[0] > averageColors[1]) and (averageColors[0] > averageColors[2]) and averageColors[0] > 20
  
  # check whether RGB sensor is reading purple
  def checkPurple(self):
    averageColors = self.getColorAverage()
    return (math.fabs(averageColors[0] - averageColors[2]) < 3) and (averageColors[1] / averageColors[0] < 0.6)

  # grab tuple containing RGB values (r, g, b, clear)
  def getColors(self):
    return self.tcs.get_raw_data()
      
  # set motor speeds of robot wheels
  def motors(self, lspeed, rspeed):
    self.aStar.motors(lspeed, rspeed)
  
  # set both motor speeds to max speed forward direction
  def goForward(self):
    self.motors(self.maxSpeed, self.maxSpeed)

  # set both motor speeds to zero
  def stop(self):
    self.motors(0, 0)
    
  # function used to getting the current time
  def getTime(self):
    return time.time()
  
  # play music notes on arduino buzzer
  def playNotes(self):
    self.aStar.play_notes("o4l16ceg>c8")
  
  # turn leds on or off
  def leds(self, red, yellow, green):
    self.aStar.leds(red, yellow, green)
   
  # reads analog information of arduino
  def readAnalog(self):
    return self.aStar.read_analog()
  
  # get the current reading of the robot battery
  def readBatteryMillivolts(self):
    return self.aStar.read_battery_millivolts()
  
  # get the boolean values of buttons on the arduino (A, B, C)
  def readButtons(self):
    return self.aStar.read_buttons()
   
  # reads the encoder information on the arduino wheels and returns a tuple (INT, INT)
  # uses relative encoder information based on class initialization
  def readEncoders(self):
    encoders = self.aStar.read_encoders()
    return (encoders[0] - self.initialLeftCount, encoders[1] - self.initialRightCount)
  
  # print r, g, b, temperature, and lux values of rgb sensor
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

  # used to calibrate direction to green facing
  def calibrateTwo(self):
    self.sweepsForGreen(100)
  
  # rotate bot a specified number of encoder counts
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

  # rotate robot 90 degrees left
  def turn90Left(self):
    self.turnCounts('left', 744)

  def turn90Right(self):
    self.turnCounts('right', 744)

  # move robot forward while calibrating the difference between the
  # wheel encoders to be within an epsilon of equivalence
  def goForwardtwo(self, offset):
    x = self.maxSpeed
    self.motors(int(100),int(100))
    grabEncoders = self.updateEncoders(offset)
    diff = math.fabs(grabEncoders[0] - grabEncoders[1])
    # print(diff)
    while(diff  >  3):
      grabEncoders = self.updateEncoders(offset)
      diff = math.fabs(grabEncoders[0] - grabEncoders[1])
      x-=1.0
      if(grabEncoders[0] < grabEncoders[1]):
        self.motors(int(self.maxSpeed), int(x))
        time.sleep(2.0/1000.0)
      elif(grabEncoders[0] > grabEncoders[1]):
        self.motors(int(x), int(self.maxSpeed))
        time.sleep(2.0/1000.0)
    self.motors(int(self.maxSpeed), int(self.maxSpeed))

  # get encoder offset (if one wheel is negative and the other is positive after a rotation)
  def zeroEncoders(self):
    return([self.aStar.read_encoders()[0]%32768, self.aStar.read_encoders()[1]%32768])
  
  # used for iterative tracking of encoder information from some original state
  # e.g. baseline = self.updateEncoders()...do loop...currentState = self.updateEncoders... compare against baseline
  def updateEncoders(self, offset):
    return([(self.aStar.read_encoders()[0]-offset[0])%32768, (self.aStar.read_encoders()[1]-offset[1])%32768])
  
  # look for green a number of rotation encoder counts in a particular direction
  def sweep(self, direction, counts):
    interval = 10
    iterations = math.ceil(counts / interval)
    for i in range (1, iterations):
      self.turnCounts(direction, interval)
      if(self.checkGreen()):
        return True
    return False
  
  # return true is green is found within a sweep distance, false otherwise
  def sweepsForGreen(self, counts):
    # counts is equal to the number of encoders counts at both sides of
    # facing direction  e.g. count = 50 searches 50 counts left and 50 right   
    initEncoders = self.readEncoders()
    self.sweep('left', counts)
    self.turnCounts('right', self.readEncoders()[1] - initEncoders[1])
    self.sweep('right', counts)
    self.turnCounts('left', self.readEncoders()[0] - initEncoders[0])
    return False

  # check where there are paths at a given intersection, return a list
  def getValidPaths(self):
    directions = list()
    self.calibrateTwo()
    if(self.checkGreen()):
      directions.append('forward')
    self.turn('left')
    if(self.checkGreen()):
      directions.append('left')
    self.turn('backward')
    if(self.checkGreen()):
      directions.append('right')
    self.turn('left')
    print(directions)
    return directions

  # center robot at intersection after intersection is detected
  def adjustIntersection(self):
    saveEncoders = self.readEncoders()
    while(self.readEncoders()[0] - saveEncoders[0] < 700
          and self.readEncoders()[1] - saveEncoders[1] < 700):
      self.goForward()
    print("Centered at intersection")

  # takes initial encoder values and newly recorded encoder values
  # and calculates the average of both to estimate the total forward distance
  def calculateForwardDistance(self, initialEncoderInfo):
    newEncoders = self.readEncoders()
    leftDistance = newEncoders[0] - initialEncoderInfo[0]
    rightDistance = newEncoders[1] - initialEncoderInfo[1]
    averageDistance = (leftDistance / 2) + (rightDistance / 2)
    return averageDistance

  # calculates current location based on a coordinate system
  def calculatePosition(self, lastPosition, directionFacing, forwardDistance):
    x = lastPosition[0]
    y = lastPosition[1]
    if(directionFacing == 'north'):
      return (x, y + forwardDistance)
    elif(directionFacing == 'west'):
      return (x - forwardDistance, y)
    elif(directionFacing == 'east'):
      return (x + forwardDistance, y)
    elif(directionFacing == 'south'):
      return (x, y - forwardDistance)
    else:
      print('invalid direction in calculatePosition()')
      return (0, 0) # we should never end up back at the starting position

  # calculate the new facing direction after turn
  def directionFacingAfterTurn(self, directionTurning, directionCurrentlyFacing):
    directions = ['north', 'west', 'south', 'east']
    index = 0
    if(directionTurning == 'left'):
      index = (directions.index(directionCurrentlyFacing) + 1) % 4
    elif(directionTurning == 'right'):
      index = (directions.index(directionCurrentlyFacing) - 1) % 4
    elif(directionTurning == 'forward'):
      index = (directions.index(directionCurrentlyFacing) + 0) % 4
    elif(directionTurning == 'backward'):
      index = (directions.index(directionCurrentlyFacing) + 2) % 4
    else:
      print('Error in directionFacingAfterTurn, invalid directionCurrentlyFacing value')    
    return directions[index]    
    
  # turn robot in a specified direction
  def turn(self, direction):
    if(direction == 'left'):
      self.turn90Left()
      self.calibrateTwo()
    elif(direction == 'right'):
      self.turn90Right()
      self.calibrateTwo()
    elif(direction == 'forward'):
      pass
    elif(direction == 'backward'):
      self.turn90Left()
      self.turn90Left()
      self.calibrateTwo()
    else:
      print("invalid direction in turn()")
    self.directionFacing = self.directionFacingAfterTurn(direction, self.directionFacing)
  
  # head back to previous intersection 
  def goToPreviousIntersection(self):
    while(not (self.checkRed())):
      if(self.checkGreen()):
        self.goForwardtwo(offset)
      else:
        self.calibrateTwo()
        offset = self.zeroEncoders()
    self.adjustIntersection()
    offset = self.zeroEncoders()
  
  # traverse through a maze using backtracking
  def completeMaze(self, previousPositions = list()):
    mazeSolved = False
    initialEncoderInfo = self.readEncoders()
    forwardDistance = 0
    # record initial position as a coordinate if list is empty, it should never be removed
    # and will always be the only position left in the list if all positions are popped
    offset = self.zeroEncoders()
    if (not previousPositions):
      previousPositions.append((0, 0))
      self.directionFacing = 'north'
    # continue until maze exit is found
    while(not mazeSolved):
      # follow the green-brick road
      if(self.checkGreen()):
        self.goForwardtwo(offset)
      # found intersection
      elif(self.checkRed()):
        self.adjustIntersection()
        forwardDistance = self.calculateForwardDistance(initialEncoderInfo)
        # In python, the [-1] references the last index in a list 
        currentPosition = self.calculatePosition(previousPositions[-1], self.directionFacing, forwardDistance)
        # if found end of maze, return
        if(self.checkPurple()):
          return True
        paths = self.getValidPaths()
        offset = self.zeroEncoders()
        # if no paths were detected, must be deadend
        if(not paths):
          pass
        else:
          # try eacn path (alter state), recurse, go back to starting position (revert state)
          for path in paths:
            self.turn(path) # change state
            offset = self.zeroEncoders()
            mazeSolved = self.completeMaze(previousPositions) # recursive call
            if(mazeSolved):
              return True
            # in order to get back to the original facing position, repeat original turn direction
            if(path != 'forward'):
                self.turn(path) # revert state
                offset = self.zeroEncoders()
            # forward is an exception, if returning from forward, stop at original position and turn around
            else:
                self.turn('backward')
                offset = self.zeroEncoders()
        self.turn('backward')   # turn towards last intersection 
        offset = self.zeroEncoders()  
        self.goToPreviousIntersection()  
        return False
      # end if checkRed()
      else:
        self.calibrateTwo() 
        offset = self.zeroEncoders()
    # end while    
    return False 
  # end completeMaze
  
# end Class Robot()


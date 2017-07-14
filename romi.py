from a_star import AStar
import Adafruit_TCS34725
import smbus
import time
import math

class Robot:
  def __init__(self):
    self.isLost = False
    self.nextSearchDirection = 0  # (left: 0, right: 1)
    self.directionFacing = 'north'
    self.veerSpeed = 30
    self.maxSpeed = 100
    self.aStar = AStar()
    self.tcs = Adafruit_TCS34725.TCS34725()
    self.initialLeftCount = self.aStar.read_encoders()[0]
    self.initialRightCount = self.aStar.read_encoders()[1]
    # self.aStar.reset_encoders()
    self.countLeft = 0
    self.countRight = 0
    self.lastCountLeft = 0
    self.lastCountRight = 0
    self.countSignLeft = 1
    self.countSignRight = -1
    # color stuff
    self.greenAvg = (0, 0, 0)
    self.greenCounts = 0
    self.redAvg = (0, 0, 0)
    self.redCounts = 0
    self.otherColorAvg = (0, 0, 0)
    self.otherColorCounts = 0

  def div(c):
    a, b = c
    return a / b
  def mul(c):
    a, b = c
    return a * b
  '''
  # check if currently reading green tape  
  def checkGreen(self):
    r, g, b, c = self.tcs.get_raw_data()
    return (g > r and g > b) and g > 45
  
  def checkRed(self):
    r, g, b, c = self.tcs.get_raw_data()
    return (r > g and r > b) and r > 45
  '''
  '''
  def getAverageTemp(self):
    numIterations = 5
    avgTemp = 0
    for i in range(0, numIterations):
      r, g, b, c = self.tcs.get_raw_data()
      temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)
      avgTemp += temp
    avgTemp /= numIterations
    return avgTemp

  def checkGreen(self):
    avgTemp = self.getAverageTemp()
    print('green temp: ' + str(avgTemp))
    return avgTemp > 2000 and avgTemp < 4000

  def checkRed(self):
    avgTemp = self.getAverageTemp()
    print('red temp: ' + str(avgTemp))
    return avgTemp > 4000 and avgTemp < 5500
  '''  
  def readCounts(self):
    differ = self.grabdifference()
    countRight = 0
    countLeft = 0
    countLeft, countRight = self.aStar.read_encoders()
    Left = countLeft
    Right = countRight
    if(differ < 100):
      countLeft, countRight = self.aStar.read_encoders()
      Right = countRight
      Left = countLeft
    else:
      maximum = max(countRight,countLeft)
      print(maximum)
      if(countRight == maximum):
        Right = Right - differ
      else:
        Left = Left - differ

    # print(countLeft, countRight)
    # diffLeft = (countLeft - self.lastCountLeft) % 0x10000
    # if diffLeft >= 0x8000:
    #     diffLeft -= 0x10000
        
    # diffRight = (countRight - self.lastCountRight) % 0x10000
    # if diffRight >= 0x8000:
    #     diffRight -= 0x10000
        
    # self.countLeft += self.countSignLeft * diffLeft
    # self.countRight += self.countSignRight * diffRight

    # self.lastCountLeft = countLeft
    # self.lastCountRight = countRight
    print(Right,Left)
    return countLeft, countRight
  def grabdifference(self):
    countLeft, countRight = self.aStar.read_encoders()
    diff = math.fabs(countLeft - countRight)
    return diff
  def reset(self):
    self.countLeft = 0
    self.countRight = 0 

  def getColorAverage(self):
    numIterations = 5
    averageG = averageR = averageB = 0
    for i in range(0,numIterations):
      r, g, b, c = self.tcs.get_raw_data()
      averageG += g
      averageR += r
      averageB += b
    averageG /= numIterations
    averageR /= numIterations
    averageB /= numIterations
    return (averageG, averageR, averageB)
  
  def checkGreen(self):
    averageColors = self.getColorAverage()
    return (averageColors[0] > averageColors[1]) and (averageColors[0] > averageColors[2]) and averageColors[0] > 20

  def checkRed(self):
    averageColors = self.getColorAverage()
    return (averageColors[1] > averageColors[0]) and (averageColors[1] > averageColors[2]) and averageColors[1] > 20

  def checkPurple(self):
    averageColors = self.getColorAverage()
    return (math.fabs(averageColors[0] - averageColors[2]) < 3) and (averageColors[1] / averageColors[0] < 0.5)

  def getColors(self):
    return self.tcs.get_raw_data()

  def calculateTupleDifference(t1, t2):
    a, b, c = t1
    x, y, z = t2
    return sum((math.fabs(a-x), math.fabs(b-y), math.fabs(c-z)))

  def decideColor(self):
    r, g, b, c = self.getColors()
    diffFromGreen = Robot.calculateTupleDifference(self.greenAvg, (r,g,b))
    diffFromRed =   Robot.calculateTupleDifference(self.redAvg, (r,g,b))
    diffFromOther = Robot.calculateTupleDifference(self.otherColorAvg, (r,g,b))
    if(diffFromGreen < diffFromRed and diffFromGreen < diffFromOther):
      self.updateColorAvg('green')
      return 'green'
    elif(diffFromRed < diffFromGreen and diffFromRed < diffFromOther):
      self.updateColorAvg('red')
      return 'red'
    else:
      self.updateColorAvg('otherColor')
      return 'other' 

  def calibrateColors(self):
    r, g, b, c = self.getColors()
    self.greenCounts += 1
    self.greenAvg = (r, g, b)
    self.playNotes()
    while(self.readButtons()[0] == False):
      pass
    time.sleep(1)
    r, g, b, c = self.getColors()
    self.redCounts += 1
    self.redAvg = (r, g, b)
    self.playNotes()
    while(self.readButtons()[0] == False):
      pass
    time.sleep(1)
    r, g, b, c = self.getColors()
    self.otherColorCounts += 1
    self.otherColorCounts = (r, g, b)
    self.playNotes()
    while(self.readButtons()[0] == False):
      pass
    time.sleep(1)

  def updateColorAvg(self, color):
    average = (0, 0, 0)
    r, g, b, c = self.getColors()
    if(color == 'green'):
      gC = self.greenCounts
      average = tuple(map(Robot.mul, zip(self.greenAvg, (gC, gC, gC))))
      average = tuple(map(sum, zip(average, (r, g, b))))
      self.greenCounts += 1
      gc = self.greenCounts
      average = tuple(map(Robot.div, zip(self.greenAvg, (gC, gC, gC))))
    elif(color == 'red'):
      rC = self.redCounts
      average = tuple(map(Robot.mul, zip(self.redAvg, (rC, rC, rC))))
      average = tuple(map(sum, zip(average, (r, g, b))))
      self.redCounts += 1
      rC = self.redCounts               
      average = tuple(map(Robot.div, zip(self.redAvg, (rC, rC, rC))))
    elif(color == 'otherColor'):
      oC = self.otherColorCounts
      average = tuple(map(Robot.mul, zip(self.otherColorAvg, (oC, oC, oC))))
      print("average: " + str(average))
      average = tuple(map(sum, zip(average, (r, g, b))))
      self.otherColorCounts += 1
      oC = self.otherColorCounts
      average = tuple(map(Robot.div, zip(self.otherColorAvg, (oC, oC, oC))))
      
  '''   
  def calibrateColors(self):
    while(self.greenCounts <  100):
      r, g, b, c = self.getColors()
      print((r, g, b))
      self.greenCounts += 1
      gC = self.greenCounts
      self.greenAvg = tuple(map(sum, zip(self.greenAvg, (r, g, b))))
      print("After Summation: " + str(self.greenAvg))
      self.greenAvg = tuple(map(Robot.div, zip(self.greenAvg, (gC, gC, gC))))
      print("After Division: " + str(self.greenAvg))
    self.playNotes()
    while(self.readButtons()[0] == False):
      pass
    while(self.redCounts < 100):
      r, g, b, c = self.getColors()
      self.redCounts += 1
      rC = self.redCounts
      self.redAvg = tuple(map(sum, zip(self.redAvg, (r, g, b))))
      self.redAvg = tuple(map(Robot.div, zip(self.redAvg, (rC, rC, rC))))
    self.playNotes()
    while(self.readButtons()[0] == False):
      pass
    while(self.otherColorCounts < 100):
      r, g, b, c = self.getColors()
      self.otherColorCounts += 1
      oC = self.otherColorCounts
      self.otherColorAvg = tuple(map(sum, zip(self.otherColorAvg, (r, g, b))))
      self.otherColorAvg = tuple(map(Robot.div, zip(self.otherColorAvg, (oC, oC, oC))))
    self.playNotes()
    while(self.readButtons()[0] == False):
      pass
    print("Average green: " + str(self.greenAvg) + ", Average red: " + str(self.redAvg) + ", Average other: " + str(self.otherColorAvg))
      
  '''
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

  def calibrateTwo(self):
    self.sweepsForGreen(80)
    
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

  def turn45Right(self):
    self.turnCounts('right', 372)

  def goForwardtwo(self, offset):
    x = self.maxSpeed
    self.motors(int(100),int(100))
    grabEncoders = self.updateEncoders(offset)
    # print(grabEncoders)
    diff = math.fabs(grabEncoders[0] - grabEncoders[1])
    # print(diff)
    while(diff  >  3):
      grabEncoders = self.updateEncoders(offset)
      diff = math.fabs(grabEncoders[0] - grabEncoders[1])
      x-=1.0
      # print(grabEncoders)
      # print(diff)
      if(grabEncoders[0] < grabEncoders[1]):
        self.motors(int(self.maxSpeed), int(x))
        time.sleep(2.0/1000.0)
      elif(grabEncoders[0] > grabEncoders[1]):
        self.motors(int(x), int(self.maxSpeed))
        time.sleep(2.0/1000.0)
    self.motors(int(self.maxSpeed), int(self.maxSpeed))

  def zeroEncoders(self):
    return([self.aStar.read_encoders()[0]%32768, self.aStar.read_encoders()[1]%32768])

  def updateEncoders(self, offset):
    return([(self.aStar.read_encoders()[0]-offset[0])%32768, (self.aStar.read_encoders()[1]-offset[1])%32768])
    

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
    #self.stop()
    #time.sleep(1)
    self.turnCounts('right', self.readEncoders()[1] - initEncoders[1])
    #self.stop()
    #time.sleep(1)
    # sweep right
    for i in range (1, iterations):
      self.turnCounts('right', interval)
      if(self.checkGreen()):
        return True
    #print(self.readEncoders()[0] - initEncoders[0])
    #self.stop()
    #time.sleep(1)
    self.turnCounts('left', self.readEncoders()[0] - initEncoders[0])
    #self.stop()
    #time.sleep(1)
    return False
  '''
  def getValidPaths(self):
    left = False
    forward = False
    right = False
    initEncoders = self.readEncoders()
    recordPaths = list()
    formatPaths = list()
    lastGreen = 0
    while(self.readEncoders()[1] < initEncoders[1] + 3400):
      self.motors(-50, 50)
      if(self.checkGreen() and self.readEncoders()[1] - lastGreen > 200):
        recordPaths.append(self.readEncoders()[1] - initEncoders[1])
        print("FOUND path at " + str(self.readEncoders()[1] - initEncoders[1]))
        lastGreen = self.readEncoders()[1]
    for record in recordPaths:
      # forward
      if(record < 150 or record > 2700):
        formatPaths.append(('forward', record))
      # left
      elif(record > 150 and record < 1250):
        formatPaths.append(('left', record))
      # backwards
      elif(record > 1250 and record < 1900):
        formatPaths.append(('backwards', record))
      # right
      elif(record > 1900 and record < 2700):
        formatPaths.append(('right', record))
    return formatPaths
  '''

  def getValidPaths(self):
    directions = list()
    self.calibrateTwo()
    if(self.checkGreen()):
      directions.append('forward')
    self.turn90Left()
    self.calibrateTwo()
    if(self.checkGreen()):
      directions.append('left')
    self.turn90Right()
    self.turn90Right()
    self.calibrateTwo()
    if(self.checkGreen()):
      directions.append('right')
    self.turn90Left()
    self.calibrateTwo()
    print(directions)
    return directions
    

  
  # def goForwardtwo(self):
  #   x = self.maxSpeed
  #   self.motors(x, x)
  #   grabEncoders = self.readCounts()
  #   # print(grabEncoders)
  #   diff = math.fabs(grabEncoders[0] - grabEncoders[1])
  #   # print(diff)
  #   while(diff  >  3):
  #     grabEncoders = self.readCounts()
  #     diff = math.fabs(grabEncoders[0] - grabEncoders[1])
  #     x-=1
  #     # print(grabEncoders)
  #     # print(diff)
  #     if(grabEncoders[0] < grabEncoders[1]):
  #       self.motors(self.maxSpeed, x)
  #       time.sleep(2.0/1000.0)
  #     elif(grabEncoders[0] > grabEncoders[1]):
  #       self.motors(x, self.maxSpeed)
  #       time.sleep(2.0/1000.0)
  #   self.motors(self.maxSpeed, self.maxSpeed)

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

  # calculates the current position of th# simple test that utilizes the romi class
  # move forward on green until lost
  #fre robot using the last position
  # and the direction in which the robot was moving
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
    

  # ugly way of calculating the new facing direction after turning
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
    
    
  #def haveBeenHereBefore(previousPositions, currentPosition):
    # define this function with some level of tolerance
    # -
    # -
    # -
    # - 

  # default parameters are needed for 'overloading', include parameters on all calls except initial
  # function call, function is meant to be called recursively
  
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
        print("IN THE FUCKING RED")
        self.adjustIntersection()
        forwardDistance = self.calculateForwardDistance(initialEncoderInfo)
        # In python, the [-1] references the last index in a list 
        currentPosition = self.calculatePosition(previousPositions[-1], self.directionFacing, forwardDistance)
      
        ''' 
        THIS SECTION IS UNNCESSARY IF WE DISALLOW LOOPS
        if(not haveBeenHereBefore(previousPositions, currentPosition)):
          # add current position to 'stack' of positions 
          previousPositions.append(currentPosition)
        else:
          # INSERT CODE TO TURN AROUND AND HEAD BACK TO LAST intersection
          pass
        '''
      
        # gets a tuple with valid paths e.g ('left', 'forward', 'right')
        # unnecessary to include 'backward' in paths, this is obvious
        # change output of getValidPaths to match the above example
        paths = self.getValidPaths()
        offset = self.zeroEncoders()
        if(not paths):
          pass
        else:
          # try eacn path (alter state), recurse, go back to starting position (revert state)
          for path in paths:
            self.directionFacing = self.directionFacingAfterTurn(path, self.directionFacing)
            self.turn(path) # change state
            offset = self.zeroEncoders()
            mazeSolved = self.completeMaze(previousPositions) # recursive call
            if(mazeSolved):
              return True
            # in order to get back to the original facing position, repeat original turn direction
            if(path != 'forward'):
                self.turn(path) # revert state
                self.directionFacing = self.directionFacingAfterTurn(path, self.directionFacing)
                offset = self.zeroEncoders()
            # forward is an exception, if returning from forward, stop at original position and turn around
            else:
                self.turn('backward')
                self.directionFacing = self.directionFacingAfterTurn('backward', self.directionFacing)
                offset = self.zeroEncoders()
        if(self.checkPurple()):
          return True
        
        previousPositions.pop() # remove this intersection from list, since NO LOOPS
        self.turn('backward')   # turn towards last intersection 
        offset = self.zeroEncoders()
        
        # head back to previous intersection 
        while(not (self.checkRed())):
          if(self.checkGreen()):
            self.goForwardtwo(offset)
          else:
            self.calibrateTwo()
            offset = self.zeroEncoders()
        self.adjustIntersection()
        offset = self.zeroEncoders()
        
        return False
      # end if (checkRed())
      
      # found blue / winning condition
      #elif(onColor == BLUE?):
        #return True
      # fix position on green (this could probably be a part of 
      # a function goForwardWhileGreen() that calibrates automatically
      else:
        self.calibrateTwo() 
        offset = self.zeroEncoders()
      
    # end while    
    return False
  
  # end completeMaze
  
# end Class Robot()


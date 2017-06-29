#Note: due to the hardware-oriented nature of the product, testing sould be done with access to the sensors and motors.

from a_star import AStar
import Adafruit_TCS34725
import smbus
import time
import unittest



def getSensorColor(tcs):
  r, g, b, c = tcs.get_raw_data()
  if(max(r, g, b)==r):
    return('red')
  elif(max(r, g, b)==g):
    return('green')
  elif(max(r, g, b)==b):
    return('blue')
  else:
    return('no max color')

def checkIfGreen(tcs):
  r, g, b, c = tcs.get_raw_data()
  return (g > r and g > b)
# end checkIfGreen()

def calibrateLeft(a_star, tcs, searchTime, turnWheelSpeed):
  adjustTime = time.time()
  a_star.motors(turnWheelSpeed, 100)
  while((time.time() - adjustTime) < searchTime):
    if(checkIfGreen(tcs)):
      return(0)
  # end while 
  return(1) 
# end calibrateDirection()

def calibrateRight(a_star, tcs, searchTime, turnWheelSpeed):
  adjustTime = time.time()
  a_star.motors(100, turnWheelSpeed)
  while((time.time() - adjustTime) < searchTime):
    if(checkIfGreen(tcs)):
      return(0)
  # end while 
  return(1)
# end calibrateDirection()


  
class TestSensor(unittest.TestCase):
  a_star = AStar()
  tcs = Adafruit_TCS34725.TCS34725()
  tcs.set_interrupt(False)
  turnWheelSpeed=70
  def testSensorColor(self):
    self.assertTrue(getSensorColor(self.tcs)=='red' or getSensorColor(self.tcs)=='green' or getSensorColor(self.tcs)=='blue')
  
  def testRecalibrateLeft(self):
    calibrateLeft(self.a_star, self.tcs, 1000, self.turnWheelSpeed)
    self.assertTrue(checkIfGreen(self.tcs))
  def testRecalibrateRight(self):
    calibrateRight(self.a_star, self.tcs, 1000, self.turnWheelSpeed)
    self.assertTrue(checkIfGreen(self.tcs))
    
    
if __name__ == "__main__": unittest.main()

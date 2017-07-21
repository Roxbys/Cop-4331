#To test if the robot is going in a straight line along a path, we must 
#first position the robot at the end of the colored tape. 
#Execute goForwardTest.py in the raspberry pi terminal. 
#Then we check to see if the Robot goes off the green tape, that it will detect the absence of color and 
#calibrate itself back to the colored tape. If so then the test passed. 
#If the Robot never went back to the colored tape then the test failed.


from romi import *
import time

def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()
  if(romi.checkGreen())
    self.goForwardtwo(0)
  romi.stop()
  romi.turnOnInterruptsRGB()
  romi.disableRGB()  
#end main
    
if __name__ == "__main__": main() 

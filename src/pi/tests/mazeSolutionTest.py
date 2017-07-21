# test of the complete Maze method of the Robot class
# main returns true if there is a solution, false otherwise
from romi import *
import time

def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()
  retval = False
  if(romi.completeMaze()):
    retval = True
  romi.stop()
  romi.turnOnInterruptsRGB()
  romi.disableRGB()  
  return retval
#end main
    
if __name__ == "__main__": main()   

# test of the completeMaze method of the Robot class
from romi import *
import time

def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()
  romi.completeMaze()
  romi.stop()
  romi.turnOnInterruptsRGB()
  romi.disableRGB()  
#end main
    
if __name__ == "__main__": main()   




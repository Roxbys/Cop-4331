# test of the playSound() method of the Robot class
from romi import *
import time

def main():
  romi = Robot()
  romi.turnOffInterruptsRGB()
  romi.playNotes()
  romi.stop()
  romi.turnOnInterruptsRGB()
  romi.disableRGB()  
#end main
    
if __name__ == "__main__": main()   



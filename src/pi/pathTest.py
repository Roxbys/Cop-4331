# simple test that utilizes the romi class
# move forward on green until lost
from romi import *

def main():
    romi = Robot()
    romi.turnOffInterruptsRGB()
    
    while(not romi.isLost):
      romi.followPath()
        
    if(romi.isLost):
        romi.giveUp()
      
    romi.turnOnInterruptsRGB()
    romi.disableRGB()
#end main
    
if __name__ == "__main__": main()

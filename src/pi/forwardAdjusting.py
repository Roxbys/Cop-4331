# small test to ensure forward movement on detection of green color by rgb sensor

from a_star import AStar
import Adafruit_TCS34725
import smbus

a_star = AStar()
tcs = Adafruit_TCS34725.TCS34725()


tcs.set_interrupt(False)
r, g, b, c = tcs.get_raw_data()
buttons = a_star.read_buttons()

# saves the last direction robot turned, left=0 right=1
lastDecision = 0   

# speeds of motors
lspeed = rspeed = int(0)

while (!cancel): 

  # totally guessing that this is how you reference button C
  cancel = (a_star.read_buttons())[2]
  
  while ((g > r and g > b) and !cancel):
  
    print('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))
    lspeed = rspeed = 100
    a_star.motors(lspeed, rspeed)
    
    r, g, b, c = tcs.get_raw_data()
    cancel = (a_star.read_buttons())[2]
    
  if(cancel):
    break
  
  while(!(g > r and g > b) and !cancel):
  
    lspeed, rspeed, lastDecision = adjustSpeed(lspeed, rspeed, lastDecision)
    a_star.motors(lspeed, rspeed)
    
    #insert some delay here
    r, g, b, c = tcs.get_raw_data()
    cancel = (a_star.read_buttons())[2]
  


# Enable interrupts and put the chip back to low power sleep/disabled.
tcs.set_interrupt(True)
tcs.disable()

def adjustSpeed(lspeed, rspeed, lastDecision)
  retval = (lspeed - 50, rspeed) if lastDecision == 1 else (lspeed, rspeed - 50)
  lastDecision = lastDecision ^ 0
  return (lspeed, rspeed, lastDecision)

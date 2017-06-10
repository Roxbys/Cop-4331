// This example drives the device in a square
#include <Romi32U4.h>

Romi32U4Motors motors;
Romi32U4ButtonA buttonA;
Romi32U4ButtonC buttonC;
int turnOff = 0;

void setup()
{
  buttonA.waitForButton();
  delay(500);
}

void loop()
{
  while(!turnOff) 
  {
    for(int speed = 0; speed < 150; speed++)
      motors.setSpeeds(speed, speed);
      
    turnOff = (turnOff == 1) ? turnOff : buttonC.isPressed();
   
    for(int speed = 150; speed > 0; speed--) 
      motors.setSpeeds(speed, speed);
      
    turnOff = (turnOff == 1) ? turnOff : buttonC.isPressed();
    
    delay(500);
    motors.setSpeeds(-50, 50);
    delay(900);
    
    turnOff = (turnOff == 1) ? turnOff : buttonC.isPressed();
  }
}

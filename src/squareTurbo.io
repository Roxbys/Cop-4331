// This example drives the device in a square
#include <Romi32U4.h>

Romi32U4Motors motors;
Romi32U4ButtonA buttonA;
Romi32U4ButtonC buttonC;

void setup()
{
  buttonA.waitForButton();
  motors.allowTurbo();
  delay(500);
}

void loop()
{
  while(!buttonC.isPressed()) 
  {
    motors.setSpeeds(400,400);
    delay(500);
    motors.setSpeeds(-50, 50);
    delay(50);
  }
}

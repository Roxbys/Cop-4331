// This example drives the device in a circle
#include <Romi32U4.h>

Romi32U4Motors motors;
Romi32U4ButtonA buttonA;
Romi32U4ButtonB buttonB;
Romi32U4ButtonC buttonC;

void setup()
{
  buttonA.waitForButton();
  delay(500);
}

void loop()
{
  motors.setLeftSpeed(200);
  motors.setRightSpeed(150);
}

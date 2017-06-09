// Simple program that moves the bot forward
// Press A: start
// Press C: cancel

#include <Romi32U4.h>

Romi32U4Motors motors;
Romi32U4ButtonA buttonA;
Romi32U4ButtonC buttonC;

void setup()
{
  // Wait for the user to press button A.
  buttonA.waitForButton();

  // Delay so that the robot does not move away while the user is
  // still touching it.
  delay(1000);
}

void loop()
{
  // Run both motors forward.
  motors.setLeftSpeed(400);
  motors.setRightSpeed(400);
  
  while(!buttonC.isPressed());

  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);
}

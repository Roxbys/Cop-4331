// Simple program that moves the bot forward
// Press A: start
// Press C: cancel

#include <Romi32U4.h>

#define MAX_SPEED 400 

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
  // run both motors forward
  for(int speed = 0; speed <= MAX_SPEED; speed += 5) 
  {
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
    delay(5);
  } 
  
  while(!buttonC.isPressed());

  // slow 'er down
  for(int speed = MAX_SPEED; speed > 0 ; speed -= 5) 
  {
    motors.setLeftSpeed(speed);
    motors.setRightSpeed(speed);
    delay(5);
  }
}

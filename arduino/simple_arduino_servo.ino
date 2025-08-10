/*
 * Simple Servo Controller
 * LEFT: Moves only left motor (motor1) from 0 to 180 and back
 * RIGHT: Moves only right motor (motor2) from 180 to 0 and back
 */

#include <Servo.h>

Servo motor1;  // Left motor on pin 13
Servo motor2;  // Right motor on pin 12

int motor1_home = 0;    // Home position for left motor
int motor2_home = 180;  // Home position for right motor

void setup() {
  Serial.begin(9600);
  motor1.attach(13);
  motor2.attach(12);
  
  // Start at home positions
  motor1.write(motor1_home);
  motor2.write(motor2_home);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.length() >= 2) {
      char direction = command.charAt(0);
      int degrees = command.substring(1).toInt();
      
      // Clamp degrees to 0-180
      degrees = constrain(degrees, 0, 180);
      
      if (direction == 'L' || direction == 'l') {
        // LEFT: Move only motor1 (left motor)
        // Goes from 0 → degrees → 0
        motor1.write(degrees);
        delay(1000);  // Hold position
        motor1.write(motor1_home);  // Return to home (0)
      }
      else if (direction == 'R' || direction == 'r') {
        // RIGHT: Move only motor2 (right motor)  
        // Goes from 180 → (180-degrees) → 180
        motor2.write(180 - degrees);
        delay(1000);  // Hold position
        motor2.write(motor2_home);  // Return to home (180)
      }
      else if (direction == 'H' || direction == 'h') {
        // HOME: Return both to home positions
        motor1.write(motor1_home);
        motor2.write(motor2_home);
      }
    }
  }
}
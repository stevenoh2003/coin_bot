#include <PWMServo.h>

PWMServo hundred_yen_servo;  // create servo object to control a servo
PWMServo ten_yen_servo;      // create servo object to control a servo

int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);            // initialize serial communication at 9600 bits per second
  hundred_yen_servo.attach(19);  // attaches the servo on pin 19 to the servo object
  ten_yen_servo.attach(18);      // attaches the servo on pin 18 to the servo object

  hundred_yen_servo.write(90);             
  ten_yen_servo.write(0);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // read the incoming byte:
    switch(command) {
      case 'T':
        ten_eject();
        break;
      case 'H':
        hundred_eject();
        break;
      default:
        // unrecognized command, you might want to handle it
        break;
    }
  }
}


void ten_eject(){
  for(pos = 0; pos < 90; pos += 2) { // goes from 0 degrees to 180 degrees, 1 degree steps
    ten_yen_servo.write(pos);  
    delay(15);                      
  }
  for(pos = 90; pos>=1; pos-=2) {   // goes from 180 degrees to 0 degrees
    ten_yen_servo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }

}

void hundred_eject(){

  for(pos = 100; pos>=1; pos-=2) {   // goes from 180 degrees to 0 degrees
    hundred_yen_servo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }

  for(pos = 0; pos < 100; pos += 2) { // goes from 0 degrees to 180 degrees, 1 degree steps
    hundred_yen_servo.write(pos);  
                
    delay(15);                      
  }
}
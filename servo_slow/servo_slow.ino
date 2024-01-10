#include <Servo.h>

Servo myservo1;
Servo myservo2;

int angle1 = 10;
int angle2 = 170;
int servopin1 = 2;
int servopin2 = 3;

void setup() {
  myservo1.attach(servopin1);
  myservo2.attach(servopin2);
  Serial.begin(115200);
}

int status1 = 0;
int status2 = 0;
int done = 0;

void loop() {
  status1 = run_servos(angle1, myservo1, 5);
  status2 = run_servos(angle2, myservo2, 5);
  Serial.println(myservo1.read());
  
  if (status1 && status2 == 1) { // status1 == 1
    done = 1;
    Serial.println("BREAK!");
    status1 = run_servos(0, myservo1, 5);
    status2 = run_servos(0, myservo2, 5);
  }
}

int run_servos(int thePos, Servo theServo, int delay_speed){
  int startPos = theServo.read(); // read the curr position
  Serial.println(startPos);
  int newPos = startPos;

  if (startPos < thePos){
    newPos = newPos + 1;
    theServo.write(newPos);
    delay(delay_speed);
    return 0;
  }

  else if (newPos > thePos){
    newPos = newPos - 1;
    theServo.write(newPos);
    delay(delay_speed);
    return 0;
  }

  else {
    return 1; // arrived position
  }
}
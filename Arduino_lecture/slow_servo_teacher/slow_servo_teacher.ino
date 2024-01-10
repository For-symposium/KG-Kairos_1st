#include<Servo.h>

Servo myServo;

int angle = 90;

int run_servos(Servo sv, int to, int speed)
{
  int curr_angle = sv.read();
  if(to > curr_angle){
    curr_angle++;
    sv.write(curr_angle);
    delay(speed);
    return 0;
  }else{
    return 1;
  }
}

void setup() {
  // put your setup code here, to run once:
  myServo.attach(2);
  myServo.write(90);
  Serial.begin(11500);

}
int sv1 = 0;
int done = 0;
void loop() {
  if(done == 0){
    sv1 = run_servos(myServo, 150, 20);
    if(sv1 == 1)
      done = 1; 
  }
}

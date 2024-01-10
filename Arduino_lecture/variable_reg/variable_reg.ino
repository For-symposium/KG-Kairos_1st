#include <Servo.h>

int analogPin = A0;
Servo myservo;

void setup() {
  Serial.begin(115200);
  pinMode(analogPin, INPUT);
  myservo.attach(9);
}

void loop() {
  // 각 180도 : 1024도 
  int value = analogRead(analogPin);
  int servo_value = map(value,0,1023,0,180);
  int my_servo_value = mapp(value,0,1023,0,180);
  Serial.print(value);
  Serial.print("    ");
  Serial.print(servo_value);
  Serial.print("    ");
  Serial.println(my_servo_value);
  myservo.write(my_servo_value);
}

int mapp(int var, int a1, int a2, int b1, int b2){
  // int result = ((b2-b1)/(float)(a2-a1)) * var; 
  return ((float)(b2-b1)/(a2-a1)) * var;;
}


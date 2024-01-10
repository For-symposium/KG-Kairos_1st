/*
서보모터
거리에 따라서 서보모터 제어 like 차량 게이지
+ 부저음
*/

#include <Servo.h>

const int servo_pin = 10;
Servo servo;

int max_dist = 60;
int curr_angle = 0;
int stop_dist = 10;
unsigned long prevTime = 0; // will store last time servo was updated
const long interval = 20;  // interval at which to update servo (milliseconds)


const int trig_pin = 5;
const int echo_pin = 6;

void setup() {
  Serial.begin(115200);
  servo.attach(servo_pin);

  pinMode(trig_pin, OUTPUT);
  pinMode(echo_pin, INPUT);
}

void servo_up(){
  for (int i=0; i<=180; i++){
    servo.write(i);
    delay(5);
  }
}

void servo_down(){
  for (int i=180; i>=0; i--){
    servo.write(i);
    delay(5);
  }
}

void loop() {
  // servo.write(0);
  // delay(500);

  ready_ultra(trig_pin);
  long duration = pulseIn(echo_pin, HIGH);
  long dist = (duration/2) / 29.1;
  float filtervalue = 0;
  // Serial.println("check");
  Serial.println(dist);


  servo_control_by_sonic_stop(max_dist, dist, stop_dist);
}

void servo_control_by_sonic_stop(int max_dist, int dist, int stop_dist){
  // int dist; // receive ultrasonic distance
  int servo_angle = map(dist, 0, max_dist, 0, 180);

  if (dist <= stop_dist){
    servo.write(curr_angle);
    Serial.print("STOP!");
  }
  else {
    curr_angle = servo_angle;

    unsigned long currentTime = millis();
    if (currentTime - prevTime >= interval) {
      // Save the last time you updated the servo
      prevTime = currentTime;
    }


    servo.write(curr_angle);
    // delay(1000);
    

    Serial.print("Dist : ");
    Serial.print(dist);
    Serial.print("\tAngle : ");
    Serial.println(servo_angle);
  }
}


void servo_control_by_sonic_slow(int max_dist, int dist, int stop_dist){
  // int dist; // receive ultrasonic distance
  int servo_angle = map(dist, 0, max_dist, 0, 180);
  int slow_rate = map(dist, 0, max_dist, 1, 20);

  if (dist <= stop_dist){
    servo.write(curr_angle);
  }
  else {
    curr_angle = servo_angle;
    servo.write(curr_angle);
    delay(slow_rate);

    Serial.print("Dist : ");
    Serial.print(dist);
    Serial.print("\tAngle : ");
    Serial.println(servo_angle);
  }
}

void ready_ultra(int trigpin){
  digitalWrite(trigpin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigpin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigpin, LOW);
}
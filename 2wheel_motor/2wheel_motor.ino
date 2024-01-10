#include <SoftwareSerial.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

#define blueTX 2
#define blueRX 3
char ser = 0;
char ble = 0;

int motor1 = 5;
int motor2 = 6;
int motor3 = 9;
int motor4 = 10;

const int trigpin = 11;
const int echopin = 12;
float filtervalue = 0;
float sensitivity = 0.1;
long duration;
long distance;
float oldvalue = 0;
float class_filter;
float currentDistance;

bool forward_active = false;
bool gyzo_active = false;

SoftwareSerial HC06(blueTX, blueRX);

void setup() {
  Serial.begin(9600);
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor3, OUTPUT);
  pinMode(motor4, OUTPUT);
  HC06.begin(9600);
  pinMode(trigpin, OUTPUT);
  pinMode(echopin, INPUT);

  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  
  // 어느 정도의 가속도를 측정할 것인지
  case MPU6050_RANGE_2_G: 
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  
  // 어느 정도의 각도 오차를 인용할 것인지
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  Serial.println("");
  delay(100);
}

void loop() {
  // bluetooth
  // HC06proc();

  if (Serial.available()){
    char readval = Serial.read();

    if (readval == '1'){ 
      stop();
      Serial.println("Stop");
      forward_active = false;
      gyzo_active = false;
    }

    else if (readval == '2'){ 
      Serial.println("Forward");
      forward_active = true;
      gyzo_active = true;
    }

    else if (readval == '3'){ 
      backward();
      Serial.println("Backward");
    }

    else if (readval == '4'){ 
      forward();
      
    }
  }

  currentDistance = get_distance();   
  forward_signal_stop_go(forward_active);
  gyro_signal_left_right(gyzo_active);
  delay(200); // Adjust delay as needed based on how responsive your system needs to be
}

void HC06proc(){
  if (Serial.available() > 0){
    ser = Serial.read();
    HC06.write(ser);
  }
  if (HC06.available() > 0){
    ble = HC06.read();
    Serial.write(ble);
  }
}

void stop(){
  analogWrite(motor1, LOW);
  analogWrite(motor2, LOW);
  analogWrite(motor3, LOW);
  analogWrite(motor4, LOW);
}

void forward(){
  analogWrite(motor1, 160); 
  analogWrite(motor2, LOW);
  analogWrite(motor3, 160); 
  analogWrite(motor4, LOW);
}

void backward(){
  analogWrite(motor1, LOW); 
  analogWrite(motor2, 163);
  analogWrite(motor3, LOW); 
  analogWrite(motor4, 120);
}

void turn_left(){
  analogWrite(motor1, 210); 
  analogWrite(motor2, LOW);
  analogWrite(motor3, 130); 
  analogWrite(motor4, LOW);
}

void turn_right(){
  analogWrite(motor1, 130); 
  analogWrite(motor2, LOW);
  analogWrite(motor3, 160); 
  analogWrite(motor4, LOW);
}

void ready_ultra(int trigpin){
  digitalWrite(trigpin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigpin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigpin, LOW);
}

float get_distance(){
  ready_ultra(trigpin);
  duration = pulseIn(echopin, HIGH);
  distance = (duration/2) / 29.1;
  return distance;
}

float get_sonic_filtered(){
  duration = pulseIn(echopin, HIGH);
  distance = (duration/2) / 29.1;
  
  // filtervalue = 0;

  // float new_dist = (filtervalue/100) * (1 - sensitivity) + distance * sensitivity;
  class_filter = sensitivity * distance + (1-sensitivity) * oldvalue;
  oldvalue = distance;  
  Serial.print("Distance : ");
  Serial.println(distance);
  Serial.print("Oldvalue : ");
  Serial.println(oldvalue);
  Serial.print("Class_filter : ");
  Serial.println(class_filter);
  return class_filter;
}

void forward_signal_stop_go(bool state){
  if (state) {
    if (currentDistance < 25) {
      stop();
      delay(500);
      Serial.print("Stop: distance = ");
      Serial.println(currentDistance);
    }
    else {
      forward();
      Serial.print("Forward: distance = ");
      Serial.println(currentDistance);
    }
  }
}

void gyro_signal_left_right(bool state){
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  if (state){
    if (g.gyro.z < -0.3){
      Serial.print("GYZO : Turn left");
      Serial.println(g.gyro.z);
      turn_left();
      delay(200);
    }
    else if (g.gyro.z > 0.3){
      Serial.print("GYZO : Turn right");
      Serial.println(g.gyro.z);
      turn_right();
      delay(200);
    }
  }
}
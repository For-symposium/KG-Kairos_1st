#include <Servo.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Servo myservo1;
Servo myservo2;
Adafruit_MPU6050 mpu;

int angle1 = 10;
int angle2 = 170;
int servopin1 = 2;
int servopin2 = 3;

void setup() {
  myservo1.attach(servopin1);
  myservo2.attach(servopin2);
  Serial.begin(115200);

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

  Serial.println("");
  delay(100);
  }
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  int angle = map(a.acceleration.y, -10, 10, 0, 180);
  // int angle = map(g.acceleration.x, -10, 10, 0, 180);

  if (a.acceleration.y >= 0){
    // angle++;
    run_servos(angle, myservo1, 20);
    Serial.print(angle);
    Serial.print("\tMinus\t");
    Serial.println(a.acceleration.y);
    if (angle >= 170){
      angle = 170;
    }
  }
  else {
    // angle--;
    run_servos(angle, myservo1, 20);
    Serial.print(angle);
    Serial.print("\tPlus\t");
    Serial.println(a.acceleration.y);
    if (angle <= 10){
      angle = 10;
    }
  }
  delay(20);
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

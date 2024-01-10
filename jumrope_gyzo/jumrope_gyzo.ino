#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

enum JumpState{
  WAITING,
  JUMP_DETECTED
};

JumpState jumpState = WAITING; // Initialize jumpstate

void setup() {
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

int count = 0;
const int threshold = 4;  // Define your own threshold for jump detection
const unsigned long debounceTime = 300;  // Debounce time in milliseconds
unsigned long lastJumpTime = 0;  // Time when the last jump was detected

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float currentAcceleration = sqrt(pow(g.gyro.x, 2) + pow(g.gyro.y, 2) + pow(g.gyro.z, 2));
  
  // Check the state and current acceleration to decide on counting logic
  if (jumpState == WAITING && currentAcceleration > threshold) {
    // A potential jump is detected
    unsigned long currentTime = millis();
    if (currentTime - lastJumpTime > debounceTime) {  // Debounce check
      // Count the jump and update the state and time
      count++;
      Serial.print("Jump count: ");
      Serial.println(count);
      lastJumpTime = currentTime;
      jumpState = JUMP_DETECTED;  // Change the state to avoid counting again until ready
    }
  } else if (jumpState == JUMP_DETECTED && currentAcceleration < threshold) {
    // Once acceleration goes below threshold, get ready for the next jump
    jumpState = WAITING;
  }

  // Add a small delay to reduce sampling rate
  delay(50);
}

float result(){
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  return sqrt(pow(g.acceleration.x, 2) + pow(g.acceleration.y, 2) + pow(g.acceleration.z, 2));
}
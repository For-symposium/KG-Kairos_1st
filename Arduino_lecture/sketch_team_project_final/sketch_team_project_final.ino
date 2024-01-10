#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Servo.h>

const int servo_pin = 10;
Servo servo;

int max_dist = 60;
int curr_angle = 0;
int stop_dist = 10;
float aa=0; float bb=5; float cc= 10; float dd=20; float ee=50; float ff=80; float gg=100;

unsigned long prevTime = 0;
const long interval = 20;

// 초음파 센서
const int trig_pin=11;//US trigger pin Number
const int echo_pin=12;//US echo pin Number

float distance_US;//the distance between the US sensor and an object
float dis_befor=0;//

// OLED 설정
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library. 
// On an arduino UNO:       A4(SDA), A5(SCL)
// On an arduino MEGA 2560: 20(SDA), 21(SCL)
// On an arduino LEONARDO:   2(SDA),  3(SCL), ...
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define NUMFLAKES     10 // Number of snowflakes in the animation example

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16
static const unsigned char PROGMEM logo_bmp[] =
{ 0b00000000, 0b11000000,
  0b00000001, 0b11000000,
  0b00000001, 0b11000000,
  0b00000011, 0b11100000,
  0b11110011, 0b11100000,
  0b11111110, 0b11111000,
  0b01111110, 0b11111111,
  0b00110011, 0b10011111,
  0b00011111, 0b11111100,
  0b00001101, 0b01110000,
  0b00011011, 0b10100000,
  0b00111111, 0b11100000,
  0b00111111, 0b11110000,
  0b01111100, 0b11110000,
  0b01110000, 0b01110000,
  0b00000000, 0b00110000 };

// Button Interrupt 설정
int stopState = 0;
int interruptPin = 2;

// Servo Motor 설정
Servo myServo; //Servo Class 객체 생성
//int servo_pin = 10;

class US{



  /////////////////////
  public:
    ///////////////Trig_Pusle/////////////////////**triger pusle setting

    void Trig_Pulse(int trig_pin, int pulse_time){//trig_pin: trig pin number, pulse_time: trigger pulse time[us]
      digitalWrite(trig_pin, LOW);
      delayMicroseconds(2);
      digitalWrite(trig_pin, HIGH);
      delayMicroseconds(pulse_time);
      digitalWrite(trig_pin, LOW);
    }
    ///////////////////////////////////////////////

    /////////////distance///////////////////////**calculate the distance from the US to an object
    float distance(int echo_pin){
        return (pulseIn(echo_pin, HIGH)/2)/29.1;
    }


  private:

};

US US1;


class Led{
public:
  Led(int pin_){
    pin=pin_;
    pinMode(pin,OUTPUT);
  }
  Led(){
    pin=3;
  }
  turnOn(){
    digitalWrite(pin,HIGH);
  }
  turnOff(){
    digitalWrite(pin,LOW);
  }
  private:
  int pin;
};

Led l1(3);
Led l2(4);
Led l3(5);
Led l4(6);
Led l5(7);
Led l6(8);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(trig_pin,OUTPUT);
  pinMode(echo_pin, INPUT);
  servo.attach(10);

  //myServo.attach(10);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), stop_Interrupt, FALLING);
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  start_display();
}

void loop() {
  // put your main code here, to run repeatedly:
  
  US1.Trig_Pulse(trig_pin,10);//Trige Pulse setting
  distance_US=US1.distance(echo_pin);//distance from an object[cm]

  Serial.print(distance_US);
  Serial.println(" cm");
  delay(100);
  float Value=distance_US;
  Serial.println(Value);
  if (Value > ff&& Value<=gg){
    l1.turnOn();
    l2.turnOff();
    l3.turnOff();
    l4.turnOff();
    l5.turnOff();
    l6.turnOff();
  }
  else if (Value<=ff&& Value>ee){
    l1.turnOn();
    l2.turnOn();
    l3.turnOff();
    l4.turnOff();
    l5.turnOff();
    l6.turnOff();
  }
  else if (Value<=ee&& Value>dd)
  {
    l1.turnOn();
    l2.turnOn();
    l3.turnOn();
    l4.turnOff();
    l5.turnOff();
    l6.turnOff();
  }
  else if (Value<=dd&& Value>cc){
    l1.turnOn();
    l2.turnOn();
    l3.turnOn();
    l4.turnOn();
    l5.turnOff();
    l6.turnOff();
  }
  else if (Value<=cc&& Value>bb){
    l1.turnOn();
    l2.turnOn();
    l3.turnOn();
    l4.turnOn();
    l5.turnOn();
    l6.turnOff();
  }
  else if (Value<=bb && Value>aa){
    l1.turnOn();
    l2.turnOn();
    l3.turnOn();
    l4.turnOn();
    l5.turnOn();
    l6.turnOn();
    // Shutt down
  }
  else {
    l1.turnOff();
    l2.turnOff();
    l3.turnOff();
    l4.turnOff();
    l5.turnOff();
    l6.turnOff();
  }
  // 비상 정지
  if(stopState == 1){
    stop_display();
    servo.write(0);
    l1.turnOff();
    l2.turnOff();
    l3.turnOff();
    l4.turnOff();
    l5.turnOff();
    l6.turnOff();
    exit(0);

  }

  distance_display(distance_US); 
  // Serial.println(stopState);

  servo.write(0);
  //delay(500);

  ready_ultra(trig_pin);
  long duration = pulseIn(echo_pin, HIGH);
  long dist = (duration/2) / 29.1;
  float filtervalue = 0;
  // Serial.println("check");
  Serial.println(dist);


  servo_control_by_sonic_stop(max_dist, dist, stop_dist);
}

void start_display(void){
  display.clearDisplay();
  display.drawRect(10 , 10, display.width()-15, display.height()-15, SSD1306_WHITE);
  display.setTextSize(1);             // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);        // Draw white text
  display.setCursor(50,15);             // Start at top-left corner
  display.println(F("Start!"));
  display.display();
  delay(1000);
}

void distance_display(int distance){
  display.clearDisplay();
  String message = "distance : " + String(distance);
  display.drawRect(10 , 10, display.width()-15, display.height()-15, SSD1306_WHITE);
  display.setTextSize(1);             // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);        // Draw white text
  display.setCursor(25,15);             // Start at top-left corner
  display.println(message);
  display.display();
  delay(100);
}

void stop_display(void){
  display.clearDisplay();
  display.drawRect(10 , 10, display.width()-15, display.height()-15, SSD1306_WHITE);
  display.setTextSize(1);             // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);        // Draw white text
  display.setCursor(50,15);             // Start at top-left corner
  display.println(F("Stop!"));
  display.display();
  delay(100);
}

void stop_Interrupt(){
  if(stopState == 0){
    stopState = 1;
  }

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
    if (currentTime - prevTime >= interval){
      prevTime = currentTime;
    }

    servo.write(curr_angle);

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

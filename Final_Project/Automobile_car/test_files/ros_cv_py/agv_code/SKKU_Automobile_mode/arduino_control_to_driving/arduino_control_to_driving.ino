#include <Car_Library.h>
String data = "";
char wait = 'i';
int car_speed = 0;
int car_coor = 115;
int motorA1=6;
int motorA2=7;
int motorA3=11;
int motorA4=10;
int analogPin=A0; //가변저항 output pin
int motorDirection1Pin = 8; // 모터 방향 핀 1
int motorDirection2Pin = 9; // 모터 방향 핀 2
int val = 110;
int data_length = 0;
String temp = "";
String temp_2 = "";

// 파이썬으로부터 오는 data는 char 형식으로 한글자씩만 들어옴
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(motorA1, OUTPUT);
  pinMode(motorA2, OUTPUT);
  pinMode(motorA3, OUTPUT);
  pinMode(motorA4, OUTPUT);
  pinMode(motorDirection1Pin, OUTPUT);
  pinMode(motorDirection2Pin, OUTPUT);
  pinMode(analogPin,INPUT);
}

void loop() {
   val = potentiometer_Read(analogPin); 
      // 신호가 들어올때까지 대기하기 위함
    if(Serial.available()) 
   {
     char wait = Serial.read();
     data.concat(wait);
     data_length = data.length();
   } 
   if (data[0] == 'g'){
    // if first word is g send current coor and speed value
    
    Serial.println(car_speed+(String)","+val);  
    data = "";
 
   }
   
   if (data[0] == 's'){
    //if first word is s read speed and coor and adopt this value to control motor and steering control
   
    if (data[data_length-1] == 'f')
    {
    // if last word is f stop reading 
      temp = data.substring(1,data_length-1);
      // ,의 index를 찾음
      int divide = temp.indexOf(",");
      temp_2 = temp.substring(0,divide);
      // data 형태가 speed, coor순으로 주어짐
      car_speed = temp_2.toInt();
      temp_2 = temp.substring(divide+1,data_length);
      car_coor = temp_2.toInt();
      
      data = "";
      // clear data
      //finish
    }
   }
  // speed control
  motor_forward(motorA1, motorA2, car_speed);
  motor_forward(motorA3, motorA4, car_speed);
  
  // val = Potentiometer vale
  if(val < car_coor)
  {
    // Read potentiometer value and adjust coor
  val = potentiometer_Read(analogPin); 
  analogWrite(motorDirection1Pin, LOW);
  analogWrite(motorDirection2Pin, 100);
  }
  else if(val>car_coor)
  {
    // Read potentiometer value and adjust coor
  val = potentiometer_Read(analogPin); 
  analogWrite(motorDirection1Pin, 100);
  analogWrite(motorDirection2Pin, LOW);
  }
  else if(val == car_coor)
  {
  val = potentiometer_Read(analogPin); 
  
  analogWrite(motorDirection1Pin, LOW);
  analogWrite(motorDirection2Pin, LOW);
  
  }
  


  
}

const int trigpin = 11;
const int echopin = 12;
float filtervalue = 0;
float sensitivity = 0.1;
long duration;
long distance;
float oldvalue;

void setup() {
  pinMode(trigpin, OUTPUT);
  pinMode(echopin, INPUT);
  Serial.begin(9600);
}

void loop() {
  ready_ultra(trigpin);

  duration = pulseIn(echopin, HIGH);
  distance = (duration/2) / 29.1;
  filtervalue = 0;
  // for (int i=0; i<100; i++){
  //   filtervalue += distance;
  //   delay(10);
  // }
  
  // float new_dist = (filtervalue/100) * (1 - sensitivity) + distance * sensitivity;
  float class_filter = low_pass(distance);

  Serial.print("Non-filtered : ");
  Serial.print(distance);
  Serial.print(" cm\t");

  Serial.print("Filtered : ");
  Serial.print(class_filter);
  Serial.print(" cm\t");

  Serial.print("Error rate : ");
  Serial.print(abs(class_filter-distance)/distance*100);
  Serial.println("%");

  // Serial.print("Filtered : ");
  // Serial.print(filtervalue/100);
  // Serial.print(" cm\t");

  // Serial.print("new dist : ");
  // Serial.print(new_dist);
  // Serial.print(" cm\t");

  // Serial.print("Error : ");
  // Serial.println(abs(filtervalue/100 - new_dist));
  
  oldvalue = distance; // Should have to consider older value
  delay(200); 
}

void ready_ultra(int trigpin){
  digitalWrite(trigpin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigpin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigpin, LOW);
}

float low_pass(float input){
  float output = sensitivity * input + (1-sensitivity) * oldvalue;
  return output;
}

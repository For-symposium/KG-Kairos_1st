const int interruptPin = 2;
const int led = 9;
volatile int interruptCount = 0;
bool state = false;
unsigned long lasttime = 0;

void setup(){
  pinMode(interruptPin, INPUT_PULLUP);
  pinMode(led, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), interruptFunction, FALLING);
  Serial.begin(115200);
}

void loop(){
  if (state == true){
    digitalWrite(led, HIGH);
  } 
  else if (state == false){
    digitalWrite(led, LOW);
  } 
}

void interruptFunction(){
  unsigned long interruptTime = millis();
  if (interruptTime - lasttime > 200){
    state = !state;
    lasttime = interruptTime;
  }

  if (state) {
    Serial.println("HIGH");
  }
  else {
    Serial.println("LOW");
  }
}


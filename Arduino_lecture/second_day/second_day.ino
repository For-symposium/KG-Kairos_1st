const int button = 2;
const int led_pin = 9;
bool curr = false;
// noInterrupts()

void interruptFunction(){
  curr = !curr;
}

int mapp(int var, int a1, int a2, int b1, int b2){
  return (float)(abs(b1-b2))/(abs(a1-a2)) * var;
}

void setup() {
  Serial.begin(115200);
  pinMode(led_pin, OUTPUT);
  pinMode(button, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(button), interruptFunction, FALLING);
}

void loop() {
  int read = analogRead(A0);
  int mapped_read = mapp(read, 0, 1023, 0, 255);

  if (curr == true){
    // digitalWrite(led_pin, HIGH);
    Serial.print(map(read, 0, 1023, 0, 255));
    Serial.print("\t");
    Serial.println(mapp(read, 0, 1023, 0, 255));
    
    // blooming은 analogWrite, not digitalWrite
    analogWrite(led_pin, mapped_read);
  }
  else {
    digitalWrite(led_pin, LOW);
  }
}

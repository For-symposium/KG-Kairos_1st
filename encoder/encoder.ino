int encoder = 2;

volatile int count = 0;
unsigned long oldTime = 0;
unsigned long newTime = 0;

void ISRencoder(){
  count++;
}

void setup() {
  Serial.begin(115200);
  pinMode(encoder, INPUT_PULLUP);
  attachInterrupt(INT1, ISRencoder, FALLING);
}

void loop() {
  newTime = millis();
  if (newTime - oldTime > 100){
    oldTime = newTime;
    // noInterrupts();
    Serial.println(count);  
    // interrupts();
  }
}

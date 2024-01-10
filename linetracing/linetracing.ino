int pin = 7;

void setup() {
  // put your setup code here, to run once:
  // pinMode(pin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(digitalRead(pin));
}

char cmd;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available()){
    cmd = Serial.read();

    switch (cmd){
      case 'a':
        Serial.println("Cmd : a");
        digitalWrite(13, HIGH);
        delay(100);
        break;

      case 'b':
        Serial.println("Cmd : b");
        digitalWrite(13, LOW);
        delay(100);
        break;
        
      default:
        Serial.println("Default");
        delay(100);
        break;
    }

    // if (cmd == 'a'){
    //   Serial.println("Cmd : a");
    //   digitalWrite(13, HIGH);
    //   delay(100);
    // }
    // else if (cmd == 'b'){
    //   Serial.println("Cmd : b");
    //   digitalWrite(13, LOW);
    //   delay(100);
    // }
    // else {
    //   Serial.println("except");
    //   delay(100);
    // }

  }
}

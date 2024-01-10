int motor1 = 9;
int motor2 = 10;
int button = 2;
bool state = false;
bool last_state;

void setup() {
  Serial.begin(115200);
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(button, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(button), interruptFunction, FALLING);
}

void loop() {
  if (Serial.available()){
    char readval = Serial.read();

    if (readval == '1'){ // button high
      analogWrite(motor1, 100); // forward
      analogWrite(motor2, LOW);
      Serial.println("a");
    }

    else if (readval == '2') { // button low
      analogWrite(motor1, LOW); // backward
      analogWrite(motor2, 100);
      Serial.println("b");
    } 

    else if (readval == '0'){ // stop
      analogWrite(motor1, LOW);
      analogWrite(motor2, LOW);
      Serial.println("c");
    }

    String readString = Serial.readString();
    int start = readString.indexOf('a');
    int mid = readString.indexOf('b');
    int end = readString.indexOf('c');
    String readdir = readString.substring(start+1, mid);
    String readSpeed = readString.substring(mid+1, end);
    int readSpeed_ = readSpeed.toInt();
    Serial.println(readdir);
    Serial.println(readSpeed_);
    
    
    if (readdir == '3'){
      analogWrite(motor1, readSpeed_);
      analogWrite(motor2, LOW);
    }
    else if (readdir == '4'){
      analogWrite(motor1, LOW);
      analogWrite(motor2, readSpeed_);
    }
  }
}


void interruptFunction(){
  state = !state;
  Serial.println(state);
}
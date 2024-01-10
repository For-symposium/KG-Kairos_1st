int led[6] = {12, 11, 10, 9, 8, 7};

class led_class{
  public:
  led_class(int pin_){
    pin = pin_;
  }
  int pin;

  void turnOn(){
    digitalWrite(pin, 20);
    Serial.println("on");
  }
  void turnOff(){
    digitalWrite(pin, LOW);
    Serial.println("off");
  }
  private:
};

class led_turn{
  public:
  led_class* leds;
  int num_leds;

  led_turn(led_class* led_array, int n) : leds(led_array), num_leds(n) {}

  void autocontrol(){
    for (int i=0; i<num_leds; i++){
      leds[i].turnOn();
      delay(100);
      leds[i].turnOff();
      delay(100);
    }
  }
};

led_class l0(led[0]);
led_class l1(led[1]);
led_class l2(led[2]);
led_class l3(led[3]);
led_class l4(led[4]);
led_class l5(led[5]);

led_class led_array[] = {l0, l1, l2, l3, l4, l5};

led_turn led_control(led_array, 6);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  for (int i=0; i<6; i++){
    pinMode(led_array[i].pin, OUTPUT);
  }
  
  // l1.setPin2(10);
  // Serial.println(l1.getPin2());
}

void loop() {
  // l0.turnOn();
  // delay(100);
  // l0.turnOff();
  // delay(100);

  // l1.turnOn();
  // delay(100);
  // l1.turnOff();
  // delay(100);

  led_control.autocontrol();
}

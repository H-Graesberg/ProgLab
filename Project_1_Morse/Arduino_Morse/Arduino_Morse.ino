const int button = 7;
const int dot = 2;
const int dash = 8;
//pins in use on the arduino

int counter = 0;
int old_count = 0;
int current_count = 0;
//variables for button_low (button pressed)


int pauseCounter = 0;
int old_count1 = 0;
int pause = 0;
//variables for button_high (button not pressed)

int wait = 100;
//variable for delay

void setup() {
  Serial.begin(9600);
  
  pinMode(dot, OUTPUT);
  pinMode(dash, OUTPUT);
  pinMode(button, INPUT);

}

void loop() {
  
  if (digitalRead(button) == LOW) { //When button is low(not pressed)
    pauseCounter = millis();        
    pause = pauseCounter-old_count1; //the time it is not pressed
    
    if (pause >1200 && pause<=3000) {
      Serial.print(2);
  }
    if (pause>3000 && pause<=10000) {
      Serial.print(3);
  } 
  if (pause>10000) {
    Serial.print(4);
  }
  old_count1 = pauseCounter;  //"reset" old_count1 so the counting starts at 0 when not pressed
  delay(wait);
  }

  
  if (digitalRead(button) == HIGH) {  //Same as over just when butten is pressed
    
    counter = millis();
    current_count = counter - old_count;
    
    if (current_count > wait + 5){    //when pressed, a stream of signals around 100ms(delay) comes. This controls to just send signal when pressed.
      if (current_count <= 600) {
        Serial.print(0);
        digitalWrite(dot, HIGH); 
      }
      if ((current_count > 600) && (current_count <= 1200)) {
        Serial.print(1);
        digitalWrite(dash, HIGH);
      }
    }
  }
    
    old_count = counter;
    delay(wait);
    digitalWrite(dot, LOW);     //Turn the lights of, can be mooved inside if-sentences to keep light on until new signal
    digitalWrite(dash, LOW);    //Think it is better this way with just a flash for each signal.
    
  }
 
  

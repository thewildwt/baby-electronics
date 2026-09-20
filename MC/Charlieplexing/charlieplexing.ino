//constants
#define LED_DELAY 500

//declaration
int LED_PINS[] = { 2, 3, 4 };
int i = 0, j = 0;
unsigned long startmillis , currentmillis;
bool led_status[6];

//setup
void setup() {

  for (int a=0; a<6 ; a++) { // setting leds to off
    led_status[a] = false;
  }
  
  startmillis = millis(); // starting timer

}

//serial for led starts from 0
void lightled(int serial) { // to control lighting of individual led
  if (serial/2 == 0){
    pinMode(LED_PINS[0] , OUTPUT);
    pinMode(LED_PINS[1] , OUTPUT);
    pinMode(LED_PINS[2] , INPUT);

    if (serial%2 ==0) {
      digitalWrite(LED_PINS[0], HIGH);
      digitalWrite(LED_PINS[1], LOW);
    }
    else {
      digitalWrite(LED_PINS[1], HIGH);
      digitalWrite(LED_PINS[0], LOW);
    }
  }
  else if (serial/2 == 1) {
    pinMode(LED_PINS[0] , INPUT);
    pinMode(LED_PINS[1] , OUTPUT);
    pinMode(LED_PINS[2] , OUTPUT);

    if (serial%2 ==0) {
      digitalWrite(LED_PINS[1], HIGH);
      digitalWrite(LED_PINS[2], LOW);
    }
    else {
      digitalWrite(LED_PINS[2], HIGH);
      digitalWrite(LED_PINS[1], LOW);
    }

  }
  else {
    pinMode(LED_PINS[0] , OUTPUT);
    pinMode(LED_PINS[1] , INPUT);
    pinMode(LED_PINS[2] , OUTPUT);

      if (serial%2 ==0) {
      digitalWrite(LED_PINS[2], HIGH);
      digitalWrite(LED_PINS[0], LOW);
    }
    else {
      digitalWrite(LED_PINS[0], HIGH);
      digitalWrite(LED_PINS[2], LOW);
    }
  }
}

void ledcycle(){ //main led pattern logic
  for (int k=0; k<6 ; k++) { //cycling led's that are on
    if (led_status[k] == true) {
      lightled(k);
    }
  }

  currentmillis = millis();

  if (currentmillis - startmillis > LED_DELAY) { // checking for led's to change
    if ( i < 6) {
      if ( j < 6-i) {
        if (j != 0) {
          led_status[6-j] = false; // turning off last led
        }
        led_status[5-j] = true; 
        startmillis = millis();
        j++;
      }
      else { // j loop is completed
      j=0;
      i++;      
      }
    }
    else { //restarting loop
      i=0;
      j=0;
      for (int a=0; a<6 ; a++) {
        led_status[a] = false;
      }
    }
  }

}


// main loop
void loop() {
  ledcycle();
}

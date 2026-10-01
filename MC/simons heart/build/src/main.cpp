#include <Arduino.h>


// pin constants
const int BUTTON_PINS[] = {2, 3, 4, 5}; // Define button pins
const int LED_PINS[] = {6, 7, 8, 9}; // Define LED pins
const int LED_HB_PIN = 10; // define heartbeat pin

//timers
unsigned long gamestart , gamecurrent;
unsigned long hbstart , hbcurrent;
unsigned long ledstart , ledcurrent;

//game
const int MAX_GAME_LENGTH = 100;
int sequence_count = 1;
int sequence[MAX_GAME_LENGTH] = {0};
const unsigned int GAME_SPEED = 550;
const int diff = 50;
unsigned int gamespeed = GAME_SPEED;


//game_flags
bool led_waiting = false;
bool game_start = false;
bool game_over = false;

int led_num;
int game_stage;
int button_num;



//buttons
int button[4] ={HIGH};
int button_old[4] = {HIGH};


//reads the input from the buttons
void buttons_read() {
  for(int i = 0 ; i < 4 ; i++) {
    int state = digitalRead(BUTTON_PINS[i]);
    if (state == button_old[i]) {
      if((button_old[i]) == LOW) {
        button[i] = HIGH;
      }
    }
    else {
      button[i] = state;
      button_old[i] = state;
      
    }
  }
}

// deals with lighting the led and the time they are on
void lightled(int pin) {
  if (led_waiting == false) {
    ledstart = millis();
    led_waiting = true;
  }
  
  if (((ledcurrent = millis()) - ledstart) >= gamespeed) {
    digitalWrite(LED_PINS[pin], LOW);
    
    if (ledcurrent - ledstart >= gamespeed*1.5){
      led_waiting = false;
      if (led_num < sequence_count-1) {
        led_num++; //next led
      }
      else{
        game_stage++; //intiialises next stage
        button_num = 0; //initialises button count
      }
    }

  }
  else{
      digitalWrite(LED_PINS[pin], HIGH);
  }
  
}

//checks the order in which buttons are pressed
void buttons_check(){
   for (int i = 0; i < 4; i++) {
    if (button[i] == LOW){
      if(i == sequence[button_num]) {
        if (button_num < sequence_count-1) {
        button_num++; //next press
        }
        else{
          game_stage++; //intiialises next stage
        }  
      }
      else{
        game_start = false;
        break;
        
      }
    }
  }
}


void game(){
  if (game_start == true) {
    switch(game_stage) {
      
      case 0: //game starts
        
        game_stage++; // next stage
        led_num = 0; // initialises next led

        sequence[sequence_count-1] = random(4); //adds the next random led
        for (int i=0; i<sequence_count; i++){
          Serial.print(sequence[i]);
        }
        Serial.println("");
        
        break;
        

      case 1: //lighting the leds
        lightled(sequence[led_num]);
        break;

      case 2: //checking button sequence
        buttons_check();
        break;

      case 3: //game restarts or stops
        if (gamespeed - diff > 0) { // linearly increases difficulty 
          gamespeed -= diff ;
          }
        sequence_count++; //increases sequence size
        game_stage = 0;
        break;
  
    }
  }
  else {
    for (int i = 0 ; i < 4; i++){
      if (button[i] == LOW) {
        game_start = true;
        game_stage = 0;
        gamespeed = GAME_SPEED;
        sequence_count = 1;
        break;
      }
    }
  }
  gamestart = millis();
}



// for the heartbeat
void heartbeat() {
  if((hbcurrent = millis()) - hbstart >= 1000) {
    if((hbcurrent = millis()) - hbstart <= 1200) {
      digitalWrite(LED_HB_PIN, HIGH);
    }
    else {
      digitalWrite(LED_HB_PIN, LOW);
      hbstart = millis();
    }
  }
}


void setup() {
  Serial.begin(115200); // serial monitor

  
  // setting up the pins
  for(int i = 0; i<4 ; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    pinMode(BUTTON_PINS[i] , INPUT_PULLUP);

    //sets up interrupts
    //attachInterrupt (digitalPinToInterrupt(BUTTON_PINS[i]), loop, CHANGE);
  }

  pinMode(LED_HB_PIN , OUTPUT);

  //timers
  hbstart = millis();
  gamestart = millis();


  // Seed the random generator using an empty analog pin
  randomSeed(analogRead(A0)); 
}

void loop() {
  buttons_read();
  game();
  heartbeat();
}




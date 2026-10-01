#include <Arduino.h>
#include <Servo.h>
#include <math.h>


Servo servo;  // create servo object to control a servo

//pins
const int SERVO_PIN = 3;
const int LED_PIN = 4;
const int sensor[2] = {A0 ,A1};

//reading variables
int readings[2];
int mean_flicker;
int reading;

//calculate constants
const int tolerance = 20;


const int stack_size = 5;
int pastdiff[stack_size] = {0};



//takes the readings from the sensors
void take_readings() {
  for(int i = 0; i < 2 ; i++){
    readings[i] = analogRead(sensor[i]);            // reads the value of the potentiometer (value between 0 and 1023)
    readings[i] = map(readings[i], 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
  }
}

void filo(int num){ //first in last out stack
  for (int i = stack_size-1 ; i > 0; i--) {
    pastdiff[i] = pastdiff[i-1];
  }
  pastdiff[0] = num; 
}

void flicker(){ // calculate mean flicker
  
  
  int diff = abs(readings[0] - readings[1]);
  filo(diff);
  long flicker = 0;
  for (int i = 0 ; i < stack_size; i++){
    flicker += pastdiff[i];
  }
  mean_flicker = flicker/stack_size;
  Serial.println(mean_flicker);
}



//calulates the final value
void function(){

  if (mean_flicker < tolerance){
    digitalWrite(LED_PIN, LOW);
    reading = (abs(readings[0] + readings[1]))/2;
    servo.write(reading); // sets the servo position according to the scaled value
  }
  else {
    digitalWrite(LED_PIN, HIGH);
  }
}

void setup() {
  Serial.begin(115200);
  servo.attach(SERVO_PIN);
}

void loop() {

  take_readings();
  flicker();
  function();
  delay(15);
}

#include <LiquidCrystal_I2C.h>
#include <Arduino.h>


//for the display
#define I2C_ADDR    0x27
#define LCD_COLUMNS 20
#define LCD_LINES   4

LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLUMNS, LCD_LINES);

// for the buttons

int pins[] = {2,4};
int button_idle = LOW;

int button_1 = LOW;
int button_2 = LOW;



//timer
unsigned long timestart_delay , timecurrent_delay;
unsigned long timestart_pomo = 0 , timecurrent_pomo = 0;

bool timer_run = false;
bool timer_pause = false;
long timercount ;

// working of button
void buttons() {
  
  button_1 = digitalRead(pins[0]);
  button_2 = digitalRead(pins[1]); 

}


//for the working of display
void pomo() {
  

  if (button_1 == HIGH) {   // start and pause button
    
    if (timer_run ==false) {
      timer_run = true;
      
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Timer started");
    }
    else {
      timer_pause = !timer_pause;
    }

  }

  if (button_2 == HIGH) {  // stop button
    timer_run = false;
    timercount = 0;

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Timer stopped!");
  }
  
  
  if (timer_run == true) {   //timer logic
    
    if (timer_pause == false) {
      
      timecurrent_pomo = millis();
      timercount += timecurrent_pomo - timestart_pomo;
      Serial.println(timercount);
      timestart_pomo = timecurrent_pomo;
      
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("elapsed:");
      lcd.setCursor(10, 0);
      lcd.print((timercount/1000)/60);

      lcd.setCursor(0, 1);
      lcd.print("remaining:");
      lcd.setCursor(10, 1);
      lcd.print(25 - ((timercount/1000)/60));
      
      if ((25 - ((timercount/1000)/60)) <= 0) {
        
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("take a break");
        
        timer_run = false;
        timercount = 0;

      }
    }
    else {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Timer Paused!");
    }
  }
  else {
    lcd.setCursor(0, 0);
    lcd.print("Press the button");
  }

}


void setup() { //setup
  //serial
  Serial.begin(115200);
  
  //timers
  timestart_delay = millis();
  
  
  //init buttons
  pinMode(pins[0], INPUT);
  pinMode(pins[1], INPUT);
  
  // Init display
  lcd.init();
  lcd.backlight();
}

void loop() { //loop
  timecurrent_delay = millis();
    if ((timecurrent_delay - timestart_delay) > 100) {
      
      buttons();
      pomo();
      
      timestart_delay = millis();  
  }
}

//Libraries
#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Tiny4kOLED.h>
#include <math.h>

Adafruit_MPU6050 mpu;

int LED_PINS[] = {3,5,6};

float accX , accY , accZ , gyroX , gyroY , gyroZ;

unsigned long start_time_gyro, current_time_gyro;



//prepare oled display

void prepareDisplay() {
  oled.clear();
  oled.begin();

  oled.setCursor(20, 1);
  oled.print(F("X: "));
  oled.setCursor(20, 2);
  oled.print(F("Y: "));
  oled.setCursor(20, 3);
  oled.print(F("Z: "));
}


// first method - integration of gyroscope results

float gyroX_initial = 0.0, gyroY_initial = 0.0, gyroZ_initial = 0.0;
float angX = 0, angY = 0 , angZ = 0;

void gyrocalculate() {
  current_time_gyro = millis();

  angX += gyroX*(current_time_gyro - start_time_gyro)/20;
  if (angX > 360) {
      angX = fmod(angX, 360);
  }
  else if (angX < 0) {
      angX += 360;
  }
  angY += gyroY*(current_time_gyro - start_time_gyro)/20;
  if (angY > 360) {
      angY = fmod(angY, 360);
  }
  else if (angY < 0) {
      angY += 360;
  }
  angZ += gyroZ*(current_time_gyro - start_time_gyro)/20;
  if (angZ > 360) { 
      angZ = fmod(angZ, 360);
  }
  else if (angZ < 0) {
      angZ += 360;
  }
  
  start_time_gyro = millis();
}

//danger levels led

void dangerlevels() {
  if (angX >= 90 && angX <= 180) {
    int X_reading = map(angX , 90 , 180 , 0 , 255);
    analogWrite(LED_PINS[0], X_reading);
  }
  if (angY >= 90 && angY <= 180) {
    int Y_reading = map(angY , 90 , 180 , 0 , 255);
    analogWrite(LED_PINS[1], Y_reading);
  }
  if (angZ >= 90 && angZ <= 180) {
    int Z_reading = map(angZ , 90 , 180 , 0 , 255);
    analogWrite(LED_PINS[2], Z_reading);
  }
  
}


void setup() {
  // IMU
  start_time_gyro = millis();
  
  Serial.begin(115200);
  
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  //oled
  oled.begin(128, 64, sizeof(tiny4koled_init_128x64br), tiny4koled_init_128x64br);

  oled.setFont(FONT6X8);

  oled.clear(); // To clear all the memory
  oled.on();
  prepareDisplay();
}

void loop() {
  sensors_event_t a, g, temp; //get new sensor readings
  mpu.getEvent(&a, &g, &temp);

  accX = a.acceleration.x; // getting values from sensors
  accY = a.acceleration.y;
  accZ = a.acceleration.z;
  gyroX = g.gyro.x;
  gyroY = g.gyro.y;
  gyroZ = g.gyro.z;

  gyrocalculate(); 
  dangerlevels(); //check danger levels and light up leds accordingly


  //oled display write
  oled.setCursor(30, 1);
  oled.print(angX, 1);
  oled.setCursor(30, 2);
  oled.print(angY, 1);
  oled.setCursor(30, 3);
  oled.print(angZ, 1);



}

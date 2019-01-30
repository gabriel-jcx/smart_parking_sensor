// **** INCLUDES *****
#include "LowPower.h"
#include <NewPing.h>
#include <avr/sleep.h>
#include <avr/power.h>

#define TRIGGER_PIN  12
#define ECHO_PIN     11
#define MAX_DISTANCE 200 //cm
#define SR04_PIN 9

#define ACK_PIN 7

const int wakeUpPin =  13;      // the number of the LED pin
const int spotStatus =  8;      // the number of the LED pin

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
int distance;

char curr_state;
char prev_state;

int timeout = 0;

void setup() {
  CLKPR = 0x80;
  CLKPR = 0x00;

  curr_state = 0;
  prev_state = 0;
  
  Serial.begin(115200);
  // initialize the LED pin as an output:
  pinMode(wakeUpPin, OUTPUT);
  pinMode(spotStatus, OUTPUT);
  pinMode(SR04_PIN, OUTPUT);
  pinMode(ACK_PIN, INPUT);
  
  ADCSRA = 0;
  power_adc_disable(); // ADC
  power_spi_disable(); // SPI
  power_twi_disable(); // TWI (I2C)
}


void loop() {
  //digitalWrite(SR04_PIN,HIGH);
  delay(50);
  Serial.print("Ping: ");
  distance = (sonar.ping_cm() + sonar.ping_cm())/2;
  Serial.print(distance);
  Serial.println("cm");

  
  if ((0 < distance) && (distance < 20)){
    Serial.println("Spot taken");
    curr_state = 0xFF;
    digitalWrite(spotStatus, HIGH);
    //delay(500);
    
  } else {
    Serial.println("Spot not taken.");
    curr_state = 0x00;
    digitalWrite(spotStatus, LOW);
  }

  if( curr_state != prev_state) {
    Serial.println("Spot status changed!");
    digitalWrite(wakeUpPin, HIGH);
    
    while(!digitalRead(ACK_PIN) && (timeout < 20000)){
      delay(1);
      timeout++;
    }
    
    if(timeout >= 20000){
      Serial.print("ERROR: ACK timedout");
    } else {
      Serial.print("Rec ACK signal in ");
      Serial.print(timeout);
      Serial.println(" ms");
    }
    digitalWrite(wakeUpPin, LOW);
    timeout = 0; 
  } else {
    digitalWrite(wakeUpPin, LOW);
    
  }
  prev_state = curr_state;
  //digitalWrite(SR04_PIN,LOW);
  delay(10);
  LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF); 
}



//uses a hard coded spot id instead of MAC address

#include <Adafruit_NeoPixel.h>

#define PIN 14
#define NUM_LED 85
// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LED, PIN, NEO_RGBW + NEO_KHZ800);

#define SLEEP

#ifdef SLEEP
  #include "esp_sleep.h"
  
  #define GPIO_DEEP_SLEEP_DURATION     4  // sleep 2 seconds and then wake up
  RTC_DATA_ATTR static time_t last;        // remember last boot in RTC Memory
  RTC_DATA_ATTR static uint32_t bootcount; // remember number of boots in RTC Memory
#endif




// --- PIN DEF ---
#define  TRIGGER 26
#define  ECHO    27



long duration;
int  distance;


RTC_DATA_ATTR static char curr_state;
RTC_DATA_ATTR static char prev_state;

void setup() {
  Serial.begin(115200);
  
  Serial.printf(" --------- End of Sleep ---------\n\n",bootcount);
  Serial.printf("\n --------- Bootcount: %d ---------\n",bootcount);
  Serial.printf(" Curr_state: %d,Prev_state: %d\n",curr_state,prev_state);

  //SR04 pins
  pinMode(TRIGGER , OUTPUT);
  pinMode(   ECHO , INPUT );

  //LED Strip setup
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'


}


void loop(){

  curr_state = spotStatus(); //0xFF == taken, 0x00 == empty



  //  --------- turn on WiFi and/or Bluetooth if needed -------
  if( ( curr_state != prev_state ) || ((bootcount % 10) == 0) ) {

    if ( (curr_state == 0xFF) && prev_state == 0x00 ){
      colorWipeUCSC(1);
    } else { 
      Serial.println("\n Getting New Tasks");
    }

  } else {
      GoToSleep(GPIO_DEEP_SLEEP_DURATION);
  }


  delay(5000);
  if(curr_state == 0xFF) {
    if(bootcount % 2 == 0) {
      colorWipeGreen(10);
      delay(8000);
      strip.clear();
    } else {
      colorWipeRed(10);
      delay(8000);
      strip.clear();
    }
  }

  prev_state == curr_state;
  GoToSleep(GPIO_DEEP_SLEEP_DURATION);
  
}

void GoToSleep(int timer) {
    //colorWipe(strip.Color(0, 0, 0), 50);
    strip.clear();
    bootcount++;
    Serial.printf("\n --------- Entering deep sleep ---------\n");
    delay(50);
    esp_deep_sleep(1000000LL * timer);
}




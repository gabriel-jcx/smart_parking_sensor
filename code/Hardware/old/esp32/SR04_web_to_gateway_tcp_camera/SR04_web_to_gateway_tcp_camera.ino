

//WIFI libaries
#include <WiFi.h>
#include <WiFiMulti.h>

//CAMERA Libaries
#include "BMP.h"
#include "OV7670.h"
#include <Adafruit_GFX.h>    // Core graphics library


//uses a hard coded spot id instead of MAC address
#define HARD_CODE_ADDR 1

#define BT
#define SLEEP

// --- BLUETOOTH DEF ---

#ifdef BT
  #include "BLEDevice.h"
  #include "BLEServer.h"
  #include "BLEUtils.h"
  
  
  #ifdef SLEEP
    #include "esp_sleep.h"
    
    #define GPIO_DEEP_SLEEP_DURATION     4  // sleep 2 seconds and then wake up
    RTC_DATA_ATTR static time_t last;        // remember last boot in RTC Memory
    RTC_DATA_ATTR static uint32_t bootcount; // remember number of boots in RTC Memory
  #endif
  
  #ifdef __cplusplus
  extern "C" {
  #endif
  
  #ifdef __cplusplus
  }
  #endif
  
  // See the following for generating UUIDs:
  // https://www.uuidgenerator.net/
  BLEAdvertising *pAdvertising;
  //struct timeval now;
#endif


// --- PIN DEF ---
#define  TRIGGER 26
#define  ECHO    27

#define  RED     14
#define  GREEN   12
#define  BLUE    13


// --- PIN CAMERA ---

const int SIOD = 21; //SDA
const int SIOC = 22; //SCL

const int VSYNC = 34;
const int HREF = 35;

const int XCLK = 32;
const int PCLK = 33;

const int D0 = 25; //27
const int D1 = 2; //17
const int D2 = 18;//16
const int D3 = 15;
const int D4 = 19;//14
const int D5 = 5; //13
const int D6 = 23;//12
const int D7 = 4;

//Camera objects
OV7670 *camera;
unsigned char bmpHeader[BMP::headerSize];




long duration;
int  distance;


RTC_DATA_ATTR static char curr_state;
RTC_DATA_ATTR static char prev_state;


uint64_t chipid; //Stores MAC Address
char macAddr[12];
int len;

const char* ssid     = "pi_gateway_1";
const char* password = "12341234";

const uint16_t port = 6001;
const char * host = "10.3.141.1"; // ip or dns

WiFiMulti WiFiMulti;

void setup() {
  Serial.begin(115200);
  
  Serial.printf(" --------- End of Sleep ---------\n\n",bootcount);
  Serial.printf("\n --------- Bootcount: %d ---------\n",bootcount);
  Serial.printf(" Curr_state: %d,Prev_state: %d\n",curr_state,prev_state);

  
  //SPOT ID Setup  
  chipid=ESP.getEfuseMac();//The chip ID is essentially its MAC address(length: 6 bytes).
  Serial.printf(" ESP32 Chip ID = %04X%08X\n",(uint16_t)(chipid>>32),(uint32_t)chipid);//print 6 byte MAC address

  #ifdef HARD_CODE_ADDR
  len = sprintf(macAddr, "%d",HARD_CODE_ADDR);
  #else
  len = sprintf(macAddr, "%04X%08X",(uint16_t)(chipid>>32),(uint32_t)chipid);
  #endif
    
  //Camera setup
  camera = new OV7670(OV7670::Mode::QQVGA_RGB565, SIOD, SIOC, VSYNC, HREF, XCLK, PCLK, D0, D1, D2, D3, D4, D5, D6, D7);
  BMP::construct16BitHeader(bmpHeader, camera->xres, camera->yres);
  

  #ifdef BT    
    // Create the BLE Device
    BLEDevice::init("ESP32");
    
    // Create the BLE Server
    BLEServer *pServer = BLEDevice::createServer();
    
    pAdvertising = pServer->getAdvertising();
  #endif

  //SR04 pins
  pinMode(TRIGGER , OUTPUT);
  pinMode(   ECHO , INPUT );
  //RGB pins
  pinMode(   BLUE , OUTPUT);
  pinMode(  GREEN , OUTPUT);
  pinMode(    RED , OUTPUT);

}


void loop(){

  int try_again = 0; //Used if TCP failed to connect
  int timeout = 0;   //Used if WiFi falid to connect


  //Check to see if a car is in the spot
  curr_state = spotStatus(); //0xFF == taken, 0x00 == empty

  // Use WiFiClient class to create TCP connections
  WiFiClient client;



  //  --------- turn on WiFi and/or Bluetooth if needed -------
  if( ( curr_state != prev_state ) || ((bootcount % 10) == 0) ) {

    if ( (curr_state == 0xFF) && prev_state == 0x00 )  
      setBeacon(); //Turn on the 
    else 
      Serial.println("\n Getting New Tasks");
    
    // We start by connecting to a WiFi network
    WiFi.begin(ssid, password);
    Serial.printf(" connecting to %s\n",host);
    Serial.print(" Wait for WiFi");
    delay(10);
    
    while (WiFi.status() != WL_CONNECTED && (timeout++ < 40)) {
        Serial.print(".");
        delay(250);
    }

    
    if(timeout >= 40) {
      //bootcount++;
      Serial.print("\n TIMEOUT: Could not connect to WiFi\n");
      GoToSleep(1); //1 sec
    } 
        
    printf("\n Took %.2f seconds to connect.\n\n", ((float)timeout)/4);
    delay(200);

  } else {
      GoToSleep(GPIO_DEEP_SLEEP_DURATION);
  }

  //Either the spot status has changed or (bootcount % 10) == 0

  if( curr_state != prev_state ) {
    Serial.println(" States changed.");
    //open a connection to the gateway
    if (!client.connect(host, port)) { //change this to a while loop
      Serial.println(" connection failed");
      Serial.println(" wait 1 sec...");
      delay(1000);
      return;
    }

    //send a message
    if( curr_state == 0xFF) {
      client.printf("%s,StatusChanged,taken",macAddr);
      Serial.printf(" Sent: %s,StatusChanged,taken\n",macAddr);

      
      
    } else {
      digitalWrite(RED,LOW);
      digitalWrite(GREEN,LOW);
      client.printf("%s,StatusChanged,empty",macAddr);
      Serial.printf(" Sent: %s,StatusChanged,empty\n",macAddr);
    }


    
    
    while (client.connected()){
      char c = client.read(); //read a char
      if(c == '#'){ //start of a message
        c = client.read();

        if (c == 'P') {
          //client.printf("%s,Picture,taken",macAddr);
          //Serial.printf("%s,Picture,taken\n",macAddr);
          
          TakePic();
          
//          for(int i = 0; i < BMP::headerSize; i++)
//            client.write(bmpHeader[i]);
//          for(int i = 0; i < camera->xres * camera->yres * 2; i++)
//            client.write(camera->frame[i]);

          client.write(bmpHeader, BMP::headerSize);
          client.write(camera->frame, camera->xres * camera->yres * 2);
          delay(10);  
          Serial.printf("Finished sending Picture.\n");
          client.stop();
          delay(10);
          client.connect(host, port);
          delay(10);
          client.printf("%s,Auth,taken",macAddr);
          
        } else if (c == 'A') {
            digitalWrite(RED,LOW);
            if (curr_state == 0xFF) digitalWrite(GREEN,HIGH);
            Serial.println(" Got ACK \n Closing connection");
            client.stop();
            prev_state = curr_state;
            delay(4000);
            try_again = 0;
        } else if (c == 'D') {
            digitalWrite(RED,HIGH);
            digitalWrite(GREEN,LOW);
            Serial.println(" Got ACK \n Closing connection");
            client.stop();
            prev_state = curr_state;
            delay(4000);
            try_again = 0;
        }
      } else {
        try_again = 1;
      }
    }
  } else if ((bootcount % 10) == 0){
    if (!client.connect(host, port)) { //change this to a while loop
      Serial.println(" connection failed");
      Serial.println(" wait 1 sec...");
      delay(1000);
      return;
    }
    if(curr_state == 0xFF) {
      Serial.printf(" Sent:%s,AnyTasks,taken\n",macAddr);
      client.printf("%s,AnyTasks,taken",macAddr);
    } else {
      Serial.printf(" Sent:%s,AnyTasks,empty\n",macAddr);
      client.printf("%s,AnyTasks,empty",macAddr);
    }
    delay(100);
    
    while (client.connected()){
      char c = client.read(); //read a char
        if(c == '#'){ //start of a message
            c = client.read();
            if (c == 'T') {
                Serial.println(" Got ACK \n Closing connection");
                client.stop();
                prev_state = curr_state;
                delay(100);
                try_again = 0;
            }
          } else if (c == 'P') {
          client.printf("%s,Picture,taken",macAddr);
          Serial.printf("%s,Picture,taken\n",macAddr);
          delay(10);
          TakePic();
          
//          for(int i = 0; i < BMP::headerSize; i++)
//            client.write(bmpHeader[i]);
//          for(int i = 0; i < camera->xres * camera->yres * 2; i++)
//            client.write(camera->frame[i]);
          client.write(bmpHeader, BMP::headerSize);
          client.write(camera->frame, camera->xres * camera->yres * 2);
          
          Serial.printf("Finished sending Picture.\n");
          client.stop();
          } else {
            try_again = 1;
          }
    }
  }

  
  if(try_again != 1){
    //bootcount++;
    client.stop();
    pAdvertising->stop();
    GoToSleep(GPIO_DEEP_SLEEP_DURATION);
  } else {
    Serial.print(" Trying again");
    delay(100);
  }
  
}

void GoToSleep(int timer) {
    bootcount++;
    Serial.printf("\n --------- Entering deep sleep ---------\n");
    delay(50);
    esp_deep_sleep(1000000LL * timer);
}

void TakePic () {
     camera->oneFrame();
     delay(10);
    camera->oneFrame();
}



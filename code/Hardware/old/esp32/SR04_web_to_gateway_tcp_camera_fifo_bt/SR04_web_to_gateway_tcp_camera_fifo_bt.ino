//CMPE 123 TEAM 3

//uses a hard coded spot id instead of MAC address
#define HARD_CODE_ADDR 2

#define BT        //enable bluetooth beacon
#define SLEEP     //enable sleep
#define HIGHREZ   //Send high rez image to gateway

//WIFI libaries
#include <WiFi.h>
#include <WiFiMulti.h>

//CAMERA Libaries
#include <Wire.h>
#include <ArduCAM.h>
#include <SPI.h>
#include "memorysaver.h"

#if !(defined ESP32 )
#error Please select the ArduCAM ESP32 UNO board in the Tools/Board
#endif
//This demo can only work on OV2640_MINI_2MP or ARDUCAM_SHIELD_V2 platform.
#if !(defined (OV2640_MINI_2MP)||defined (OV5640_MINI_5MP_PLUS) || defined (OV5642_MINI_5MP_PLUS) \
    || defined (OV5642_MINI_5MP) || defined (OV5642_MINI_5MP_BIT_ROTATION_FIXED) \
    ||(defined (ARDUCAM_SHIELD_V2) && (defined (OV2640_CAM) || defined (OV5640_CAM) || defined (OV5642_CAM))))
#error Please select the hardware platform and camera module in the ../libraries/ArduCAM/memorysaver.h file
#endif

// set GPIO17 as the slave select :
const int CS = 17;
const int CAM_POWER_ON = 10;
#if defined (OV2640_MINI_2MP) || defined (OV2640_CAM)
  ArduCAM myCAM(OV2640, CS);
#elif defined (OV5640_MINI_5MP_PLUS) || defined (OV5640_CAM)
  ArduCAM myCAM(OV5640, CS);
#elif defined (OV5642_MINI_5MP_PLUS) || defined (OV5642_MINI_5MP) || defined (OV5642_MINI_5MP_BIT_ROTATION_FIXED) ||(defined (OV5642_CAM))
  ArduCAM myCAM(OV5642, CS);
#endif

static const size_t bufferSize = 2048;
static uint8_t buffer[bufferSize] = {0xFF};
uint8_t temp = 0, temp_last = 0;
int i = 0;
bool is_header = false;




#ifdef SLEEP
  #include "esp_sleep.h"
  
  #define GPIO_DEEP_SLEEP_DURATION     4  // sleep 2 seconds and then wake up
  RTC_DATA_ATTR static time_t last;        // remember last boot in RTC Memory
  RTC_DATA_ATTR static uint32_t bootcount; // remember number of boots in RTC Memory
#endif

// --- BLUETOOTH DEF ---

#ifdef BT
  #include "SimpleBLE.h"
  
  #if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
  #error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
  #endif
  SimpleBLE ble;
  
  String ble_name = "Spot:WR,";
#endif


// --- PIN DEF ---
#define  TRIGGER 26
#define  ECHO    27

#define  RED     14
#define  GREEN   12
#define  BLUE    13


long duration;
int  distance;


RTC_DATA_ATTR static char curr_state;
RTC_DATA_ATTR static char prev_state;


uint64_t chipid; //Stores MAC Address
char macAddr[12];
int len_mac;

const char* ssid     = "pi_gateway";
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
  len_mac = sprintf(macAddr, "%d",HARD_CODE_ADDR);
  ble_name += len_mac;
  #else
  len_mac = sprintf(macAddr, "%04X%08X",(uint16_t)(chipid>>32),(uint32_t)chipid);
  #endif
    
  
  //SR04 pins
  pinMode(TRIGGER , OUTPUT);
  pinMode(   ECHO , INPUT );
  //RGB pins
  pinMode(   BLUE , OUTPUT);
  pinMode(  GREEN , OUTPUT);
  pinMode(    RED , OUTPUT);


  uint8_t vid, pid;
  //uint8_t temp;
    //set the CS as an output:
    pinMode(CS,OUTPUT);
    pinMode(CAM_POWER_ON , OUTPUT);
    digitalWrite(CAM_POWER_ON, HIGH);
  #if defined(__SAM3X8E__)
  Wire1.begin();
  #else
  Wire.begin();
  #endif
  
  
  
  // initialize SPI:
  SPI.begin();
  SPI.setFrequency(4000000); //4MHz
  
  //Check if the ArduCAM SPI bus is OK
  myCAM.write_reg(ARDUCHIP_TEST1, 0x55);
  temp = myCAM.read_reg(ARDUCHIP_TEST1);
  if (temp != 0x55){
  Serial.println(F("SPI1 interface Error!"));
  while(1);
  }
  
  //Check if the ArduCAM SPI bus is OK
  myCAM.write_reg(ARDUCHIP_TEST1, 0x55);
  temp = myCAM.read_reg(ARDUCHIP_TEST1);
  if (temp != 0x55){
  Serial.println(F("SPI1 interface Error!"));
  while(1);
  }
  
  #if defined (OV2640_MINI_2MP) || defined (OV2640_CAM)
    //Check if the camera module type is OV2640
    myCAM.wrSensorReg8_8(0xff, 0x01);
    myCAM.rdSensorReg8_8(OV2640_CHIPID_HIGH, &vid);
    myCAM.rdSensorReg8_8(OV2640_CHIPID_LOW, &pid);
    if ((vid != 0x26 ) && (( pid != 0x41 ) || ( pid != 0x42 )))
      Serial.println(F("Can't find OV2640 module!"));
    else
      Serial.println(F("OV2640 detected."));
  #endif

  //Change to JPEG capture mode and initialize the OV2640 module
  #ifdef BMPIMG
    myCAM.set_format(BMP);
  #else
    myCAM.set_format(JPEG);
  #endif
  myCAM.InitCAM();

  #ifdef HIGHSREZ
    myCAM.OV2640_set_JPEG_size(OV2640_1600x1200);
  #else
    myCAM.OV2640_set_JPEG_size(OV2640_640x480);
  #endif
  myCAM.clear_fifo_flag();

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

    if ( (curr_state == 0xFF) && prev_state == 0x00 ){
    #ifdef BT  
      ble.begin(ble_name);
    #endif
    } else { 
      Serial.println("\n Getting New Tasks");
    }
    // We start by connecting to a WiFi network
    WiFi.begin(ssid, password);
    Serial.printf(" connecting to %s\n",host);
    Serial.print(" Wait for WiFi");
    delay(10);
    
    while (WiFi.status() != WL_CONNECTED && (timeout++ < 40)) {
        Serial.print(".");
        delay(250);
    }

    // timeout is 10 sec
    if(timeout >= 40) {
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

      
      
    } else {git 
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
          
          myCAM.clear_fifo_flag();
          start_capture();
          Serial.println(F("CAM Capturing"));
          
          int total_time = 0;
          
          total_time = millis();
          while (!myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));
          total_time = millis() - total_time;
          Serial.print(F("capture total_time used (in miliseconds):"));
          Serial.println(total_time, DEC);
          
          total_time = 0;
          
          Serial.println(F("CAM Capture Done."));
          total_time = millis();

          //
          uint32_t len  = myCAM.read_fifo_length();
          if (len >= MAX_FIFO_SIZE) //8M
          {
            Serial.println(F("Over size."));
          }
          if (len == 0 ) //0 kb
          {
            Serial.println(F("Size is 0."));
          }
          
          myCAM.CS_LOW();
          myCAM.set_fifo_burst(); 
          
          i = 0;
          while ( len-- ) {
            temp_last = temp;
            temp =  SPI.transfer(0x00);
            //Read JPEG data from FIFO
            if ( (temp == 0xD9) && (temp_last == 0xFF) ) //If find the end ,break while,
            {
              buffer[i++] = temp;  //save the last  0XD9     
              //Write the remain bytes in the buffer
              if (!client.connected()) break;
              client.write(&buffer[0], i);
              is_header = false;
              i = 0;
              myCAM.CS_HIGH();
              break; 
            }  
            if (is_header == true) { 
              //Write image data to buffer if not full
              if (i < bufferSize)
                buffer[i++] = temp;
              else {
                //Write bufferSize bytes image data to file
                if (!client.connected()) break;
                client.write(&buffer[0], bufferSize);
                i = 0;
                buffer[i++] = temp;
              }        
            }
            else if ((temp == 0xD8) & (temp_last == 0xFF)) {
              is_header = true;
              buffer[i++] = temp_last;
              buffer[i++] = temp;   
            } 
          } 
          //
          
          //camCapture(myCAM);
          total_time = millis() - total_time;
          Serial.print(F("send total_time used (in miliseconds):"));
          Serial.println(total_time, DEC);
          Serial.println(F("CAM send Done."));
            
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
            
            myCAM.clear_fifo_flag();
            start_capture();
            Serial.println(F("CAM Capturing"));
            
            int total_time = 0;
            
            total_time = millis();
            while (!myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));
            total_time = millis() - total_time;
            Serial.print(F("capture total_time used (in miliseconds):"));
            Serial.println(total_time, DEC);
            
            total_time = 0;
            
            Serial.println(F("CAM Capture Done."));
            total_time = millis();
  
            //
            uint32_t len  = myCAM.read_fifo_length();
            if (len >= MAX_FIFO_SIZE) //8M
            {
              Serial.println(F("Over size."));
            }
            if (len == 0 ) //0 kb
            {
              Serial.println(F("Size is 0."));
            }
            
            myCAM.CS_LOW();
            myCAM.set_fifo_burst(); 
            
            i = 0;
            while ( len-- ) {
              temp_last = temp;
              temp =  SPI.transfer(0x00);
              //Read JPEG data from FIFO
              if ( (temp == 0xD9) && (temp_last == 0xFF) ) //If find the end ,break while,
              {
                buffer[i++] = temp;  //save the last  0XD9     
                //Write the remain bytes in the buffer
                //if (!client.connected()) break;
                client.write(&buffer[0], i);
                is_header = false;
                i = 0;
                myCAM.CS_HIGH();
                break; 
              }  
              if (is_header == true) { 
                //Write image data to buffer if not full
                if (i < bufferSize)
                  buffer[i++] = temp;
                else {
                  //Write bufferSize bytes image data to file
                  if (!client.connected()) break;
                  client.write(&buffer[0], bufferSize);
                  i = 0;
                  buffer[i++] = temp;
                }        
            } else if ((temp == 0xD8) & (temp_last == 0xFF)) {
              is_header = true;
              buffer[i++] = temp_last;
              buffer[i++] = temp;   
            } 
          } 
          //
          
          //camCapture(myCAM);
          total_time = millis() - total_time;
          Serial.print(F("send total_time used (in miliseconds):"));
          Serial.println(total_time, DEC);
          Serial.println(F("CAM send Done."));
          
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
    #ifdef BT
    ble.end();
    #endif
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

void start_capture(){
  myCAM.clear_fifo_flag();
  myCAM.start_capture();
}



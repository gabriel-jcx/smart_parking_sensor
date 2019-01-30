
//#define BMPIMG //uses BMP instead of JPGE

#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClient.h>

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


#define ssid1        "pi_gateway"
#define password1    "12341234"

WiFiMulti wifiMulti;
WiFiServer server(80);


void serve()
{
  WiFiClient client = server.available();
  if (client) 
  {
    Serial.println("New Client.");
    String currentLine = "";
    while (client.connected()) 
    {
      if (client.available()) 
      {
        char c = client.read();
        Serial.write(c);
        if (c == '\n') 
        {
          if (currentLine.length() == 0) 
          {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            client.print(
              "<style>body{margin: 0}\nimg{height: 100%; width: auto}</style>"
              "<img id='a' src='/camera' onload='this.style.display=\"initial\"; var b = document.getElementById(\"b\"); b.style.display=\"none\"; b.src=\"camera?\"+Date.now(); '>"
              "<img id='b' style='display: none' src='/camera' onload='this.style.display=\"initial\"; var a = document.getElementById(\"a\"); a.style.display=\"none\"; a.src=\"camera?\"+Date.now(); '>");
            client.println();
            break;
          } 
          else 
          {
            currentLine = "";
          }
        } 
        else if (c != '\r') 
        {
          currentLine += c;
        }
        
        if(currentLine.endsWith("GET /camera"))
        {
          
          delay(1000);
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
          
          client.println("HTTP/1.1 200 OK");
          #ifdef BMPIMG
            client.println("Content-Type: image/bmp");
          #else
            client.println("Content-Type: image/jpeg");
          #endif
          client.println();
          String response = "HTTP/1.1 200 OK\r\n";
          response += "Content-Type: image/jpeg\r\n";
          response += "Content-len: " + String(len) + "\r\n\git r\n";
          //client.println(response);
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

        }
      }
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }  
}

void setup() 
{
  Serial.begin(115200);

  wifiMulti.addAP(ssid1, password1);
  //wifiMulti.addAP(ssid2, password2);
  Serial.println("Connecting Wifi...");
  if(wifiMulti.run() == WL_CONNECTED) {
      Serial.println("");
      Serial.println("WiFi connected");
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
  }
  
  uint8_t vid, pid;
  uint8_t temp;
    //set the CS as an output:
    pinMode(CS,OUTPUT);
    pinMode(CAM_POWER_ON , OUTPUT);
    digitalWrite(CAM_POWER_ON, HIGH);
  #if defined(__SAM3X8E__)
  Wire1.begin();
  #else
  Wire.begin();
  #endif
  Serial.begin(115200);
  Serial.println(F("ArduCAM Start!"));
  
  
  
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
  myCAM.OV2640_set_JPEG_size(OV2640_1600x1200);
  //myCAM.OV2640_set_JPEG_size(OV2640_640x480); //works
  //myCAM.OV2640_set_JPEG_size(OV2640_1280x1024); //works
  myCAM.clear_fifo_flag();

  
  server.begin();
}

void start_capture(){
  myCAM.clear_fifo_flag();
  myCAM.start_capture();
}
//
//void camCapture(ArduCAM myCAM){
//  //WiFiClient client = server.client();
//  WiFiClient client = server.available();
//  uint32_t len  = myCAM.read_fifo_length();
//  if (len >= MAX_FIFO_SIZE) //8M
//  {
//    Serial.println(F("Over size."));
//  }
//  if (len == 0 ) //0 kb
//  {
//    Serial.println(F("Size is 0."));
//  }
//  myCAM.CS_LOW();
//  myCAM.set_fifo_burst(); 
//  if (!client.connected()) return;
//  String response = "HTTP/1.1 200 OK\r\n";
//  response += "Content-Type: image/jpeg\r\n";
//  response += "Content-len: " + String(len) + "\r\n\r\n";
//  client.println(response);
//  i = 0;
//  while ( len-- )
//  {
//  temp_last = temp;
//  temp =  SPI.transfer(0x00);
//  //Read JPEG data from FIFO
//  if ( (temp == 0xD9) && (temp_last == 0xFF) ) //If find the end ,break while,
//  {
//  buffer[i++] = temp;  //save the last  0XD9     
//  //Write the remain bytes in the buffer
//  if (!client.connected()) break;
//  client.write(&buffer[0], i);
//  is_header = false;
//  i = 0;
//  myCAM.CS_HIGH();
//  break; 
//  }  
//  if (is_header == true)
//  { 
//  //Write image data to buffer if not full
//  if (i < bufferSize)
//  buffer[i++] = temp;
//  else
//  {
//  //Write bufferSize bytes image data to file
//  if (!client.connected()) break;
//  client.write(&buffer[0], bufferSize);
//  i = 0;
//  buffer[i++] = temp;
//  }        
//  }
//  else if ((temp == 0xD8) & (temp_last == 0xFF))
//  {
//  is_header = true;
//  buffer[i++] = temp_last;
//  buffer[i++] = temp;   
//  } 
//  } 
//}
//
//void serverCapture(){
//  delay(1000);
//  start_capture();
//  Serial.println(F("CAM Capturing"));
//  
//  int total_time = 0;
//  
//  total_time = millis();
//  while (!myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));
//  total_time = millis() - total_time;
//  Serial.print(F("capture total_time used (in miliseconds):"));
//  Serial.println(total_time, DEC);
//  
//  total_time = 0;
//  
//  Serial.println(F("CAM Capture Done."));
//  total_time = millis();
//  camCapture(myCAM);
//  total_time = millis() - total_time;
//  Serial.print(F("send total_time used (in miliseconds):"));
//  Serial.println(total_time, DEC);
//  Serial.println(F("CAM send Done."));
//}

//void handleNotFound(){
//  String message = "Server is running!\n\n";
//  message += "URI: ";
//  //message += server.uri();
//  message += "\nMethod: ";
//  message += (server.method() == HTTP_GET)?"GET":"POST";
//  message += "\nArguments: ";
//  message += server.args();
//  message += "\n";
//  server.send(200, "text/plain", message);
//  Serial.println(message);
//
//
//
//  if (server.hasArg("ql")){
//  int ql = server.arg("ql").toInt();
//  #if defined (OV2640_MINI_2MP) || defined (OV2640_CAM)
//  myCAM.OV2640_set_JPEG_size(ql);
//  #elif defined (OV5640_MINI_5MP_PLUS) || defined (OV5640_CAM)  
//  myCAM.OV5640_set_JPEG_size(ql);
//  #elif defined (OV5642_MINI_5MP_PLUS) || defined (OV5642_MINI_5MP_BIT_ROTATION_FIXED) ||(defined (OV5642_CAM))
//  myCAM.OV5642_set_JPEG_size(ql);
//  #endif
//  
//  Serial.println("QL change to: " + server.arg("ql"));
//  }
//}

void loop()
{
  serve();

}

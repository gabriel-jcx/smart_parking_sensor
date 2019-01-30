
#include <WiFi.h>

#define TRIGGER 27
#define ECHO    14

long duration;
int  distance;

char curr_state;
char prev_state;

const char* ssid     = "";
const char* password = "";

WiFiServer server(80);

void setup()
{
    Serial.begin(115200);
    pinMode(TRIGGER, OUTPUT);
    pinMode(ECHO, INPUT);
    pinMode(13, OUTPUT);      // set the LED pin mode

    delay(10);
    
    curr_state = 0;
    prev_state = 0;
    
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    
    server.begin();

}

int value = 0;

void loop(){
  delay(100);
    distance = SR04(); //(duration/2) / 29.1;


  if ((0 < distance) && (distance < 20)){
    Serial.println("Spot taken");
    curr_state = 0xFF;
    
  } else {
    Serial.println("Spot not taken.");
    curr_state = 0x00;
  }

  
 WiFiClient client = server.available();   // listen for incoming clients

  if (client) {                             // if you get a client,
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        if (c == '\n') {                    // if the byte is a newline character

          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // the content of the HTTP response follows the header:
            if( curr_state != prev_state) {
              client.print("The status the spot has changed.<br>");
              if( curr_state == 0xFF){
                client.print("The current status is taken.<br>");
              } else {
                client.print("The current status is empty.<br>");
              }
              client.print("Click <a href=\"/ACK\">here</a> to send ACK signal.<br>");
            } else {
              client.print("The status the spot has not changed.<br>");
              if( curr_state == 0xFF){
                client.print("The current status is taken.<br>");
              } else {
                client.print("The current status is empty.<br>");
              }
            }
            client.printf("The current distance is %d .<br>", distance);
            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          } else {    // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

        // Check to see if the client request was "GET /H" or "GET /L":
        if (currentLine.endsWith("GET /ACK")) {
          prev_state = curr_state;
          digitalWrite(13, HIGH);               // GET /ACK turns the LED on
        } else {
          digitalWrite(13, LOW);               // else, turns the LED off
        }
      }
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }

  
}



long SR04(){
  digitalWrite(TRIGGER, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIGGER, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIGGER, LOW);
  duration = pulseIn(ECHO, HIGH);
  return (duration/2) / 29.1;
}


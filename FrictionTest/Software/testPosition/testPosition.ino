#include <SPI.h>
//#include <SD.h>
//#include "RTClib.h"
//#include <WiFiNINA.h> 
//#include <PubSubClient.h>
//#include "credentials.h"

//_____________________________________________________
// position Sensors

// Read Sensors
String getPos(){
  // Channel 1
  float volt1 = analogRead(A7);
  float  pos1 = map(volt1, 0.0, 1023, 0.0, 100.0); 
    
  // Compile results
  String  majorResult = String(pos1); 
  return majorResult;     
}


/////////// Setup ///////////
//_____________________________________________________
// Function: Setup
void setup() {
  // put your setup code here, to run once:
  // start serial port
  Serial.begin(9600);

  // Set pinMode for led
  pinMode(A7, INPUT);  
  Serial.println("Setup Complete"); 
}
  

//_____________________________________________________
// Main Loop
void loop() {
    String data = getPos();   
    Serial.println(data);
    delay(10);
}

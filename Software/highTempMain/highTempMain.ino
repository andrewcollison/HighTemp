#include <SPI.h>
#include <SD.h>
#include "RTClib.h"
#include <Adafruit_MAX31856.h>
// A0: Stat LED
// A1: Log LED
// A2: Error LED

// Define constants
const int SDchipSelect = 2;
RTC_DS1307 rtc;
char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
int timeElapsed = 0;
const int TS1_chipSelect = 7; // Chipselect for temp senor channel 1
const int TS2_chipSelect = 6; // Chipselect for temp senor channel 2
const int TS3_chipSelect = 5; // Chipselect for temp senor channel 3
const int TS4_chipSelect = 4; // Chipselect for temp senor channel 4

Adafruit_MAX31856 maxthermo1 = Adafruit_MAX31856(TS1_chipSelect);
Adafruit_MAX31856 maxthermo2 = Adafruit_MAX31856(TS2_chipSelect);
Adafruit_MAX31856 maxthermo3 = Adafruit_MAX31856(TS3_chipSelect);
Adafruit_MAX31856 maxthermo4 = Adafruit_MAX31856(TS4_chipSelect);

//_____________________________________________________
// Function: Get time 
String getTime(){
  DateTime now = rtc.now();
  String current_year = String(now.year());  
  String current_month ; 
  if(now.month() < 10){
     current_month = String(0) + String(now.month());     
    }
  else{
    current_month = String(now.month());    
    }    
  String current_day;
  if(now.day() < 10){
     current_day = String(0) + String(now.day());
    }
  else{
    current_day = String(now.day());    
    }  
  String current_hour = String(now.hour());
  String current_minute = String(now.minute());
  String current_second = String(now.second());
  
  // Fotmat data in ISO8601 Standard format
  String time_data = current_year + "-" + current_month + "-" + current_day + "," + current_hour + ":" + current_minute + ":" + current_second;  
  return time_data;  
}
  
//_____________________________________________________
// Function: Store Data
void storeData(String filename, String readout){
    File dataFile = SD.open(filename, FILE_WRITE);
  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(readout);
    dataFile.close();
    // print to the serial port too:
    //Serial.println(readout);
  }
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening data file");
    digitalWrite(A2, HIGH);
  }  
}


//_____________________________________________________
// Temperature Sensors

// Read Sensors
String getTemp(){
  String majorResult;
  maxthermo1.triggerOneShot();
  maxthermo2.triggerOneShot();
  maxthermo3.triggerOneShot();
  maxthermo4.triggerOneShot();
  delay(600);
  
  ///// Get temp: Channel 1
  float tempResult1;
  String tempString1; 
  tempResult1 = maxthermo1.readThermocoupleTemperature(); 
  tempString1 = String(tempResult1);

  ///// Get temp: Channel 2
  float tempResult2;
  String tempString2; 
  tempResult2 = maxthermo2.readThermocoupleTemperature();
  tempString2 = String(tempResult2);
  
  ///// Get temp: Channel 3
  float tempResult3;
  String tempString3; 
  tempResult3 = maxthermo3.readThermocoupleTemperature();
  tempString3 = String(tempResult3);
  
  ///// Get temp: Channel 4
  float tempResult4;
  String tempString4; 
  tempResult4 = maxthermo4.readThermocoupleTemperature();
  tempString4 = String(tempResult4);


  
  // Compile results
  majorResult = tempString1 + ", " + tempString2 + ", " + tempString3 + ", " + tempString4;
  return majorResult;     
}


//_____________________________________________________
// Function: Setup
void setup() {
  // put your setup code here, to run once:
  // start serial port
  Serial.begin(9600);
  Serial.println("got to here");
  // Setting Up RTC
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }

  // Set pinMode for led
  pinMode(A0, OUTPUT);
  digitalWrite(A0, LOW);
  
  pinMode(A1, OUTPUT);
  digitalWrite(A1, LOW);  

  pinMode(A2, OUTPUT);
  digitalWrite(A2, LOW);


  
  if (! rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    // following line sets the RTC to the date & time this sketch was compiled
     rtc.adjust(DateTime(__DATE__, __TIME__));
    }
//    rtc.adjust(DateTime(__DATE__, __TIME__)); // Uncomment this line to reset rtc time to current time

    // Setup SD card storage
    //  Serial.println("Initializing SD card...");
    // see if the card is present and can be initialized:
    if (!SD.begin(SDchipSelect)) {
      Serial.println("Card failed, or not present");
      // don't do anything more:
      Serial.println("SD failure");
      digitalWrite(A2, HIGH);
//      while (1);
    }
    Serial.println("card initialized.");

  

  //// Setup MAX31856
  // Channel 1
  if (!maxthermo1.begin()) {
    Serial.println("Could not initialize thermocouple 1.");
    Serial.println("got to here");
    while (1) delay(10);
  }
  maxthermo1.setThermocoupleType(MAX31856_TCTYPE_K);
  maxthermo1.setConversionMode(MAX31856_ONESHOT_NOWAIT);
   
  // Channel 2
  if (!maxthermo2.begin()) {
    Serial.println("Could not initialize thermocouple 2.");
    Serial.println("got to here");
    while (1) delay(10);
  }
  maxthermo2.setThermocoupleType(MAX31856_TCTYPE_K);
  maxthermo2.setConversionMode(MAX31856_ONESHOT_NOWAIT);
//  Serial.println("Sensor Started");

  // Channel 3
  if (!maxthermo3.begin()) {
    Serial.println("Could not initialize thermocouple 3.");
    Serial.println("got to here");
    while (1) delay(10);
  }
  maxthermo3.setThermocoupleType(MAX31856_TCTYPE_K);
  maxthermo3.setConversionMode(MAX31856_ONESHOT_NOWAIT);

  // Channel 4
  if (!maxthermo4.begin()) {
    Serial.println("Could not initialize thermocouple 4.");
    Serial.println("got to here");
    while (1) delay(10);
  }
  maxthermo4.setThermocoupleType(MAX31856_TCTYPE_K);
  maxthermo4.setConversionMode(MAX31856_ONESHOT_NOWAIT);
    

  
  Serial.println("Setup Complete");

  
}
  

//_____________________________________________________
// Main Loop
void loop() {
  // put your main code here, to run repeatedly:
  // Get temperature from sensor
  digitalWrite(A1, HIGH);
    
  String  tempOut = getTemp();
//  Serial.println(tempOut);
  String data = getTime()+", " + tempOut;   
//  storeData("Dt.txt", data); // Keep file name short (<8 Characters)
  
  digitalWrite(A1, LOW);

  // Print data to serial
  Serial.println(data);
   
  

  delay(1000);
}

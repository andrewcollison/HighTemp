#include <WiFiNINA.h> 
#include <PubSubClient.h>

// MQTT Server allocation
const char* ssid = "control1";
const char* password = "internetplease";
const char* mqttServer = "192.168.1.4";
const char* mqttUsername = "mqtt";
const char* mqttPassword = "mqtt";

char subTopic[] = "arduino/press1cmd";     //payload[0] will control/set LED
char pubTopic[] = "arduino/press1";       //payload[0] will have ledState value
unsigned long lastMsg = 0;
int value = 0;
#define MSG_BUFFER_SIZE  (100)
char msg[MSG_BUFFER_SIZE];
float resultData[5] = {0, 0, 0, 0, 0};

WiFiClient wifiClient;
PubSubClient client(wifiClient);

//_____________________________________________________
// Function: Reconnect to mqtt server
void reconnect() 
{
  // Loop until we're reconnected
  while (!client.connected()) 
  {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ArduinoClient-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), mqttUsername, mqttPassword)) 
    {
      Serial.println("connected");
      // ... and resubscribe
      client.subscribe(subTopic);
    } else 
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


//_____________________________________________________
// Function: Callback
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
//    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    Serial.println("LED on");
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
//    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
    Serial.println("LED off");
  }

}

//______________________________________________
// Map values as floats
float fmap(float x, float in_min, float in_max, float out_min, float out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

//______________________________________________
// Get pressure data
void getPress(){
  resultData[0] = avgPress(A0, 100);
  resultData[1] = avgPress(A1, 100);
  resultData[2] = avgPress(A2, 100);
  resultData[3] = avgPress(A3, 100);
  resultData[4] = avgPress(A6, 100);  
}

//______________________________________________
// Analog to pressure 
float avgPress(int anPin, int ns){
  float tallyList[ns] = {};
  for(int i=0; i < ns; i++){
    float  an = analogRead(anPin); 
    float testV= fmap(an, 0.000, 1023.000, 0.000, 3.300);
    tallyList[i] = fmap(testV, 0.681, 3.400, 0.000, 100.000);
//    Serial.print("Average tally");
//    Serial.println(String(tallyList));
    delay(100);
  }
  float tallyP;
  for(int i =0; i < ns; i++){
    tallyP = tallyP + tallyList[i];    
  }
//  Serial.print("tallyP: ");
//  Serial.println(tallyP);

  float avgP = (tallyP/ns)*0.01;
//  Serial.print("Average Press: ");
//  Serial.println(avgP, 3);  
  return avgP;
}


/////////// Setup ///////////

//_____________________________________________________
// Function: Wifi Setup
void setup_wifi() 
{
  delay(10);
  
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
} 


void setup() {
  // Serial Coms
  Serial.begin(9600);
  Serial.println("got to here");

  // Setting up mqtt server
  setup_wifi();
  client.setServer(mqttServer, 1883);
  client.setCallback(callback);
  Serial.println("Setup Complete");  
}

void loop() {
  // put your main code here, to run repeatedly:
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    String data = String(resultData[0]) + "," + String(resultData[1]) + "," + String(resultData[2]) + "," + String(resultData[3]) + "," + String(resultData[4]);
    int str_len = data.length() + 1;
    char char_array[str_len];
    data.toCharArray(char_array, str_len);
    
//    snprintf (msg, MSG_BUFFER_SIZE, "%ld", data);
    Serial.print("Publish message: ");
    Serial.println(data);
    client.publish("press1", char_array);
  }

}

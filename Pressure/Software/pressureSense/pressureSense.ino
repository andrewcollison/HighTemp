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

//_____________________________________________________
// Temperature Sensors

// Read Sensors
String getPress(){
  // Channel 1
  float volt1 = analogRead(A0)*(5.0 / 1023.0);
  float  press1 = map(volt1, 0.6, 3.3, 0, 100);
  

  
  // Compile results
  String  majorResult = String(press1); 
  return majorResult;     
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

  // Set pinMode for sensor
  pinMode(A0, INPUT);


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
    String data = getPress();
    int str_len = data.length() + 1;
    char char_array[str_len];
    data.toCharArray(char_array, str_len);
    
//    snprintf (msg, MSG_BUFFER_SIZE, "%ld", data);
    Serial.print("Publish message: ");
    Serial.println(data);
    client.publish("temp2", char_array);
  }

}

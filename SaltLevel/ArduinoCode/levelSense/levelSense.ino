// Arduino level sensor code
// Anderw Collison

const int level_1 = 2;
const int level_2 = 3;
const int level_3 = 4;
const int level_4 = 5;

//_____________________________________________________
// Level Sensors

// Read Sensors
String get_level(){
  String major_result;
  int probe[4] = {0, 0, 0, 0};

  if(digitalRead(level_1) ==HIGH){
    probe[0] = 1;
    } 

  if(digitalRead(level_2) == HIGH){
    probe[1] = 1;
    }

  if(digitalRead(level_3) == HIGH){
    probe[2] = 1;
    }

  if(digitalRead(level_4) == HIGH){
    probe[3] = 1;
    }

  major_result = String(probe[3]) + ", " + String(probe[2]) + ", " + String(probe[1]) + ", " + String(probe[0]);
  Serial.println(major_result);

  
  // Compile results
//  major_result = "got to here";
  return major_result;     
}


//_____________________________________________________
// Function: Setup
void setup() {
  // put your setup code here, to run once:
  // start serial port
  Serial.begin(9600);

  pinMode(level_1, INPUT);
  pinMode(level_2, INPUT);
  pinMode(level_3, INPUT);
  pinMode(level_4, INPUT);
  
  Serial.println("Setup Complete");  
}
  

//_____________________________________________________
// Main Loop
void loop() {
  // put your main code here, to run repeatedly:
      
  String  level_out = get_level();
  Serial.println(level_out);
  delay(1000);

}

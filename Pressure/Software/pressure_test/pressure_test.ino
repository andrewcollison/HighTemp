float resultData[5] = {0, 0, 0, 0, 0};

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
//  resultData[1] = avgPress(A1, 100);
//  resultData[2] = avgPress(A2, 100);
//  resultData[3] = avgPress(A3, 100);
//  resultData[4] = avgPress(A6, 100);  
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

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
  Serial.println("Setup Complete");
  pinMode(A1, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int anPin;
  int ns;
//  avgPress(A0, 100);
  getPress();
  String datString = String(resultData[0],3) + "," + String(resultData[1]) + "," + String(resultData[2]) + "," + String(resultData[3]) + "," + String(resultData[4]);
  Serial.println(datString);
  delay(500);
}

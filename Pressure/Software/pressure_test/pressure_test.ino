float resultData[5] = {0, 0, 0, 0, 0};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
  Serial.println("Setup Complete");
  pinMode(A1, INPUT);
}


float fmap(float x, float in_min, float in_max, float out_min, float out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void getPress(){
  // Channel 1

  float volt1 = analogRead(A0)*(3.3 / 1023.0);  
  resultData[0] = fmap(volt1, 0.6, 3.3, 0, 100);
  float testV= fmap(an, 0.000, 1023.000, 0.000, 3.300);
  float  = fmap(volt1, 0.681, 3.400, 0.000, 100.000);

  float volt2 = analogRead(A1)*(3.3 / 1023.0);
  resultData[1] = fmap(volt2, 0.30, 3.30, -100.00, 100.00 );
//  Serial.println(resultData[1]);

  float volt3 = analogRead(A2)*(3.3 / 1023.0);
  resultData[2] = fmap(volt3, 0.6, 3.3, 0, 100);

  float volt4 = analogRead(A3)*(3.3 / 1023.0);
  resultData[3] = fmap(volt4, 0.6, 3.3, 0, 100);

  float volt5 = analogRead(A6)*(3.3 / 1023.0);
  resultData[4] = fmap(volt5, 0.00, 3.30, 0.00, 10.00);

  float  an = analogRead(A0);
//   float  an = analogRead(A0)*(3.300 / 1023.000);
  float testV= fmap(an, 0.000, 1023.000, 0.000, 3.300);
  float testp = fmap(volt1, 0.681, 3.400, 0.000, 100.000);
//  Serial.print("Ana: ");
//  Serial.println(an, 3);
//  Serial.print("Voltage: ");
//  Serial.println(testV, 3);
//  Serial.print("Test pressure: ");
  Serial.println(testp*0.010, 3);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  getPress();
  String datString = String(resultData[0]) + "," + String(resultData[1]) + "," + String(resultData[2]) + "," + String(resultData[3]) + "," + String(resultData[4]);
//  Serial.println(datString);
  delay(500);
}

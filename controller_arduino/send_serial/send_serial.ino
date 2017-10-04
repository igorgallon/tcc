#define LED  13
 
String serialData = "";
boolean onSerialRead = false; 
 
void setup(){
  pinMode(LED, OUTPUT);
  // initialize serial
  Serial.begin(9600);
  serialData.reserve(200);
}
 
void procesSerialData(){
  Serial.write("LED\n");
  digitalWrite(LED, HIGH);
  delay(1000);
  Serial.write("OFF\n");
  digitalWrite(LED, LOW);
  delay(1000);
}
 
void loop(){
  procesSerialData();
}

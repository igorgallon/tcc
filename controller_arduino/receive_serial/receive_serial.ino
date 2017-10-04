#define LED  13
 
String serialData = "";
boolean onSerialRead = false; 
 
void setup() {
  pinMode(LED, OUTPUT);
  // initialize serial
  Serial.begin(9600);
  serialData.reserve(200);
}
 
void procesSerialData(){
  Serial.print("Data " + serialData);
  if (serialData == "LED") {    
    Serial.println(" LED ON");
    digitalWrite(LED, HIGH);
  } else {
    Serial.println(" LED OFF");
    digitalWrite(LED, LOW);
  }
  serialData = "";
  onSerialRead = false;
}
 
void loop() {
  if (onSerialRead) {
    procesSerialData();
  }
}
 
void serialEvent(){
  while(Serial.available()){
    char inChar = (char)Serial.read();
    if (inChar == '\n'){
      onSerialRead = true;
    }else{
      serialData += inChar;
    }
  }
}

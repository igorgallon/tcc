#define LED  13
 
String serialData = "";
boolean onSerialRead = false; 
 
void setup() {
  pinMode(LED, OUTPUT);
  // initialize serial
  Serial.begin(9600);
}
 
void procesSerialData(){
  Serial.print("Data " + serialData);
  if (serialData == "LED") {
    Serial.print("GotIt");
    digitalWrite(LED, HIGH);
  } else {
    digitalWrite(LED, LOW);
  }
  serialData = "";
  onSerialRead = false;
}
 
void loop() {
  if (onSerialRead) {
    Serial.println("Process");
    procesSerialData();
  }
}
 
void serialEvent(){
  Serial.println("Trying");
  while(Serial.available()){
    char inChar = (char)Serial.read();
    if (inChar == '\n'){
      onSerialRead = true;
    }else{
      serialData += inChar;
    }
    Serial.println("Event");
    Serial.println(serialData);
  }
}

#include <IRremote.h>

// Key codes for IR comunication
unsigned long FORWARD       = 0x2FDD827;
unsigned long BACKWARD      = 0x2FDF807;
unsigned long LEFT          = 0x2FD7887;
unsigned long RIGHT         = 0x2FD58A7;
unsigned long STOP          = 0x2FD48B7;
unsigned long TRAINING_MODE = 0x2FD807F;  // Key 1
unsigned long PREDICT_MODE  = 0x2FD40BF;  // Key 2
unsigned long IDLE_MODE     = 0x2FDC03F;  // Key 3

// Pins
int M1A       = 5;              // Motor 1 - A
int M1B       = 6;              // Motor 1 - B
int M1EN      = 7;              // Motor 1 - Enable
int M2A       = 8;              // Motor 2 - A
int M2B       = 9;              // Motor 2 - B
int M2EN      = 10;             // Motor 2 - Enable
int RECV_PIN  = 11;             // IR Receiver

// Messages for Serial comunication
char msgTraining[]    = "TR";
char msgPredicting[]  = "PD";
char msgForward[]     = "FW";
char msgBackward[]    = "BW";
char msgLeft[]        = "LF";
char msgRight[]       = "RH";
char msgStop[]        = "ST";

IRrecv irrecv(RECV_PIN);
decode_results results;

String serialData = "";         // Data received from Serial comunication
boolean onSerialRead = false;   // Determines when stop to receive data
float codeIR;                   // Code got from IR control

void setup() {
  pinMode(M1A, OUTPUT);
  pinMode(M1B, OUTPUT);
  pinMode(M2A, OUTPUT);
  pinMode(M2B, OUTPUT);
  pinMode(M1EN, OUTPUT);
  pinMode(M2EN, OUTPUT);
  
  irrecv.enableIRIn();          // Setting the IR sensor receiver
  
  Serial.begin(9600);           // Initialize serial comunication
  serialData.reserve(200);
}

void loop(){
  if(irrecv.decode(&results)){
    
    codeIR = (results.value);
        
    if(codeIR == TRAINING_MODE){
      Serial.println("Training mode");
      training();
    }
    if(codeIR == PREDICT_MODE){
      Serial.println("Prediction mode");
      predicting();
    }
    
    irrecv.resume();                          // Receives the next value from IR sensor
  }
}

void training(){

  Serial.write(msgTraining);                  // Inform the Raspberry that the Training mode has begun
  enableMotor();                              // Enable motors
  
  while(codeIR != STOP){
    
    if(irrecv.decode(&results)){
      codeIR = (results.value);
      drive(codeIR);                          // Drive the motor according to the given command
      irrecv.resume();
    } 
  }

  Serial.println("Stop");
  Serial.write(msgStop);                      // Inform the Rasberry that the Training mode has finished
  drive(STOP);                                // Stop motors
  disableMotor();                             // Disable motors
}

void predicting(){

  Serial.write(msgPredicting);                // Inform the Raspberry that the Predicting mode has begun
  enableMotor();

  while(codeIR != STOP){
    if(onSerialRead){
      if(serialData == msgForward){
        Serial.println("[Prediction] Drive to Forward");
        drive(FORWARD);
      }
      if(serialData == msgLeft){
        Serial.println("[Prediction] Drive to Left");
        drive(LEFT);
      }
      if(serialData == msgRight){
        Serial.println("[Prediction] Drive to Right");
        drive(RIGHT);
      }
      if(serialData == msgBackward){
        Serial.println("[Prediction] Drive to Backward");
        drive(BACKWARD);
      }
      
      serialData = "";
      onSerialRead = false; 
    }

    // Verify if the STOP button has been pressed
    if(irrecv.decode(&results)){
      codeIR = (results.value);
      irrecv.resume();
    }
    
  }

  Serial.println("Stop prediction");
  drive(STOP);
  disableMotor();
}

void drive(float   command){

  if(command == FORWARD){
    Serial.println("Forward");
    Serial.write(msgForward);
    forward();
  }
  if(command == LEFT){
    Serial.println("Left");
    Serial.write(msgLeft);
    left();
  }
  if(command == RIGHT){
    Serial.println("Right");
    Serial.write(msgRight);
    right();
  }
  if(command == BACKWARD){
    Serial.println("Backward");
    Serial.write(msgBackward);
    backward();
  }
  if(command == STOP){
    Serial.println("Stop");
    Serial.write(msgStop);
    stopMotor();
  }
}

void enableMotor(){
  digitalWrite(M1EN, HIGH);   // Enable Motor 1
  digitalWrite(M2EN, HIGH);   // Enable Motor 2
}

void disableMotor(){
  digitalWrite(M1EN, LOW);    // Disanable Motor 1
  digitalWrite(M2EN, LOW);    // Disanable Motor 2
}

void forward(){
  digitalWrite(M1A, HIGH);    // Turn forward Motor 1
  digitalWrite(M1B, LOW); 
  digitalWrite(M2A, HIGH);    // Turn forward Motor 2
  digitalWrite(M2B, LOW);
}

void backward(){
  digitalWrite(M1A, LOW);     // Turn backward Motor 1
  digitalWrite(M1B, HIGH);
  digitalWrite(M2A, LOW);     // Turn backward Motor 1
  digitalWrite(M2B, HIGH);
}

void left(){
  digitalWrite(M1A, LOW);     // Turn backward Motor 1
  digitalWrite(M1B, HIGH);
  digitalWrite(M2A, HIGH);    // Turn forward Motor 2
  digitalWrite(M2B, LOW);
}

void right(){
  digitalWrite(M1A, HIGH);    // Turn forward Motor 1
  digitalWrite(M1B, LOW);
  digitalWrite(M2A, LOW);     // Turn backward Motor 2
  digitalWrite(M2B, HIGH);
}
  
void stopMotor(){
  digitalWrite(M1A, LOW);     // Turn off Motor 1
  digitalWrite(M1B, LOW);
  digitalWrite(M2A, LOW);     // Turn off Motor 2
  digitalWrite(M2B, LOW);
}

// Trigger event when it detects an input of serial
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

#include <IRremote.h>

// Key codes for IR comunication
unsigned long FORWARD       = 0x2FDD827;
unsigned long BACKWARD      = 0x2FDF807;
unsigned long LEFT          = 0x2FD7887;
unsigned long RIGHT         = 0x2FD58A7;
unsigned long STOP          = 0x2FDC837;
unsigned long PAUSE         = 0x2FD38C7;
unsigned long TRAINING_MODE = 0x2FD807F;  // Key 1
unsigned long PREDICT_MODE  = 0x2FD40BF;  // Key 2
unsigned long IDLE_MODE     = 0x2FDC03F;  // Key 3

// Pins
int M1A       = 4;              // Motor 1 - A
int M1B       = 5;              // Motor 1 - B
int M1EN      = 6;              // Motor 1 - Enable (PWM)
int M2A       = 8;              // Motor 2 - A
int M2B       = 9;              // Motor 2 - B
int M2EN      = 10;             // Motor 2 - Enable (PWM)
int RECV_PIN  = 11;             // IR Receiver

// Messages for Serial comunication
char msgTraining[]    = "TR\n";
char msgPredicting[]  = "PD\n";
char msgForward[]     = "FW\n";
char msgBackward[]    = "BW\n";
char msgLeft[]        = "LF\n";
char msgRight[]       = "RH\n";
char msgStop[]        = "ST\n";

IRrecv irrecv(RECV_PIN);
decode_results results;

int speedM1 = 115;
int speedM2 = 115;
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

  Serial.begin(9600);           // Initialize serial comunication
  serialData.reserve(200);
  
  irrecv.enableIRIn();          // Setting the IR sensor receiver
}

void loop(){
  if(irrecv.decode(&results)){
    
    codeIR = (results.value);
        
    if(codeIR == TRAINING_MODE){
      irrecv.resume();                          // Receives the next value from IR sensor
      training();
    }
    if(codeIR == PREDICT_MODE){
      irrecv.resume();                          // Receives the next value from IR sensor
      predicting();
    }
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
}

void predicting(){

  Serial.write(msgPredicting);                // Inform the Raspberry that the Predicting mode has begun

  enableMotor();

  codeIR = 0;
  
  while(codeIR != STOP){
    serialEvent();
    
    if(onSerialRead){     
      if(serialData == msgForward){
        forward();
      }
      if(serialData == msgLeft){
        left();
      }
      if(serialData == msgRight){
        right();
      }
      if(serialData == msgBackward){
        backward();
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

  Serial.write(msgStop);
  stopMotor();
  disableMotor();
}

void drive(float command){

  if(command == FORWARD){
    Serial.write(msgForward);
    forward();
  }
  if(command == LEFT){
    Serial.write(msgLeft);
    left();
  }
  if(command == RIGHT){
    Serial.write(msgRight);
    right();
  }
  if(command == BACKWARD){
    Serial.write(msgBackward);
    backward();
  }
  if(command == STOP){
    Serial.write(msgStop);
    stopMotor();
    disableMotor();                             // Disable motors
  }
  if(command == PAUSE){
    stopMotor();
  }
}

void enableMotor(){
  analogWrite(M1EN, speedM1);   // Enable Motor 1
  analogWrite(M2EN, speedM2);   // Enable Motor 2
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
  digitalWrite(M1B, LOW);
  digitalWrite(M2A, HIGH);    // Turn forward Motor 2
  digitalWrite(M2B, LOW);
}

void right(){
  digitalWrite(M1A, HIGH);    // Turn forward Motor 1
  digitalWrite(M1B, LOW);
  digitalWrite(M2A, LOW);     // Turn backward Motor 2
  digitalWrite(M2B, LOW);
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
      serialData += '\n';
    }else{
      serialData += inChar;
    }
  }
}


#include <IRremote.h>

// Key codes
int FORWARD       = 0x2FDD827;
int BACKWARD      = 0x2FDF807;
int LEFT          = 0x2FD7887;
int RIGHT         = 0x2FD58A7;
int STOP          = 0x2FD48B7;
int TRAINING_MODE = 0x2FD807F;  // Key 1
int PREDICT_MODE  = 0x2FD40BF;  // Key 2
int IDLE_MODE     = 0x2FDC03F;  // Key 3

// Pins
int M1A       = 5;      // Motor 1 - A
int M1B       = 6;      // Motor 1 - B
int M1EN      = 7;      // Motor 1 - Enable

int M2A       = 8;      // Motor 2 - A
int M2B       = 9;      // Motor 2 - B
int M2EN      = 10;     // Motor 2 - Enable

int RECV_PIN  = 11;     // IR Receiver

IRrecv irrecv(RECV_PIN);
decode_results results;

float codeIR;           // Code got from IR control

void setup() {
  pinMode(M1A, OUTPUT);
  pinMode(M1B, OUTPUT);
  pinMode(M2A, OUTPUT);
  pinMode(M2B, OUTPUT);
  pinMode(M1EN, OUTPUT);
  pinMode(M2EN, OUTPUT);
  irrecv.enableIRIn();          // Setting the IR sensor receiver
}

void loop(){
  if(irrecv.decode(&results)){
    
    Serial.println(results.value, HEX);
    codeIR = (results.value);
    
    if(codeIR == TRAINING_MODE){
      training(codeIR);
    }
    if(codeIR == PREDICT_MODE){
    }
    
    irrecv.resume();            // Receives the next value from IR sensor
  }
}

void training(){
  
  while(codeIR != STOP){
    if(irrecv.decode(&results)){
    
      Serial.println(results.value, HEX);
      codeIR = (results.value);
    
      if(codeIR == TRAINING_MODE)
    
      irrecv.resume();            // Receives the next value from IR sensor
    } 
  }
}

void drive(float command){

  if(command == RIGHT)
  
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

void stopMotor(){
  digitalWrite(M1A, LOW);     // Turn off Motor 1
  digitalWrite(M1B, LOW);
  digitalWrite(M2A, LOW);     // Turn off Motor 2
  digitalWrite(M2B, LOW);
  }

void enableMotor(){
  digitalWrite(M1EN, HIGH);   // Enable Motor 1
  digitalWrite(M2EN, HIGH);   // Enable Motor 2
  }

void disableMotor(){
  digitalWrite(M1EN, LOW);    // Disanable Motor 1
  digitalWrite(M2EN, LOW);    // Disanable Motor 2
  }

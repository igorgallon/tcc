import RPi.GPIO as gpio
import serial
import time
import sys
import os
from Messages import Messages

currentState   = "stopped";

def main():
    
    # Instantiate Serial comunication
    arduino = serial.Serial('/dev/ttyACM0', 9600)    
    
    msg = ""
    
    while (1):
        try:
            msg = arduino.readline()
            print(msg)
            
            if(msg ==  Messages.msgTraining):
                currentState = "training"
                print("Training mode")
                # training mode
            
            
            
        except:
            pass
    
    print("Stopped")
    
    
    
def training():
    pass

def predicting():
    pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
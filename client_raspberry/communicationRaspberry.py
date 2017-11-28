import RPi.GPIO as gpio
import serial
import time
import sys
import os
from Messages import Messages
from sendDataTraining import SendDataTraining
from receiveModel import ReceiveModel
from predictingFrames import PredictingFrames

currentState   = "stopped";
msg = ""

def training(arduino):
    
    serverPC = "192.168.0.100"
    #serverPC = "10.0.0.108"
    
    # Create connection socket with Server PC
    train = SendDataTraining(serverPC, arduino)
    
    print("[Raspberry CONTROLLER] Sending frames...")
    train.sendFrames()
    
    try:
        print("[Raspberry CONTROLLER] Waiting for model from Server PC...")
        model = ReceiveModel('')
        model.receive()    
    except Exception as e:
        print(str(e))
    finally:
        pass
    
    
def predicting(arduino):
    
    print("[Raspberry CONTROLLER] Start prediction...")
    predict = PredictingFrames(arduino)
    predict.run()
    
    
# Instantiate Serial comunication
print("[Raspberry CONTROLLER] Estabilishing Serial Communication with Arduino...")
arduino = serial.Serial('/dev/ttyACM0', 9600)
#arduino = serial.Serial('/dev/ttyAMA0', 9600)

while 1:
    
    try:
        
        print("[Raspberry CONTROLLER] Waiting for Arduino command...")
        msg = arduino.readline()
        print(msg)
        
        if msg != "":
            
            if msg == Messages.msgStop:
                break
            
            if msg == Messages.msgTraining:
                print("[Raspberry CONTROLLER] Training mode!")
                currentState = "training"
                # training mode
                training(arduino)
            
            if msg == Messages.msgPredicting:
                print("[Raspberry CONTROLLER] Predicting mode!")
                currentState = "predicting"
                #  predicting mode
                predicting(arduino)
                
    except:
        pass
    
    
print("[Raspberry CONTROLLER] Stopped...")
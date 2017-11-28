import RPi.GPIO as gpio
import serial
import time
import sys
import os

def main():
    
    print("Connecting Arduino")
    #s = serial.Serial('/dev/ttyACM0', 9600)
    s = serial.Serial('/dev/ttyAMA0', 9600)
    print("Connected!")
    
    while 1:
        
        try:
            print("Trying to receive...")
            msg = s.readline()
            print("Message received {}".format(msg))
            
        except Exception as e:
            print(str(e))        
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
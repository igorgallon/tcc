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
            print("Turining ON")
            try:
                s.write("LED\n")
                time.sleep(1)
            except Exception as e:
                print(str(e))
                pass
            
            print("Turining OFF")
            s.write("OFF\n")
            time.sleep(1)
        
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
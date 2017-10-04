import RPi.GPIO as gpio
import serial
import time
import sys
import os

def main():

    s = serial.Serial('/dev/ttyACM0', 9600)
    
    while 1:
        s.write("LED\n")
        print("Turining ON")
        time.sleep(1)
        s.write("OFF\n")
        print("Turining OFF")
        time.sleep(1)        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
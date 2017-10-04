import RPi.GPIO as gpio
import serial
import time
import sys
import os

def main():

    s = serial.Serial('/dev/ttyACM0', 9600)
    
    while 1:
        try:
            msg = s.readline()
            print(msg)
        except:
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
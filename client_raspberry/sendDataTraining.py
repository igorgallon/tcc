# Picamera reference: http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# Socket reference: https://pymotw.com/2/socket/tcp.html
# Streaming by socket reference: http://picamera.readthedocs.io/en/release-1.9/recipes1.html#capturing-to-a-network-stream
# Struct referece: https://docs.python.org/2/library/struct.html

__author__ = 'Igor Gallon'

from Resolution import Resolution
from Messages import Messages
import picamera
import io
import time
import socket
import struct

class SendDataTraining(object):
    
    def __init__(self, host, serialPort):
        # PC Server address to connect
        # 192.168.1.103
        self.HOST = host
        self.PORT = 8000
        self.res = Resolution(320, 240);					    # Frame resolution
        
        self.frameClass = 1
        
        # Instantiate Serial comunication
        self.arduino = serialPort
        
        self.openConnection()
        
        
    def openConnection(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
        self.serverAddress = (self.HOST, self.PORT)
        
        print("[TRAINING] Trying to connect to Server...")
        self.clientSocket.connect(self.serverAddress)                            # Connect to PC Server
        print("[TRAINING] Connected!")
        # Make a file-like object out of the connection
        self.connection = self.clientSocket.makefile('wb')
        
    def closeConnection(self):
        print("[TRAINING] Closing connection...")
        self.connection.close()
        self.clientSocket.close()
        
    def convertToClass(self, message):
        classes = {
            Messages.msgBackward: 0,
            Messages.msgForward:  1,
            Messages.msgLeft:     2,
            Messages.msgRight:    3
        }
        
        return classes.get(message, -1)    
        
    def sendFrames(self):
        
        msg = ""
        classification = 0
        
        try:
            # Initializing picamera
            with picamera.PiCamera() as camera:
                
                camera.resolution = (self.res.width, self.res.height)       # Sets the camera resolution
                camera.framerate = 10                                       # 20 frames per second
        
                camera.start_preview()                                      # Start a preview
                time.sleep(2)                                               # Wait camera initializing (adjust luminosity or focus)
                
                stream = io.BytesIO()
                
                print("[TRAINING] Start streaming...")
                
                while 1:
                
                    try:
                        # Check if Arduino sent data
                        msg = self.arduino.readline();
                        
                        print("[TRAINING] Sending frame with class: {}".format(msg))
                        
                        if msg != "":
                            
                            if msg == Messages.msgStop:
                                break                    
                            
                            #Capture frame from camera
                            camera.capture(stream, 'jpeg')
                            
                            #Write the byte validation of message (1: valid / 0: not else)
                            self.connection.write(struct.pack('<I', 1))
                            self.connection.flush()
                            
                            classification = self.convertToClass(msg)
                            
                            #Write the command pressioned when training -> class of current sent frame
                            self.connection.write(struct.pack('<I', classification))
                            self.connection.flush()
                            
                            #Write the length of the capture to the stream and flush to
                            #ensure it actually gets sent
                            self.connection.write(struct.pack('<L', stream.tell()))
                            self.connection.flush()
                            
                            #Rewind the stream and send the image data over the wire
                            stream.seek(0)
                            self.connection.write(stream.read())
                            
                            #Reset the stream for the next capture
                            stream.seek(0)
                            stream.truncate()
                    except:
                        pass
                
                print("[TRAINING] Stop...")
                # Write the byte validation zero signalling the end of trasmission
                self.connection.write(struct.pack('<I', 0))
            
        finally:
            self.closeConnection()
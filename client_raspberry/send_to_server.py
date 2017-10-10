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

class Training():
    
    def __init__(self):
        # PC Server address to connect
        HOST = '192.168.1.103'
        PORT = 8000
        self.res = Resolution(32, 24);					    # Frame resolution
        
        self.frameClass = 1
        
        # Instantiate Serial comunication
        self.arduino = serial.Serial('/dev/ttyACM0', 9600)         
        
        openConnection()
    
    
    def openConnection(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
        self.serverAddress = (HOST, PORT)
    
        self.clientSocket.connect(serverAddress)                                 # Connect to PC Server
    
        # Make a file-like object out of the connection
        self.connection = clientSocket.makefile('wb')        
    
    
    def closeConnection(self):
        self.connection.close()
        self.clientSocket.close()
    
    
    def run(self):
        
        msg = ""
        
        try:
            # Initializing picamera
            with picamera.PiCamera() as camera:
                
                camera.resolution = (self.res.width, self.res.height)                 # Sets the camera resolution
                camera.framerate = 10                                       # 10 frames per second
        
                camera.start_preview()                                      # Start a preview
                time.sleep(2)                                               # Wait camera initializing (adjust luminosity or focus)
                
                stream = io.BytesIO()
                
                while (msg != Messages.msgStop):
                    
                    # Check if Arduino send data
                    msg = self.arduino.readLine();
                    
                    if(msg != ""):
                        
                        camera.capture(stream, 'jpeg')
                        
                        # Write the command pressioned when training -> class of current sent frame
                        self.connection.write(struct.pack('<L', msg))
                        self.connection.flush()                        
                        
                        # Write the length of the capture to the stream and flush to
                        # ensure it actually gets sent
                        self.connection.write(struct.pack('<L', stream.tell()))
                        self.connection.flush()
                        
                        # Rewind the stream and send the image data over the wire
                        stream.seek(0)
                        self.connection.write(stream.read())
            
                        # Reset the stream for the next capture
                        stream.seek(0)
                        stream.truncate()
                
                print("[TRAINING] Stop.")
                
            # Write a length of zero to the stream to signal we're done
            self.connection.write(struct.pack('<L', 0))
        finally:
            closeConnection()
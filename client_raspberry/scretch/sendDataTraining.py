# Picamera reference: http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# Socket reference: https://pymotw.com/2/socket/tcp.html
# Streaming by socket reference: http://picamera.readthedocs.io/en/release-1.9/recipes1.html#capturing-to-a-network-stream
# Struct referece: https://docs.python.org/2/library/struct.html

__author__ = 'Igor Gallon'

from Resolution import Resolution
import picamera
import io
import time
import socket
import struct

# PC Server addres to connect
HOST = '10.0.0.105'
PORT = 8000
res = Resolution(320, 240);					    # Frame resolution
thresholdParam = 90
maxThreshold = 255

frameClass = 1                                                      # ID of classification of current frame (1: foward / 2: left / 3: right)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
serverAddress = (HOST, PORT)
clientSocket.connect(serverAddress)                                 # Connect to PC Server

# Make a file-like object out of the connection
connection = clientSocket.makefile('wb')

try:
    # Initializing picamera
    with picamera.PiCamera() as camera:
        camera.resolution = (res.width, res.height)                 # Sets the camera resolution
        camera.framerate = 32                                       # 32 frames per second
        camera.led = False                                          # Disable red LED from camera
        
        camera.start_preview()                                      # Start a preview
        time.sleep(2)                                               # Wait camera initializing (adjust luminosity or focus)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        for img in camera.capture_continuous(stream, 'jpeg'):
            
            # Write the command pressioned when training -> class of current sent frame
            connection.write(struct.pack('<I', frameClass))
            connection.flush()
            
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
                        
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # If we've been capturing for more than 30 seconds, quit
            if time.time() - start > 30:
                print("Passou 30s")
                break
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    camera.led = True
    connection.close()
    clientSocket.close()
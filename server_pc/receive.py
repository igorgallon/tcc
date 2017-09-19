# Socket reference: https://pymotw.com/2/socket/tcp.html

import cv2
import numpy as np
import io
import socket
import struct
import pygame
from pygame.locals import *

HOST = ''
PORT = 8000

thresholdParam = 70

frameID = 1
frameClass = 0                                                      # ID of classification of current frame (1: foward / 2: left / 3: right)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
clientAddress = (HOST, PORT)
serverSocket.bind(clientAddress)                                    # Bind connection to Raspberry client

print('Waiting for a connection...')
# Listen for incoming connections
serverSocket.listen(1)

pygame.init()
pygame.display.set_mode()

# Accept a single connection and make a file-like object out of it
connection = serverSocket.accept()[0].makefile('rb')

try:
    while True:
        
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        
        image_mat = np.fromstring(image_stream.getvalue(), dtype=np.uint8)          # Converting image stream array into may numpy format 
        
        print("Decoding...")
        
        frame = cv2.imdecode(image_mat, 1)                                          # Decoding the image 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                             # Apply Gray filter
        frame = cv2.threshold(frame, thresholdParam, 255, cv2.THRESH_BINARY)[1]     # Binarizing image
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                print("key pressed")
                if event.key == K_UP:
                    frameClass = 1
                if event.key == K_LEFT:
                    frameClass = 2
                if event.key == K_RIGHT:
                    frameClass = 3
                
                # Save image in path format:
                # data_training/{class}.{image_num}.jpg
                cv2.imwrite('dataTraining/{classification}.{idf}.jpg'.format(classification=frameClass , idf=frameID) , frame)
                frameID += 1
        
        cv2.imshow("Streaming from Raspberry Pi", frame)
        cv2.waitKey(1)
        
finally:
    connection.close()
    serverSocket.close()
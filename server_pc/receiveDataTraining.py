# Socket reference: https://pymotw.com/2/socket/tcp.html

import cv2
import numpy as np
import io
import socket
import struct

class ReceiveDataTraining(object):
    
    def __init__(self, host):
        # Listen to all connections
        self.HOST = host
        self.PORT = 8000
        
        # Parameter used in binaryzation
        self.thresholdParam = 30

        self.frameID = 1
        self.verification = -1
        
        self.openConnection()
        
        
    def openConnection(self):
        # Create a TCP/IP socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientAddress = (self.HOST, self.PORT)
        self.serverSocket.bind(self.clientAddress) # Bind connection to Raspberry client
        
        print("[SERVER RECEIVE DATA TRAINING] Waiting for a Raspberry connection...")
        
        # Listen for incoming connections
        self.serverSocket.listen(1)
        
        print("[SERVER RECEIVE DATA TRAINING] Connection estabilished...")
        # Accept a single connection and make a file-like object out of it
        self.connection = self.serverSocket.accept()[0].makefile('rb')
    
    
    def closeConnection(self):
        print("[SERVER RECEIVE DATA TRAINING] Closing connection...")
        self.connection.close()
        self.serverSocket.close()        
        
        
    def receive(self):
        
        try:
            while True:        
                # Read the verification byte. If the verification is zero, quit the loop
                self.verification = struct.unpack('<I', self.connection.read(struct.calcsize('<I')))[0]
                if self.verification == 0:
                    break        
                
                # Read the classification of the current frame
                # (1: foward / 2: left / 3: right / 4: backward)
                frameClass = struct.unpack('<I', self.connection.read(struct.calcsize('<I')))[0]        
                
                print("[SERVER RECEIVE DATA TRAINING] Classification received: {}".format(frameClass))
                
                #Read the length of the image as a 32-bit unsigned int
                image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                
                #Construct a stream to hold the image data and read the image
                #data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connection.read(image_len))
                #Rewind the stream
                image_stream.seek(0)
                # Converting image stream array into may numpy format 
                image_mat = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
                
                frame = cv2.imdecode(image_mat, 1)  # Decoding the image 
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Apply Gray filter
                frame = cv2.threshold(frame, self.thresholdParam, 255, cv2.THRESH_BINARY)[1] # Binarizing image
                
                #Save image in path format:
                #data_training/{class_label}.{image_num}.jpg
                cv2.imwrite('dataTraining/{classification}.{idf}.jpg'.format(classification=frameClass , idf=self.frameID) , frame)
                self.frameID += 1
                
                cv2.imshow("Streaming from Raspberry Pi", frame)
                cv2.waitKey(1)
                
        finally:
            
            cv2.destroyWindow("Streaming from Raspberry Pi")
            self.closeConnection()
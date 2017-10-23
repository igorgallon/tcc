import socket
import struct
import json

class SendModel(object):
    
    def __init__(self, host):
        self.HOST = host
        self.PORT = 8000
        
        self.openConnection()    
    
    
    def openConnection(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
        self.clientAddress = (self.HOST, self.PORT)
    
        self.serverSocket.connect(self.clientAddress)                            # Connect to Raspberry client
    
        # Make a file-like object out of the connection
        self.connection = self.serverSocket.makefile('wb')
        
        
    def closeConnection(self):
        self.connection.close()
        self.serverSocket.close()
    
    
    def send(self):
        
        with open('model.json', 'r') as json_file:
            # Load the model from saved file - serialyze json object 
            json_data = json.load(json_file)
            jsonString = json.dumps(json_data)
            jsonBytes = jsonString.encode('utf-8')
            
            # Write the byte validation of message (1: valid / 0: not else)
            self.connection.write(struct.pack('<I', 1))
            self.connection.flush()            
            # Send the length of JSON string
            self.connection.write(struct.pack('<L', len(jsonBytes)))
            self.connection.flush()
            # Send model
            self.connection.write(jsonBytes)
            self.connection.flush()
            
            print("[SEND MODEL] JSON object sent")
            
            
        with open('model.h5', 'rb') as weights:
            modelBytes = weights.read()
            
            self.connection.write(struct.pack('<L', len(modelBytes)))
            self.connection.flush()            
            
            self.connection.write(modelBytes)
            self.connection.flush()
            
            print("[SEND MODEL] Model weights sent")
        
        # Write the byte validation zero signalling the end of trasmission
        self.connection.write(struct.pack('<I', 0))         
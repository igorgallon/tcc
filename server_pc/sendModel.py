import socket
import struct
import json

class SendModel(object):
    
    def __init__(self, host):
        self.HOST = host
        self.PORT = 8000
        
        self.openConnection()    
    
    
    def openConnection(self):
        # Create a TCP/IP socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientAddress = (self.HOST, self.PORT)
        
        print("[SERVER SEND MODEL] Trying to connect to Raspberry...")
        self.serverSocket.connect(self.clientAddress) # Connect to Raspberry client
    
        # Make a file-like object out of the connection
        self.connection = self.serverSocket.makefile('wb')
        
        
    def closeConnection(self):
        print("[SERVER SEND MODEL] Closing connection...")
        self.connection.close()
        self.serverSocket.close()
    
    
    def send(self):
        
        endTransmission = 0
        
        # Write the byte validation of message (1: valid / 0: not else)
        self.connection.write(struct.pack('<I', 1))
        self.connection.flush()           
        
        with open('model.json', 'r') as json_file:
            # Load the model from saved file - serialyze json object 
            json_data = json.load(json_file)
            jsonString = json.dumps(json_data)
            jsonBytes = jsonString.encode('utf-8')
            
            # Send the length of JSON string
            self.connection.write(struct.pack('<L', len(jsonBytes)))
            self.connection.flush()
            # Send model
            self.connection.write(jsonBytes)
            self.connection.flush()
            
            print("[SERVER SEND MODEL] Neural Network Model sent...")
            
            
        with open('model.h5', 'rb') as weights:
            modelBytes = weights.read()
            
            self.connection.write(struct.pack('<L', len(modelBytes)))
            self.connection.flush()            
            
            self.connection.write(modelBytes)
            self.connection.flush()
            
            print("[SERVER SEND MODEL] Weights sent...")
        
        # Write the byte validation zero signalling the end of trasmission
        self.connection.write(struct.pack('<I', 0))
        self.connection.flush()
        
        self.closeConnection()

        
        
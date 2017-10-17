import socket
import struct
import json

class SendModel(object):
    
    def openConnection(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
        self.clientAddress = (self.HOST, self.PORT)
    
        self.serverSocket.connect(self.clientAddress)                            # Connect to Raspberry client
    
        # Make a file-like object out of the connection
        self.connection = serverSocket.makefile('wb')
        
        
    def closeConnection(self):
        self.connection.close()
        self.serverSocket.close()
    
    
    def send(self):
        
        with open('model.json') as json_data:
            # Load the model from saved file 
            jsonString = json.load(json_data)
    
        
    def __init__(self, host):
        self.HOST = host
        self.PORT = 8000
        
        openConnection()
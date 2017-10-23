import io
import socket
import struct
import json

class ReceiveModel(object):
    
    def __init__(self, host):
        # Listen to all connections
        self.HOST = host
        self.PORT = 8000
        
        self.openConnection()
        
        
    def openConnection(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
        self.serverAddress = (self.HOST, self.PORT)
        self.clientSocket.bind(self.serverAddress)                               # Bind connection to Server PC
        
        print("[RASPBERRY] Waiting for Server connection...")
        
        # Listen for incoming connections
        self.clientSocket.listen(1)
        
        print("[RASPBERRY] Connection estabilished...")
        # Accept a single connection and make a file-like object out of it
        self.connection = self.clientSocket.accept()[0].makefile('rb')
    
    
    def closeConnection(self):
        print("[RASPBERRY] Closing connection")
        self.connection.close()
        self.clientSocket.close()        
        
        
    def receive(self):
        
        try:
            while True:        
                # Read the verification byte. If the verification is zero, quit the loop
                self.verification = struct.unpack('<I', self.connection.read(struct.calcsize('<I')))[0]
                if self.verification == 0:
                    break
                
                # Read length of JSON (NN model)
                json_length = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                
                # Receive JSON Neural Network model
                json_string = self.connection.read(json_length)
                #json_object = json.loads(json_string)
                
                # Receive length of model weights file
                weights_length = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                
                # Receive Model Weights file
                model_string = self.connection.read(weights_length)
                
                stream = io.BytesIO()
                # Save model
                with open("model.json", "w") as json_file:
                    stream.write(json_string)                    
                    json_file.write(stream.getvalue())
                    stream.seek(0)
                    
                print("JSON file saved!")
                
                with open("model.h5", "w") as weights_file:
                    stream.write(model_string)
                    weights_file.write(stream.getvalue())
                    stream.seek(0)
                
                print("Model weights saved!")

        finally:
            self.closeConnection()
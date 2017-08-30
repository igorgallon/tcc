# Socket reference: https://pymotw.com/2/socket/tcp.html

import socket

HOST = ''
PORT = 8000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a TCP/IP socket
serverAddress = (HOST, PORT)
print('starting up on %s port %s' % serverAddress)
clientSocket.bind(serverAddress)                                    # Bind connection to Raspberry client

# Listen for incoming connections
clientSocket.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = clientSocket.accept()
    
    try:
        print('connection from ', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('received "%s"' % data)
            if data:
                print ('sending data back to the client')
                connection.sendall(data)
            else:
                print('no more data from ' , client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()    
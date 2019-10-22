import socket
from phe import paillier

# create a socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()                           
portTrustee = 12345

# connection to hostname on the port.
clientSocket.connect((host, portTrustee))                               
# Receive no more than 1024 bytes
msg = clientSocket.recv(1024)                                

print(msg.decode('ascii'))
clientSocket.close()

#discussions here pls 
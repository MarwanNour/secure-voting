import socket
import json
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
public_key = msg.decode("ascii")
clientSocket.close()

# Client needs to vote
candidates = ['Donald Trump', 'Roger Federer', 'Britney Spears', 'Ali El Deek','Steve Jobs']

print("Choose your candidates (up to 2) among the list: "  + str(candidates))

# print(public_key)            

# Deserialize the public key
received_dict = json.loads(public_key)
pk = received_dict['public_key']
public_key_rec = paillier.PaillierPublicKey(n=int(pk['n']))
print(str(public_key_rec))


vote_count = 0
# choice is 0 by default so it can compute to 0 when encoded
choice = "-1"
summed_choices = 0

while(vote_count < 2):
    print("0 - Donald Trump")
    print("1 - Roger Federer")
    print("2 - Britney Spears")
    print("3 - Ali El Deek")
    print("4 - Steve Jobs")
    print("9  to exit")
    choice = int(input())
    #encode the choice
    if(choice == 9):
        break
    summed_choices += pow(10, choice)
    vote_count += 1 

print("summed choices " + str(summed_choices))

# now we encrypt with it the summed choices
encrypted_choices = public_key_rec.encrypt(summed_choices)

print(encrypted_choices)

# discussions here pls   


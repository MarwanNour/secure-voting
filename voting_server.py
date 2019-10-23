import socket
import json
from phe import paillier

# Create socket to get public key from trustee
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()                           
portTrustee = 10001
clientSocket.connect((host, portTrustee))                               
msg = clientSocket.recv(1024)                                
public_key = msg.decode("ascii")
clientSocket.close()

# Deserialize the public key
received_dict = json.loads(public_key)
pk = received_dict['public_key']
public_key_rec = paillier.PaillierPublicKey(n=int(pk['n']))
print(str(public_key_rec))


# Create socket to get votes from clients/voters
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10002
serv.bind((host, port))
serv.listen(5)

# make list of votes
vote_list_encrypted = []

# Allow certain number of clients to connect before proceeding
client_count = 0

# Receive encrypted_choices from client
while client_count < 2:     # MODIFY CLIENT COUNT
    conn, addr = serv.accept()
    print("Connection from client: ", addr)
    msg = conn.recv(1024)
    encrypted_choices_str = msg.decode("ascii")
    print(encrypted_choices_str)
    # Get EncryptedNumber because encrypted_choices is of type str
    encrypted_choices = paillier.EncryptedNumber(public_key_rec, encrypted_choices_str)
    print(encrypted_choices)
    # Add to list
    vote_list_encrypted.append(encrypted_choices)
    client_count += 1
    conn.close()


print(vote_list_encrypted)

# Add list to accumulator in JSON format
vote_list_encrypted_with_public_key = {}
vote_list_encrypted_with_public_key['values'] = [
    (str(x.ciphertext()), x.exponent) for x in vote_list_encrypted
    ]

print(vote_list_encrypted_with_public_key)

# # Send to Trustee Server
# serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostname()
# port = 10003
# serv.bind((host, port))
# serv.listen(5)


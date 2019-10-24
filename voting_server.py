# Author: Marwan Nour

import socket
import json
from phe import paillier

# Create Client Socket to get public key from trustee
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()                           
portTrustee = 10001
client_socket.connect((host, portTrustee))                               
msg = client_socket.recv(2000)                                
public_key = msg.decode("ascii")
client_socket.close()

# Deserialize the public key
received_dict = json.loads(public_key)
pk = received_dict['public_key']
public_key_rec = paillier.PaillierPublicKey(n=int(pk['n']))
print(str(public_key_rec))


# Create Server Socket to get votes from clients/voters
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10002
serv.bind((host, port))
serv.listen(5)

# make list of votes
vote_list_encrypted = []

# Allow certain number of clients to connect before proceeding
client_count = 0
supported_client_count = 2
# Receive encrypted_choices from client
while client_count < supported_client_count:     # MODIFY CLIENT COUNT
    conn, addr = serv.accept()
    print("Connection from client: ", addr)
    msg = conn.recv(2000)
    encrypted_choices_ciphertext_str = msg.decode("ascii")
    # RECEIVE THE CIPHERTEXT
    encrypted_choices_ciphertext = int(encrypted_choices_ciphertext_str)
    print(encrypted_choices_ciphertext)
    # CREATE THE ENCRYPTED NUMBER OBJECT FROM PUBLIC KEY AND CIPHERTEXT
    encrypted_choices = paillier.EncryptedNumber(public_key_rec, encrypted_choices_ciphertext)
    print(encrypted_choices)
    # Add to list
    vote_list_encrypted.append(encrypted_choices)
    client_count += 1
    conn.close()


print(vote_list_encrypted)

# Add list to accumulator in JSON format
vote_list_encrypted_with_public_key = {}

vote_list_encrypted_with_public_key['public_key'] = {'n': public_key_rec.n}
vote_list_encrypted_with_public_key['values'] = [
    (str(x.ciphertext()), x.exponent) for x in vote_list_encrypted
    ]

print(vote_list_encrypted_with_public_key)

serialized_list = json.dumps(vote_list_encrypted_with_public_key)

# Send to Trustee Server
# Create Client Socket
client_socket_trustee = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()                           
portTrustee = 10003
client_socket_trustee.connect((host, portTrustee))                               
msg = client_socket_trustee.send(serialized_list.encode())                                
client_socket_trustee.close()


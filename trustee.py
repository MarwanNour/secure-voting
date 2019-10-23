import socket
import json
from phe import paillier

public_key, private_key = paillier.generate_paillier_keypair()
# secret_list = [21, 34, 231]
# print(secret_list)
# encrypted_list = [public_key.encrypt(x) for x in secret_list]
# print(encrypted_list)
# print([private_key.decrypt(x) for x in encrypted_list])

# Encryption works

# Need to send public key to clients
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10001
serv.bind((host, port))
serv.listen(5)

# serialize to json
dict_public_key = {}
dict_public_key['public_key'] =  {'n': public_key.n}
serialized_public_key = json.dumps(dict_public_key)

print(serialized_public_key)

# number of connections: n clients + 1 voting server
num_connections = 0
# Send public key to clients and voting server 
while num_connections < 3:      # MODIFY NUMBER OF CONNECTIONS HERE LATER
    conn, addr = serv.accept()
    print("Connection from client: ", addr)
    # cast to string then encode into bytes
    conn.send(str(serialized_public_key).encode())
    conn.close()

# Receive accumulated votes from Voting server
# Create Server Socket
servTrustee = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
portTrustee = 10003
servTrustee.bind((host, port))
servTrustee.listen(5)
trusteeConn, trusteeAddr = servTrustee.accept()
print("Connected to trustee: ", trusteeAddr)
msg = trusteeConn.recv(1024)
trusteeConn.close()

serialized_dict = msg.decode("ascii")

# Deserialize the values from json
received_dict = json.loads(serialized_dict)
pk = received_dict['public_key']
public_key_rec = paillier.PaillierPublicKey(n=int(pk['n']))
vote_list_encrypted_with_public_key = [
    paillier.EncryptedNumber(public_key_rec, int(x[0]), int(x[1]))
    for x in received_dict['values']
]

print(public_key_rec)
print(vote_list_encrypted_with_public_key)

# Decrypt with Private Key
decrypted_list = [private_key.decrypt(x) for x in vote_list_encrypted_with_public_key]
print(decrypted_list)
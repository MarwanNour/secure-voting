import socket
import json
from phe import paillier

public_key, private_key = paillier.generate_paillier_keypair()

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
    # increment number of connections
    num_connections += 1
    conn.close()

# Receive accumulated votes from Voting server
# Create Server Socket
servTrustee = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
portTrustee = 10003
servTrustee.bind((host, portTrustee))
servTrustee.listen(5)
voting_conn, voting_addr = servTrustee.accept()
print("Connected to voting server: ", voting_addr)
msg = voting_conn.recv(3500)
voting_conn.close()

serialized_dict = msg.decode("ascii")


# # FOR TESTING: GETS THE NUMBER OF BYTES
# def utf8len(s):
#     return len(s.encode('utf-8'))

# print()
# print(serialized_dict)
# print(utf8len(serialized_dict))
# print()

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

# Get sum of votes
decrypted_list_sum = sum(decrypted_list)

candidates = ['Donald Trump', 'Roger Federer', 'Britney Spears', 'Ali El Deek','Steve Jobs']

zero_filled_sum = str(decrypted_list_sum).zfill(len(candidates))        # zero filled because the length of the sum might be less than length of list of candidates
print(zero_filled_sum)

# Reverse list
zero_filled_sum_reversed = zero_filled_sum[::-1]
print(zero_filled_sum_reversed)

# Put sum reversed in a list
def split(word): 
    return [char for char in word]  

reversed_sum_list = split(zero_filled_sum_reversed)
print(reversed_sum_list)

# put candidates and zero_filled_sum_reversed in dictionary
candidates_dict = dict(zip(candidates, reversed_sum_list))
print(candidates_dict)

# get maximum number of votes
# and winner
max_votes = 0
winner = ""

for x in candidates_dict:
    if(int(candidates_dict[x]) > max_votes):
        max_votes = int(candidates_dict[x])
        winner = x


winner_str  = "Winner : " + winner + "\n" + "Winner Votes : " + str(max_votes)
print(winner_str)

# send winner to client
# Create Client socket for trustee to send winner to client
# Client awaits message from trustee -> Client becomes server
winner_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_winner = 10004
winner_sock.connect((host, port_winner))
msg  = winner_sock.send(winner_str.encode())
winner_sock.close()

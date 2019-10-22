import socket
from phe import paillier

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 23456
serv.bind((host, port))
serv.listen(5)

# make list of votes
vote_list_encrypted = []
client_count = 0

# Receive encrypted_choices from client
while client_count < 2:     # MODIFY CLIENT COUNT
    conn, addr = serv.accept()
    print("Connection from client: ", addr)
    msg = conn.recv(1024)
    encrypted_choices = msg.decode("ascii")
    # add to accumulator
    vote_list_encrypted.append(encrypted_choices)
    client_count += 1
    conn.close()


print(encrypted_choices)
# Send the sum to Trustee Server


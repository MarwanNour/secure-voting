import socket
from phe import paillier

public_key, private_key = paillier.generate_paillier_keypair()
secret_list = [21, 34, 231]
print(secret_list)
encrypted_list = [public_key.encrypt(x) for x in secret_list]
print(encrypted_list)
print([private_key.decrypt(x) for x in encrypted_list])

# Encryption works

# Need to send public key to clients
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
serv.bind((host, port))
serv.listen(5)

while True:
    conn, addr = serv.accept()
    print("Connection from client", addr)
    conn.send("You have connected to MY SERVER")
    conn.close()
    
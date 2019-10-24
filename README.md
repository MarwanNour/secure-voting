# secure-voting
A secure voting framework using paillier cryptosystem (homomorphic encryption)

## Guidlines:
First run trustee.py, then run voting_server.py and then run client.py

### Notes:
- The following code accepts 2 clients/voters. You can modify the number of supported clients in the code to increase or decrease
the number of clients/voters. In order to do this, you need to modify the value of ``` supported_client_count ``` in ```voting_server.py```
and also in ```trustee.py```
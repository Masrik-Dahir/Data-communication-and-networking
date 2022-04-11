# Author: Masrik Dahir
# Date: 2021-05-04

# Sample input: GET /index.html HTTP/1.0

import socket
server_name = '127.0.0.1'
server_port = 8000

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_name, server_port))
sentence = input('Input: ')
# option = input('Options: ')
client.send(sentence.encode())
# client.send(option.encode())
modifiedSentence = client.recvfrom(2048)
print (modifiedSentence[0].decode())
client.close()
# Author: Masrik Dahir
# Date: 2021-05-04

# Sample input: GET /index.html HTTP/1.0

# p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*)(?P<path>[^\s]*)'
# link = re.search(p, url)
#
# host_name = link.group('host')
# print("host= " + host_name)
#
# port_name = link.group('port')
# if port_name == "":
#     port_name = "80"
#     addSlash = True
# print("port= " + port_name)
#
# path_name = link.group('path')
# if addSlash:
#     path_name = "/" + path_name
# if path_name == "":
#     path_name = "/"
# print("path= " + path_name)





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